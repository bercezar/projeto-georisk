import pandas as pd
from sqlalchemy import create_engine, inspect
import os
import sys


def create_database():

    db_folder = 'database'
    db_file = 'georisk.db'
    db_path = os.path.join(db_folder, db_file)

    try:
        # Cria a pasta database se ela não existir
        if not os.path.exists(db_folder):
            os.makedirs(db_folder)
            print(f"Pasta '{db_folder}' criada.")

        # 2. Conexão com o banco
        engine = create_engine(f'sqlite:///{db_path}')

        arquivos = {
            'ocorrencias': 'data/simulacao_chuvas_deslizamentos_rj.csv',
            'adaptacao': 'data/indice_capacidade_adaptativa.xlsx'
        }

        for nome, caminho in arquivos.items():
            if not os.path.exists(caminho):
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

        print("Lendo arquivos e padronizando dados...")

        df_ocorrencias = pd.read_csv(arquivos['ocorrencias'])
        df_adaptacao = pd.read_excel(arquivos['adaptacao'])

        if 'nome' in df_adaptacao.columns:
            df_adaptacao = df_adaptacao.rename(columns={'nome': 'municipio'})

        df_ocorrencias.columns = df_ocorrencias.columns.str.strip().str.lower()
        df_adaptacao.columns = df_adaptacao.columns.str.strip().str.lower()

        for df in [df_ocorrencias, df_adaptacao]:
            if 'municipio' in df.columns:
                df['municipio'] = df['municipio'].astype(
                    str).str.strip().str.lower()

        with engine.begin() as conn:
            df_ocorrencias.to_sql('ocorrencias', conn,
                                  if_exists='replace', index=False)
            df_adaptacao.to_sql('capacidade_adaptativa',
                                conn, if_exists='replace', index=False)

        # 8. Inspeção Final
        inspector = inspect(engine)
        tabelas = inspector.get_table_names()
        print(f"Sucesso! Banco populado. Tabelas existentes: {tabelas}")

    except Exception as e:
        print(f"Erro crítico durante a criação do banco: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_database()
