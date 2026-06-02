import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os


st.set_page_config(page_title="Dashboard GeoRisk",
                   layout="wide", page_icon="📊")
st.title("📊 GeoRisk - Análise de Vulnerabilidade e Deslizamentos")
st.markdown("---")


db_path = os.path.join("database", "georisk.db")
engine = create_engine(f'sqlite:///{db_path}')


@st.cache_data
def load_data():

    query = """
    SELECT 
        o.*, 
        c.valor_adaptativo,
        c.classe_adaptativa,
        c.valor_per_capita,
        c.classe_per_capita
    FROM ocorrencias o
    LEFT JOIN capacidade_adaptativa c ON o.municipio = c.municipio
    """
    return pd.read_sql(query, engine)


try:
    df = load_data()
    st.success("Banco de dados conectado e cruzamento realizado com sucesso!")

    # Imprime a tabela crua na tela para validação
    st.subheader("Visualização da Base Consolidada")
    st.dataframe(df)

except Exception as e:
    st.error(f"Erro ao conectar ou ler o banco: {e}")
