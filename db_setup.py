import pandas as pd
from sqlalchemy import create_engine, inspect
import os
import sys


def create_database():
    # Configuração
    db_folder = 'database'
    db_file = 'georisk.db'
    db_path = os.path.join(db_folder, db_file)

    try:
        if not os.path.exists(db_folder):
            os.makedirs(db_folder)
            print(f"Pasta '{db_folder}' criada.")

        # Conexão
        engine = create_engine(f'sqlite:///{db_path}')

        # Mapeamento de arquivos
        arquivos = {
            'ocorrencias': 'data/simulacao_chuvas_deslizamentos_rj.csv',
            'adaptacao': 'data/indice_capacidade_adaptativa.xlsx',
        }

        # Validação
        for nome, caminho in arquivos.items():
            if not os.path.exists(caminho):
                raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

        print("Lendo arquivos e padronizando dados...")

        df_ocorrencias = pd.read_csv(arquivos['ocorrencias'])
        df_adaptacao = pd.read_excel(arquivos['adaptacao'])

        df_ocorrencias.columns = df_ocorrencias.columns.str.strip().str.lower()
        df_adaptacao.columns = df_adaptacao.columns.str.strip().str.lower()
        # Padronização de nomes de municípios para o JOIN funcionar
        for df in [df_ocorrencias, df_adaptacao]:
            df['municipio'] = df['municipio'].astype(
                str).str.strip().str.lower()

        with engine.begin() as conn:
            df_ocorrencias.to_sql('ocorrencias', conn,
                                  if_exists='replace', index=False)
            df_adaptacao.to_sql('capacidade_adaptativa',
                                conn, if_exists='replace', index=False)

        inspector = inspect(engine)
        tabelas = inspector.get_table_names()
        print(f"Sucesso! Banco populado. Tabelas existentes: {tabelas}")

    except Exception as e:
        print(f"Erro durante a criação do banco: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_database()
