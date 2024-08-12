import pandas as pd
from sqlalchemy import create_engine
from django.shortcuts import render
from django.http import HttpResponse
import logging
import io
from upload.models import *
from django.db.models import Q
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URI = 'postgresql://postgres:pgadmin@localhost:5432/migration_data'
engine = create_engine(DATABASE_URI)

def load_csv_to_db(file, table_name, chunksize=100000):
    try:
        # Verifica se a tabela existe no banco de dados
        if not engine.dialect.has_table(engine, table_name):
            logger.error(f"Tabela {table_name} não encontrada no banco de dados.")
            return

        # Ler o arquivo CSV em pedaços (chunks)
        for chunk in pd.read_csv(io.StringIO(file.read().decode('utf-8')), chunksize=chunksize):
            # Verifica se a coluna "timestamp" existe e converte para datetime e depois para bigint
            if 'timestamp' in chunk.columns:
                chunk['timestamp'] = pd.to_datetime(chunk['timestamp'], unit='s', errors='coerce')
                chunk['timestamp_bigint'] = chunk['timestamp'].apply(lambda x: int(time.mktime(x.timetuple())) if pd.notna(x) else None)

            # Insere o chunk no banco de dados
            chunk.to_sql(table_name, engine, if_exists='append', index=False)
            logger.info(f"Chunk inserido na tabela {table_name}")
    except Exception as e:
        logger.error(f"Erro ao inserir dados na tabela {table_name}: {e}")

def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        table_name = request.POST.get('table_name')

        if file and table_name:
            try:
                load_csv_to_db(file, table_name)
                return HttpResponse(f'Arquivo {file.name} carregado com sucesso na tabela {table_name}!')
            except Exception as e:
                logger.error(f"Erro ao processar o arquivo {file.name}: {e}")
                return HttpResponse(f"Erro ao carregar o arquivo {file.name}.")
        else:
            return HttpResponse("Por favor, envie um arquivo e forneça o nome da tabela.")

    return render(request, 'upload_form.html')

def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(genres__name__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    return render(request, 'search_results.html', {'results': results, 'query': query})
