import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os
from sklearn.tree import DecisionTreeClassifier

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GeoRisk Dashboard",
                   layout="wide", page_icon="📊")


st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    .metric-card-container {
        background: #171717; border: 1px solid #262626; padding: 2rem;
        border-radius: 12px; text-align: center; margin-bottom: 2rem;
    }

    .kpi-row-dash {
        display: flex;
        justify-content: space-between;
        gap: 1.5rem;
        flex-wrap: wrap;
        margin-bottom: 2rem;
        padding: 2rem;
        background: #020617;
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        border: 1px solid #1e293b;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }

    .kpi-box-dash {
        flex: 1;
        background: rgba(15, 23, 42, 0.6);

        border: 1px solid #0284c7;
        border-top: 3px solid #00d4ff;

        padding: 1.5rem;
        border-radius: 8px;
        min-width: 200px;
        text-align: center;

        box-shadow: 0 0 15px rgba(0, 212, 255, 0.15);
    }

    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        justify-content: center !important;
        gap: 0 !important;
        border-bottom: none !important;
    }

    .stTabs [data-baseweb="tab-list"] button {
        flex-grow: 1 !important;
        max-width: 300px !important;
        background-color: transparent !important;
        border-radius: 0 !important;
        transition: all 0.3s ease !important;
        padding: 10px 20px !important;
    }

    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: transparent !important;
        border-bottom: 2px solid #00d4ff !important;
        box-shadow: none !important;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: transparent !important;
        border-bottom: 3px solid #00d4ff !important;
        box-shadow: none !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        border-bottom: none !important;
    }

    .stTabs [data-baseweb="tab-list"] button:hover p,
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] p {
        color: #00d4ff !important;
        font-weight: 700 !important;
        text-shadow: 0 0 8px rgba(0, 212, 255, 0.4) !important;
    }

    .stTabs [data-baseweb="tab-list"] button p {
        color: #94a3b8 !important;
        transition: color 0.3s ease !important;
    }

    .stTabs [data-baseweb="tab-list"] button:focus,
    .stTabs [data-baseweb="tab-list"] button:focus-visible {
        outline: none !important;
        background-color: transparent !important;
    }

    .kpi-box-dash span {
        display: block;
        color: ##94a3b8;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }

    .kpi-box-dash strong {
        color: #00d4ff;
        font-size: 2.2rem;
        line-height: 1;
        font-weight: 700;
        text-shadow: 0 0 8px rgba(0, 212, 255, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNÇÕES DE DADOS E ML ---


@st.cache_data
def load_data():
    database_path = os.path.abspath(os.path.join("database", "georisk.db"))
    engine = create_engine(f"sqlite:///{database_path}")

    query = """
        SELECT o.*, c.valor_adaptativo, c.classe_adaptativa, c.valor_per_capita
        FROM ocorrencias o
        LEFT JOIN capacidade_adaptativa c ON o.municipio = c.municipio
    """
    df = pd.read_sql(query, engine)
    return df


@st.cache_resource
def train_model(df):
    features = ['chuva_mm', 'indice_solo', 'municipio', 'regiao_rj']
    target = 'nivel_risco'

    df_model = df[features + [target]].dropna()

    X = df_model[features].copy()
    y = df_model[target]

    cidades = sorted(X['municipio'].unique())
    mapa_cidades = {cidade: idx for idx, cidade in enumerate(cidades)}
    X['municipio'] = X['municipio'].map(mapa_cidades)

    regioes = sorted(X['regiao_rj'].unique())
    mapa_regioes = {regiao: idx for idx, regiao in enumerate(regioes)}
    X['regiao_rj'] = X['regiao_rj'].map(mapa_regioes)

    model = DecisionTreeClassifier(max_depth=4, min_samples_split=20)
    model.fit(X, y)

    # 4. Cruzar Município -> Região
    dic_cidade_regiao = df[['municipio', 'regiao_rj']].drop_duplicates(
    ).set_index('municipio')['regiao_rj'].to_dict()

    return model, cidades, mapa_regioes, dic_cidade_regiao


# Inicialização do Dataset e Modelo
df_completo = load_data()
modelo_ia, lista_cidades_ia, mapa_regioes_ia, dic_cidade_regiao_ia = train_model(
    df_completo)


# --- CABEÇALHO E FILTROS ---
st.title("📊 GeoRisk: Painel Analítico")
st.link_button("⬅️ Voltar para a Home",
               "https://bercezar.github.io/projeto-georisk/")
st.markdown("---")


_, col_filtros, _ = st.columns([1, 2, 1])
with col_filtros:
    st.markdown("<h4 style='text-align: center; color: #94a3b8; margin-bottom: 1rem;'></h4>",
                unsafe_allow_html=True)

    mun = st.selectbox(
        "Município:",
        ["Todos"] + sorted(df_completo['municipio'].unique().tolist())
    )

    ano_selecionado = st.slider(
        "Selecione o Ano:",
        int(df_completo['ano'].min()),
        int(df_completo['ano'].max()),
        (2014, 2024)
    )

# Filtros globais
filtered_df = df_completo.copy()
if mun != "Todos":
    filtered_df = filtered_df[filtered_df['municipio'] == mun]

filtered_df = filtered_df[(filtered_df['ano'] >= ano_selecionado[0]) &
                          (filtered_df['ano'] <= ano_selecionado[1])]

# --- KPIs GLOBAIS ---
st.markdown("### Indicadores de Impacto")
with st.container():

    val_ocorrencias = f"{filtered_df['ocorrencias_deslizamento'].sum():,.0f}".replace(
        ",", ".")
    val_obitos = f"{filtered_df['obitos'].sum():,.0f}".replace(",", ".")
    val_desalojados = f"{filtered_df['desalojados'].sum():,.0f}".replace(
        ",", ".")

    # Formatação para chuva acumulada
    chuva_acumulada = filtered_df['chuva_mm'].sum()
    txt_chuva = f"{chuva_acumulada:,.1f}"
    val_chuva_max = txt_chuva.replace(",", "X").replace(
        ".", ",").replace("X", ".") + " mm"

    st.markdown(f"""
    <div class="kpi-row-dash">
        <div class="kpi-box-dash">
            <span>Ocorrências</span>
            <strong>{val_ocorrencias}</strong>
        </div>
        <div class="kpi-box-dash">
            <span>Óbitos</span>
            <strong>{val_obitos}</strong>
        </div>
        <div class="kpi-box-dash">
            <span>Desalojados</span>
            <strong>{val_desalojados}</strong>
        </div>
        <div class="kpi-box-dash">
            <span>Chuva Máx Registrada</span>
            <strong>{val_chuva_max}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)


# --- ABAS ---
aba1, aba2, aba3, aba4, aba5 = st.tabs(
    ["📈 Panorama Histórico", "🔬 Modo Exploração", "📊 Análises Comparativas", "🗺️ Mapa de Concentração", "🤖 GeoRisk Classificador de Risco"])


# Séries Temporais
with aba1:
    st.subheader("Evolução Temporal de Ocorrências e Desalojados")

    df_timeline = filtered_df.groupby(
        'ano')[['ocorrencias_deslizamento', 'desalojados']].sum().reset_index()

    fig_linha = px.line(df_timeline, x='ano', y='ocorrencias_deslizamento',
                        title="Ocorrências ao longo dos anos", markers=True, template="plotly_dark")
    st.plotly_chart(fig_linha, use_container_width=True)
    with st.expander("🔍 Análise dos dados (2014-2024)"):
        st.markdown("""
        O gráfico apresenta o comportamento das ocorrências de 2014 a 2024 nas cidades selecionadas (Niterói, Rio, Nova Iguaçu, Petrópolis, Teresópolis, Angra dos Reis, Campos dos Goytacazes e Nova Friburgo).

        * **Comportamento Distinto:** Não existe um padrão único para todas as cidades. Petrópolis e Friburgo, por exemplo, mostram picos de ocorrências que não aparecem com a mesma intensidade nas cidades da baixada ou no litoral. Isso confirma que a topografia é o fator que mais pesa nos dados.
        
        * **Dependência de Fatores Climáticos:** Os dados mostram que os picos de ocorrência estão ligados diretamente aos anos de maior pluviosidade. O sistema não mostra uma redução consistente de riscos ao longo da década, o que indica que as medidas preventivas atuais não estão acompanhando o ritmo dos eventos climáticos.
        
        * **Conclusão:** O histórico desses 11 anos prova que o problema não é igual para todos os municípios. O GeoRisk serve para mostrar que, para gerir o risco nessas cidades, não dá para usar a mesma régua. Cada cidade tem uma resposta diferente para o mesmo volume de chuva.
        """)


# Análise Exploratória
with aba2:
    st.subheader("Exploração Dinâmica de Variáveis")
    st.write("Selecione as variáveis abaixo para descobrir correlações entre clima, impacto e capacidade adaptativa.")
    display_labels = {
        'chuva_mm': 'Precipitação (mm)',
        'temperatura_media': 'Temperatura Média (°C)',
        'ocorrencias_deslizamento': 'Ocorrências de Deslizamento',
        'desalojados': 'Total de Desalojados',
        'obitos': 'Total de Óbitos',
        'indice_solo': 'Índice do Solo',
        'umidade': 'Umidade Relativa',
        'valor_adaptativo': 'Índice Adaptativa',
        'municipio': 'Município',
        'regiao_rj': 'Região RJ',
        'nivel_risco': 'Nível de Risco',
        'classe_adaptativa': 'Classe Adaptativa',
        'valor_per_capita': 'Índice Per Capita',
        'classe_per_capita': 'Classe de Investimento Per Capita'
    }

    col_x, col_y, col_color = st.columns(3)

    numeric_features = ['chuva_mm', 'temperatura_media', 'ocorrencias_deslizamento',
                        'desalojados', 'obitos', 'indice_solo', 'umidade', 'valor_adaptativo', 'valor_per_capita', 'classe_per_capita']
    categorical_features = ['municipio', 'regiao_rj',
                            'nivel_risco', 'classe_adaptativa']

    with col_x:
        axis_x = st.selectbox(
            "Eixo X (Causa/Dimensão):",
            numeric_features + categorical_features,
            index=0,
            format_func=lambda x: display_labels.get(x, x)
        )
    with col_y:
        axis_y = st.selectbox(
            "Eixo Y (Efeito/Métrica):",
            numeric_features,
            index=2,
            format_func=lambda x: display_labels.get(x, x)
        )
    with col_color:
        grouping_feature = st.selectbox(
            "Colorir por (Agrupamento):",
            categorical_features,
            index=2,
            format_func=lambda x: display_labels.get(x, x)
        )

    dynamic_title = f"Relação: {display_labels.get(axis_x, axis_x)} vs {display_labels.get(axis_y, axis_y)}"

    dynamic_fig = px.scatter(
        filtered_df,
        x=axis_x,
        y=axis_y,
        color=grouping_feature,
        hover_data=['municipio'],
        template="plotly_dark",
        opacity=0.7,
        title=dynamic_title,
        labels=display_labels
    )

    st.plotly_chart(dynamic_fig, use_container_width=True)
    with st.expander("🔍 Guia de Análise: Identificando Padrões"):
        st.markdown("""
        Esta visualização dinâmica permite cruzar variáveis para identificar correlações que não são óbvias à primeira vista. Ao manipular os eixos, considere os seguintes pontos de análise:

        * **Eixo X vs. Y (Causa e Efeito):** Ao colocar 'Precipitação' no X e 'Ocorrências' no Y, procure por *limiares de inclinação*. Se os pontos formam um agrupamento que sobe rapidamente a partir de certo ponto de chuva, você identificou o ponto crítico onde a infraestrutura local tende a falhar.

        * **A força da cor (Agrupamento):** Ao colorir por 'Município' ou 'Classe Adaptativa', você consegue ver se os problemas são generalizados ou se estão concentrados em grupos específicos. Se uma classe de "Alta Adaptabilidade" ainda apresenta muitos pontos de alta ocorrência (no topo do gráfico), isso indica uma falha na eficácia das medidas de mitigação em certas áreas, independente do índice oficial.

        * **Detecção de Anomalias:** Observe os pontos isolados (outliers). Eles representam eventos fora da curva — seja um município com muita chuva e pouca ocorrência (possível exemplo de boa gestão local) ou pouca chuva e muita ocorrência (indicativo de alta vulnerabilidade geomorfológica).

        **O objetivo desta ferramenta não é provar uma regra única, mas sim mostrar que os dados são variáveis e complexos.** O GeoRisk fornece a liberdade para que o tomador de decisão explore diferentes cenários e entenda que o risco geológico no Rio de Janeiro depende de múltiplos fatores que variam de cidade para cidade.
        """)
# Rankings e Distribuição
with aba3:
    st.subheader("Rankings e Distribuição de Impacto")
    st.write(
        "Análise comparativa entre municípios e suas respectivas classes adaptativas.")

    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:

        df_top10 = filtered_df.groupby(
            'municipio')['ocorrencias_deslizamento'].sum().nlargest(10).reset_index()

        fig_barras = px.bar(
            df_top10,
            x='ocorrencias_deslizamento',
            y='municipio',
            orientation='h',
            title="Top 10 Municípios (Mais Ocorrências)",
            template="plotly_dark",
            color='ocorrencias_deslizamento',
            color_continuous_scale="Blues"
        )

        fig_barras.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_barras, use_container_width=True)

    with col_graf2:
        df_rosca = filtered_df.groupby('classe_adaptativa')[
            'desalojados'].sum().reset_index()

        fig_rosca = px.pie(
            df_rosca,
            values='desalojados',
            names='classe_adaptativa',
            hole=0.4,
            title="Desalojados vs Capacidade Adaptativa",
            template="plotly_dark",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        st.plotly_chart(fig_rosca, use_container_width=True)
    with st.expander("🔍 Análise Técnica: O Paradoxo da Adaptabilidade"):
        st.markdown("""
        Um dado contraintuitivo emerge ao cruzar a Capacidade Adaptativa com o número de desalojados: cidades com maior índice adaptativo, em termos absolutos, frequentemente apresentam maiores números de desalojados.

        * **Viés de Notificação:** Municípios com maior capacidade adaptativa possuem, por definição, sistemas de Defesa Civil mais estruturados e eficientes no registro de dados. O maior número de desalojados registrado reflete, em parte, uma cobertura de monitoramento mais eficaz, enquanto municípios com baixa capacidade podem sofrer de subnotificação severa.
        
        * **Densidade vs. Vulnerabilidade:** Não podemos confundir capacidade institucional com ausência de risco. Grandes centros urbanos, mesmo com indicadores adaptativos elevados, possuem densidade populacional e ocupação de encostas muito mais complexas. O índice de adaptabilidade mede a estrutura de resposta, não a eliminação do risco geológico pré-existente.
        
        * **Conclusão:** O dado revela que a capacidade adaptativa não atua de forma isolada. O alto número de desalojados em cidades "preparadas" indica que a infraestrutura, embora existente, muitas vezes ainda é insuficiente frente à magnitude dos eventos climáticos nessas zonas de alta densidade. 
        
        **O GeoRisk revela que o investimento em capacidade adaptativa precisa ser acompanhado de uma revisão profunda do planejamento urbano e não apenas da estrutura de resposta à crise.**
        """)
# Heatmap de Ocorrências
with aba4:
    st.subheader("Mapa de Calor (Heatmap) de Ocorrências Anuais")
    st.write("Identifique os 'pontos quentes' ao longo do tempo. Cores mais claras indicam anos e municípios com maior intensidade de desastres.")

    df_heatmap = filtered_df.pivot_table(
        index='municipio',
        columns='ano',
        values='ocorrencias_deslizamento',
        aggfunc='sum',
        fill_value=0
    )

    if not df_heatmap.empty:
        fig_heat = px.imshow(
            df_heatmap,
            labels=dict(x="Ano", y="Município", color="Ocorrências"),
            x=df_heatmap.columns,
            y=df_heatmap.index,
            color_continuous_scale="Viridis",
            aspect="auto",
            title="Intensidade de Deslizamentos por Município e Ano"
        )

        fig_heat.update_xaxes(side="top")
        fig_heat.update_layout(template="plotly_dark", margin=dict(l=150))

        st.plotly_chart(fig_heat, use_container_width=True)
    else:
        st.info("Não há dados de ocorrências para os filtros selecionados.")
    with st.expander("🔍 Análise Técnica: Geografia do Risco (Mapa de Calor)"):
        st.markdown("""
        O mapa de calor evidencia a distribuição temporal e geográfica das ocorrências de deslizamento no estado do Rio de Janeiro entre 2014 e 2024. A leitura dos dados permite identificar padrões de vulnerabilidade persistente:

        * **Polarização do Risco:** É possível observar uma disparidade clara: municípios como Teresópolis, Petrópolis e Nova Friburgo exibem uma coloração consistentemente mais intensa (tons claros/amarelos) ao longo de quase toda a série temporal. Isso confirma que a vulnerabilidade nessas áreas é estrutural e não apenas um evento climático isolado.
        
        * **Perfis de Vulnerabilidade Distintos:** Enquanto a Região Serrana apresenta "pontos quentes" persistentes, municípios como Rio de Janeiro e Nova Iguaçu mostram uma intensidade menor no registro de ocorrências. Isso não significa ausência de risco, mas que a natureza do desastre nesses locais possui um perfil geológico e de ocupação urbana distinto.
        
        * **Independência Climática Local:** O dado mostra que anos críticos para um município não são necessariamente críticos para outro. Por exemplo, um ano de alta intensidade na Região Serrana pode não refletir o mesmo cenário em municípios de baixada. Isso valida a necessidade de políticas públicas de gestão de risco que sejam descentralizadas e locais, em vez de medidas estaduais generalistas.
        
        **Conclusão da análise:** O heatmap deixa claro que a "geografia do medo" no Rio de Janeiro tem nome e sobrenome (Região Serrana). O GeoRisk utiliza esse padrão histórico para demonstrar que o risco não é distribuído de forma aleatória: ele é concentrado, crônico e previsível com base no histórico de cada localidade.
        """)
# Predição ( Decision tree )
with aba5:
    st.subheader("Simulador Preditivo de Risco")
    st.write(
        "Ajuste as condições climáticas e geográficas para prever o nível de alerta.")

    col_ia1, col_ia2, col_ia3 = st.columns(3)

    with col_ia1:
        cidade = st.selectbox("Selecione o Município:", lista_cidades_ia)

    with col_ia2:
        chuva = st.number_input(
            "Previsão de Chuva (mm):", min_value=0.0, max_value=300.0, value=50.0)

    with col_ia3:
        solo = st.number_input(
            "Índice de Saturação do Solo (0.0 a 1.0):", min_value=0.0, max_value=1.0, value=0.5)

    if st.button("🔮 Prever Nível de Risco"):
        id_cidade = lista_cidades_ia.index(cidade)

        nome_regiao = dic_cidade_regiao_ia[cidade]
        id_regiao = mapa_regioes_ia[nome_regiao]

        X_novo = [[chuva, solo, id_cidade, id_regiao]]

        previsao = modelo_ia.predict(X_novo)[0]

        st.markdown("<br>", unsafe_allow_html=True)
        if previsao in ["Baixo", "Médio"]:
            st.success(
                f"✅ Nível de Risco Previsto para {cidade} ({nome_regiao}): **{previsao}**")
        elif previsao in ["Alto", "Crítico"]:
            st.warning(
                f"⚠️ Nível de Risco Previsto para {cidade} ({nome_regiao}): **{previsao}**")
        else:
            st.error(
                f"🚨 Nível de Risco Previsto para {cidade} ({nome_regiao}): **{previsao}**")
    with st.expander("🔍 Como a Inteligência Artificial toma essa decisão?"):
        st.markdown("""
            Este simulador utiliza um modelo de Machine Learning chamado **Árvore de Decisão**. A escolha desse modelo foi feita porque ele permite entender de forma clara quais fatores influenciam a classificação do risco, tornando o processo mais transparente.

            A decisão do modelo é baseada principalmente em três informações:

            * **Volume de chuva:** A partir dos dados históricos, o modelo identifica faixas de precipitação que costumam estar associadas a diferentes níveis de risco. Quanto maior o volume de chuva, maior tende a ser a probabilidade de ocorrência de deslizamentos.

            * **Saturação do solo:** O risco não depende apenas da chuva do momento. O modelo também considera o quanto o solo já está encharcado. Uma mesma quantidade de chuva pode gerar impactos diferentes dependendo das condições do terreno.

            * **Características da região:** Cada município possui características geográficas próprias. Por isso, o sistema considera a região à qual a cidade pertence, permitindo que a análise seja mais adequada às condições locais.

            **Na prática:** o modelo compara os valores informados com padrões identificados nos dados históricos e, com base nesses critérios, classifica o nível de risco apresentado na simulação.
        """)
