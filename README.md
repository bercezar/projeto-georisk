# 📊 GeoRisk: Painel Analítico de Riscos Geológicos

Este projeto foi desenvolvido para a disciplina de **Linguagens de Programação**, sob a orientação do professor **Alexandre Neves Louzada**. O GeoRisk é uma solução focada em **Análise de Dados, Estatística Computacional e Desenvolvimento em Python**, dedicada à modelagem e mitigação de riscos de deslizamentos no estado do Rio de Janeiro.

---

### 🎯 Sobre o Projeto
O GeoRisk cruza dados históricos de ocorrências com indicadores de capacidade adaptativa para gerar insights preditivos. A base de dados utilizada provém da [AdaptaBrasil (INPE)](https://data.inpe.br/geonetwork/srv/api/records/adaptabrasil60005), garantindo rigor técnico e científico à análise.

---

### 🛠️ Stack Tecnológica
Abaixo estão as tecnologias fundamentais utilizadas no desenvolvimento do sistema:

- **Streamlit:** Framework de Front-end para renderização de aplicações Web dinâmicas (SPA).
- **Python & Pandas:** Motor principal de processamento lógico e agregação matemática de dados em tempo de execução.
- **Scikit-Learn:** Biblioteca de Machine Learning utilizada para treinamento e execução do modelo de Árvore de Decisão responsável pela classificação preditiva dos níveis de risco.
- **SQLite & SQLAlchemy:** Banco de dados relacional e ORM para abstração e segurança nas integrações lógicas.
- **HTML5 & CSS3:** Customização padrão para aprimorar a interface de usuário e a legibilidade dos dados apresentados.
- **Plotly Express:** Biblioteca de DataViz para renderização de gráficos e mapeamento geográfico interativo.

---

### ✨ Funcionalidades Principais

- [x] Integração e cruzamento de bases de dados distintas
- [x] Modelagem relacional com SQLAlchemy e SQLite
- [x] KPIs dinâmicos e indicadores de impacto
- [x] Dashboards organizados em múltiplas seções
- [x] Aplicação web interativa com Streamlit
- [x] Análise exploratória e visualização de dados
- [x] Aplicação de modelo de árvore de decisão
- [x] Modelo preditivo de Machine Learning para classificação de risco
- [x] Simulador interativo de cenários baseado em Árvore de Decisão

---

### 🏗️ Arquitetura do Sistema
graph TD
    A[Base de Dados AdaptaBrasil / INPE] --> B[(SQLite DB)]
    B --> C[SQLAlchemy / ORM]
    C --> D[Pandas / Processamento]
    D --> E[Scikit-Learn: Árvore de Decisão]
    D --> F[Streamlit Dashboard]
    E -->|Previsão de Risco| F
    F --> G(Usuário Final)

    style B fill:#1e293b,stroke:#00d4ff
    style F fill:#0f172a,stroke:#00d4ff,stroke-width:2px
    style E fill:#0f172a,stroke:#00d4ff

O pipeline de dados assegura a integridade desde o armazenamento bruto até à inferência do modelo. A lógica foi encapsulada para garantir performance e escalabilidade, seguindo boas práticas de desenvolvimento Python.

---

### 📈 Gráficos do .ipynb
* **Correlação entre Capacidade Adaptativa e Impacto:**
  ![Análise de Adaptabilidade e Impacto](images/adaptativa_deslizamento.png)
* **Estrutura do Modelo Preditivo (Árvore de Decisão):**
  ![Estrutura da IA](images/arvore_de_decisao.png)
* **Ranking de Mortalidade por Município:**
  ![Mortalidade](images/obito_municipio.png)
* **Impacto da Precipitação na Frequência de Ocorrências:**
  ![Impacto da Precipitação](images/ocorrencia_por_preciptacao.png)

--
