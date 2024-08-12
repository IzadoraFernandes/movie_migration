# Migração de dados com Postgresql
Repositório criado para desenvolvimento de projeto para leitura e escrita de arquivos CSV's para um banco de dados relacional Postgresql.

### O que foi utilizado para desenvolver o projeto: 
Django;
Html;
Css;
Buutstrap;

Máterial do   YouTube: https://www.youtube.com/watch?v=VXMJHcO5Zvs&t=1898s 


## Instalação e execução do projeto:

### Criando e ativando a virtual env:
python -m venv env
Source env/bin/activate 

### Instalando os pacotes do projeto:
pip install -r requirements.txt 

### Rodando o projeto:


python manage.py runserver 

### Acessar a URL e adicionar os arquivos:
http://127.0.0.1:8000/upload/

### Para leitura e escrita dos arquivos, utilizei a biblioteca Chunk.
pip install django-multiple-chunk-upload

## Estrutura do DB: 
![jerf](https://github.com/user-attachments/assets/5a89e029-2bc4-4a67-9b17-bd6a9e3063f9)




