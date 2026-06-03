import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os

# --- CONSTANTES DE ESTILO ---
COLOR_SEQUENCE = ["#0f766e", "#2563eb",
                  "#dc2626", "#7c3aed", "#ca8a04", "#475569"]
DARK_COLOR_SEQUENCE = ["#2dd4bf", "#60a5fa",
                       "#fb7185", "#c084fc", "#facc15", "#94a3b8"]

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GeoRisk Dashboard",
                   layout="wide", page_icon="🌧️")

# --- CSS PERSONALIZADO (ESTÉTICA E GRADIENTE) ---


def apply_custom_css():
    st.markdown("""
        <style>
        .stApp { background: #020617; color: #f8fafc; }
        
        /* Justificação do texto e centralização básica */
        div[data-testid="stMarkdownContainer"] p { text-align: justify; }
        h1, h2, h3 { text-align: center; }
        .block-container { max-width: 70%; margin: auto; padding-top: 10rem; }
        
        /* Estilo das Métricas dentro do Gradiente */
        .kpi-row {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            flex-wrap: wrap;
        }
        
        .kpi-box {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(45, 212, 191, 0.3);
            border-top: 3px solid #2dd4bf;
            padding: 1.5rem;
            border-radius: 8px;
            min-width: 180px;
        }
        
        .kpi-box span {
            display: block;
            color: #99f6e4;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        
        .kpi-box strong {
            color: #f8fafc;
            font-size: 2.2rem;
            line-height: 1;
        }

        /* Restante do teu CSS original */
        .metric-card-container { 
                background: #111827; border: 1px solid #334155; padding: 2rem; border-radius: 12px; margin-bottom: 2rem; text-align: center; 
        }
        .stButton > button { 
            width: 100%; 
            min-height: 58px; 
            padding: 0 28px; 
            border-radius: 8px; 
            border: 1px solid #020024; 
            background: linear-gradient(90deg, rgba(2, 0, 36, 1) 0%, rgba(9, 9, 121, 1) 100%, rgba(27, 171, 204, 1) 100%) !important; 
            color: #ffffff !important; 
            font-size: 1.08rem; 
            font-weight: 700;
            transition: all 0.3s ease; 
        }
        .stButton > button:hover {
            border-color: #2dd4bf !important; 
            box-shadow: 0 0 18px rgba(45, 212, 191, 0.6) !important;
            transform: translateY(-2px);
            
        }

        .intro-card-container { 
                background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 2.5rem; margin-top: 1rem; margin-bottom: 2rem;
        }
        .intro-card-container h3 { 
                color: #1BABCC !important; margin-top: 0; margin-bottom: 1.5rem; font-size: 1.8rem; 
        }
        .intro-card-container p { 
                color: #e2e8f0; line-height: 1.6; margin-bottom: 1rem; 
        }
        </style>
    """, unsafe_allow_html=True)


# --- 2. CONTROLO DE NAVEGAÇÃO ---
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = 'apresentacao'


def mudar_pagina(nova_pagina):
    st.session_state.pagina_atual = nova_pagina

# --- 3. CARREGAMENTO DE DADOS ---


@st.cache_data
def load_data():
    caminho_banco = os.path.abspath(os.path.join("database", "georisk.db"))
    engine = create_engine(f"sqlite:///{caminho_banco}")
    df_historico = pd.read_sql("SELECT * FROM ocorrencias", engine)

    query_2015 = """
        SELECT o.municipio, o.ocorrencias_deslizamento, o.obitos, o.desalojados,
               c.valor_adaptativo, c.classe_adaptativa, c.valor_per_capita, c.classe_per_capita
        FROM ocorrencias o JOIN capacidade_adaptativa c ON o.municipio = c.municipio
        WHERE o.ano = 2015
    """
    df_2015 = pd.read_sql(query_2015, engine)
    return df_historico, df_2015


df_historico, df_2015 = load_data()

# --- 4. PÁGINA 1: APRESENTAÇÃO ---
if st.session_state.pagina_atual == 'apresentacao':
    apply_custom_css()
st.markdown("""
            <style>
            .artistic-title-container {
                text-align: center;
                margin-bottom: 3rem;
                margin-top: 1rem;
            }
            .georisk-logo {
                font-size: 5rem;
                font-weight: 900;
                /* O truque mágico: Gradiente aplicado diretamente na fonte */
                background: linear-gradient(90deg, #2dd4bf 0%, #3b82f6 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: -2px;
                display: block;
                line-height: 1.1;
            }
            .georisk-subtitle {
                font-size: 1.4rem;
                color: #94a3b8;
                font-weight: 400;
                letter-spacing: 3px;
                text-transform: uppercase;
                margin-top: 0.5rem;
                display: block;
            }
            </style>
            
            <div class="artistic-title-container">
                <span class="georisk-logo">GeoRisk</span>
                <span class="georisk-subtitle">Análise de Riscos no Rio de Janeiro</span>
            </div>
        """, unsafe_allow_html=True)
# st.sidebar.header("Filtros Gerais")
# mun = st.sidebar.selectbox("Selecione o Município (Visão Geral):",
#                            ["Todos"] + sorted(df_historico['municipio'].unique().tolist()))

# df_f = df_historico if mun == "Todos" else df_historico[df_historico['municipio'] == mun]

# col_esq, col_centro, col_dir = st.columns([1.5, 4, 1.5])

# with col_centro:
#     # TUDO AQUI DENTRO VAI FICAR COM O FUNDO AZUL GRADIENTE
#     with st.container():
#         # A âncora que chama o CSS
#         st.markdown('<span id="meu-fundo-gradiente"></span>',
#                     unsafe_allow_html=True)

#         st.markdown("<h1>GeoRisk: Análise de Riscos no RJ</h1>",
#                     unsafe_allow_html=True)

#         # O SELETOR ESTÁ AQUI, NATIVO E FUNCIONANDO!
#         _, col_filtro, _ = st.columns([1, 2, 1])
#         with col_filtro:
#             mun = st.selectbox("Selecione o Município (Visão Geral):", [
#                                "Todos"] + sorted(df_historico['municipio'].unique().tolist()))

#         # O Python filtra os dados
#         df_f = df_historico if mun == "Todos" else df_historico[df_historico['municipio'] == mun]

#         val_ocorrencias = f"{df_f['ocorrencias_deslizamento'].sum():,.0f}".replace(
#             ",", ".")
#         val_obitos = f"{df_f['obitos'].sum():,.0f}".replace(",", ".")
#         val_desalojados = f"{df_f['desalojados'].sum():,.0f}".replace(
#             ",", ".")

#         # AS CAIXAS DE KPI, USANDO A SUA ESTRUTURA HTML ORIGINAL
#         st.markdown(f"""
#         <div class="kpi-row">
#             <div class="kpi-box">
#                 <span>Ocorrências</span>
#                 <strong>{val_ocorrencias}</strong>
#             </div>
#             <div class="kpi-box">
#                 <span>Óbitos</span>
#                 <strong>{val_obitos}</strong>
#             </div>
#             <div class="kpi-box">
#                 <span>Desalojados</span>
#                 <strong>{val_desalojados}</strong>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
st.markdown(
    """
<div class="intro-card-container">
<h3>Sobre</h3>
<p>O GeoRisk é uma plataforma voltada à análise de riscos geológicos e impactos socioambientais no estado do Rio de Janeiro. Por meio da integração de dados históricos de deslizamentos, precipitação e indicadores de capacidade adaptativa municipal, a plataforma oferece suporte à compreensão de padrões de vulnerabilidade e risco entre os anos de 2014 e 2024.</p>
</div>

<div class="intro-card-container">
<h3>Desenvolviemento e Funcionalidades</h3>
<p>O projeto foi desenvolvido a partir da análise da base <strong>simulacao_chuvas_deslizamentos.csv</strong>, fornecida no Projeto G2 - Tema 2, contendo informações sobre precipitação, ocorrências de deslizamentos, nível de risco, óbitos e desalojados em municípios do estado do Rio de Janeiro.</p>
<p>Para enriquecer as análises, foi realizada a integração dessa base com indicadores de capacidade adaptativa e investimento per capita obtidos na plataforma <strong><a href="https://data.inpe.br/geonetwork/srv/api/records/adaptabrasil60005" target="_blank" style="color: #2dd4bf;">
AdaptaBrasil</a></strong>, considerando os dados referentes ao ano de 2015. O cruzamento foi realizado por meio da identificação dos municípios em comum entre as duas bases, permitindo investigar possíveis relações entre investimentos em adaptação climática, capacidade de resposta municipal e impactos causados pelos deslizamentos.</p>
<p>Os dados foram modelados e armazenados em um banco de dados SQLite utilizando SQLAlchemy, possibilitando consultas relacionais e integração entre as tabelas. A partir dessa estrutura foram desenvolvidos indicadores dinâmicos, visualizações analíticas e dashboards interativos utilizando Streamlit.</p>
<p>Além das análises exploratórias, foi implementado um modelo de árvore de decisão para investigar como variáveis como precipitação, nível de risco e índice do solo influenciam a classificação dos eventos analisados.</p>
<ul style="color: #e2e8f0; line-height: 1.6;">
<li>✅ Integração e cruzamento de bases de dados distintas</li>
<li>✅ Modelagem relacional com SQLAlchemy e SQLite</li>
<li>✅ KPIs dinâmicos e indicadores de impacto</li>
<li>✅ Dashboards organizados em múltiplas seções</li>
<li>✅ Aplicação web interativa com Streamlit</li>
<li>✅ Análise exploratória e visualização de dados</li>
<li>✅ Aplicação de modelo de árvore de decisão</li>
</ul>
</div>

<div class="intro-card-container">
<h3>Tecnologias Utilizadas</h3>
<p>O ecossistema deste projeto foi dividindo claramente as responsabilidades de Front-end, Back-end e Processamento de Dados:</p>
<ul style="color: #e2e8f0; line-height: 1.8;">
<li><strong>Streamlit:</strong> Framework de Front-end para renderização de aplicações Web dinâmicas (SPA).</li>
<li><strong>Python & Pandas:</strong> Motor principal de processamento lógico e agregação matemática de dados em tempo de execução.</li>
<li><strong>SQLite & SQLAlchemy:</strong> Banco de dados relacional e ORM para abstração e segurança nas integrações lógicas.</li>
<li><strong>HTML5 & CSS3:</strong> Customização avançada de UI/UX, utilizando Flexbox para estruturação responsiva dos componentes.</li>
<li><strong>Plotly Express:</strong> Biblioteca de DataViz para renderização de gráficos e mapeamento geográfico interativo.</li>
</ul>
</div>
""",
    unsafe_allow_html=True
)
if st.button("📊 ACESSAR DASHBOARD DE DADOS", use_container_width=True, type="primary"):
    mudar_pagina('dashboard')

# --- 5. PÁGINA 2: O DASHBOARD ---
elif st.session_state.pagina_atual == 'dashboard':
    apply_custom_css()

    col_titulo, col_botao = st.columns([4, 1])
    with col_titulo:
        st.title("📊 GeoRisk: Painel Analítico")
    with col_botao:
        if st.button("⬅️ Voltar"):
            st.session_state.show_dashboard = False
            st.rerun()

    st.markdown("---")

    st.sidebar.header("Filtros")
    mun = st.sidebar.selectbox(
        "Município:", ["Todos"] + sorted(df_historico['municipio'].unique().tolist()))
    df_f = df_historico if mun == "Todos" else df_historico[df_historico['municipio'] == mun]

    st.markdown("### Indicadores de Impacto")
    with st.container():
        st.markdown('<div class="metric-card-container">',
                    unsafe_allow_html=True)
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Ocorrências",
                  f"{df_f['ocorrencias_deslizamento'].sum():,.0f}")
        k2.metric("Óbitos", f"{df_f['obitos'].sum():,.0f}")
        k3.metric("Desalojados", f"{df_f['desalojados'].sum():,.0f}")
        k4.metric("Mun. Top", df_historico.groupby('municipio')
                  ['ocorrencias_deslizamento'].sum().idxmax())
        st.markdown('</div>', unsafe_allow_html=True)

    aba1, aba2 = st.tabs(
        ["📈 Panorama Histórico", "🏙️ Capacidade vs Investimento (2015)"])
    with aba1:
        st.write("Gráficos de evolução aqui...")
    with aba2:
        st.write("Gráficos de 2015 aqui...")
