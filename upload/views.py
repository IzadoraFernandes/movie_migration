import pandas as pd
from sqlalchemy import create_engine
from django.shortcuts import render
from django.http import HttpResponse
import logging
import io

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do banco de dados
DATABASE_URI = 'postgresql://postgres:pgadmin@localhost:5432/migration_data'
engine = create_engine(DATABASE_URI)

# Função para carregar CSV em chunks e inserir no banco
def load_csv_to_db(file, table_name, chunksize=10000):
    try:
        for chunk in pd.read_csv(io.StringIO(file.read().decode('utf-8')), chunksize=chunksize):
            chunk.to_sql(table_name, engine, if_exists='append', index=False)
            logger.info(f"Chunk inserido na tabela {table_name}")
    except Exception as e:
        logger.error(f"Erro ao inserir dados na tabela {table_name}: {e}")

def upload_files(request):
    if request.method == 'POST':
        files = {
            'movies': request.FILES['movies'],
            'genome_scores': request.FILES['genome_scores'],
            'genome_tags': request.FILES['genome_tags'],
            'links': request.FILES['links'],
            'ratings': request.FILES['ratings'],
            'tags': request.FILES['tags']
        }

        for name, file in files.items():
            try:
                load_csv_to_db(file, name)
            except Exception as e:
                logger.error(f"Erro ao processar o arquivo {name}: {e}")
                return HttpResponse(f"Erro ao carregar o arquivo {name}.")

        return HttpResponse('Arquivos carregados com sucesso!')
    return render(request, 'upload_form.html')
