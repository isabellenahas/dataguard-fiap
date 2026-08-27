
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="DataGuard",
    page_icon="🛡️",
    layout="wide"
)

# =========================
# ESTILO
# =========================

st.markdown("""
<style>

.block-container {
    padding-top: 1.5rem;
}

[data-testid="stMetric"] {
    background-color: rgba(120,120,120,0.08);
    border: 1px solid rgba(120,120,120,0.18);
    padding: 16px;
    border-radius: 12px;
}

h1 {
    font-weight: 700;
}

.small-text {
    opacity: 0.70;
    font-size: 0.85rem;
}

</style>
""", unsafe_allow_html=True)


# =========================
# DADOS
# =========================

@st.cache_data
def carregar_dados():

    historico = pd.read_csv(
        "outputs/historico_diario.csv",
        parse_dates=["Data"]
    )

    previsao = pd.read_csv(
        "outputs/previsao_d7.csv",
        parse_dates=["Data"]
    )

    ola = pd.read_csv(
        "outputs/ranking_ola.csv",
        parse_dates=["Aberto"]
    )

    patterns = pd.read_csv(
        "outputs/patterns_ic.csv"
    )

    grupos = pd.read_csv(
        "outputs/grupos.csv"
    )

    metricas_forecast = pd.read_csv(
        "outputs/metricas_forecast.csv"
    )

    metricas_ola = pd.read_csv(
        "outputs/metricas_ola.csv"
    )

    return (
        historico,
        previsao,
        ola,
        patterns,
        grupos,
        metricas_forecast,
        metricas_ola
    )


(
    historico,
    previsao,
    ola,
    patterns,
    grupos,
    metricas_forecast,
    metricas_ola
) = carregar_dados()


# =========================
# SIDEBAR
# =========================

st.sidebar.title("DATAGUARD")

st.sidebar.caption(
    "AIOps Predictive Operations"
)

pagina = st.sidebar.radio(
    "Navegação",
    [
        "Overview",
        "Predict",
        "OLA Risk",
        "Patterns"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Enterprise Challenge FIAP + Locaweb 2026"
)


# =========================
# OVERVIEW
# =========================

if pagina == "Overview":

    st.title("DataGuard")

    st.caption(
        "Plataforma Preditiva de Operações de TI"
    )

    d1 = int(
        previsao.iloc[0]["Previsao_Incidentes"]
    )

    d7 = int(
        previsao["Previsao_Incidentes"].sum()
    )

    criticos = ola[
        ola["Faixa_Risco"] == "CRÍTICO"
    ].shape[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Previsão D+1",
        f"{d1:,}",
        help="Estimativa de incidentes para o próximo dia."
    )

    col2.metric(
        "Previsão D+7",
        f"{d7:,}",
        help="Volume acumulado projetado para os próximos 7 dias."
    )

    col3.metric(
    "Registros em faixa crítica",
    f"{criticos:,}",
    help="Registros históricos classificados acima do threshold crítico do OLA Risk Score."
)

    col4.metric(
        "Registros analisados",
        "122.543"
    )

    st.subheader(
        "Operação: histórico e projeção"
    )

    hist = historico.tail(14)[
        ["Data", "Volume_Total"]
    ].copy()

    hist["Tipo"] = "Real"

    hist = hist.rename(
        columns={"Volume_Total": "Incidentes"}
    )

    prev = previsao.copy()

    prev["Tipo"] = "Previsão"

    prev = prev.rename(
        columns={
            "Previsao_Incidentes": "Incidentes"
        }
    )

    plot = pd.concat(
        [hist, prev],
        ignore_index=True
    )

    fig = px.line(
        plot,
        x="Data",
        y="Incidentes",
        color="Tipo",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "O regime recente apresentou mudança estrutural "
        "a partir de setembro de 2025. "
        "A modelagem prioriza o comportamento operacional recente."
    )


# =========================
# PREDICT
# =========================

elif pagina == "Predict":

    st.title("Predict")

    st.caption(
        "Antecipação de volume operacional"
    )

    d1 = int(
        previsao.iloc[0]["Previsao_Incidentes"]
    )

    d7 = int(
        previsao["Previsao_Incidentes"].sum()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "D+1",
        f"{d1:,} incidentes"
    )

    col2.metric(
        "D+7",
        f"{d7:,} incidentes"
    )

    col3.metric(
        "MAPE validado",
        "14,18%"
    )

    st.subheader(
        "Projeção da próxima semana"
    )

    st.subheader(
        "Comparação de modelos"
    )
    
hist_predict = historico.tail(14)[
    ["Data", "Volume_Total"]
].copy()

hist_predict["Tipo"] = "Histórico"

hist_predict = hist_predict.rename(
    columns={
        "Volume_Total": "Incidentes"
    }
)

prev_predict = previsao.copy()

prev_predict["Tipo"] = "Previsão"

prev_predict = prev_predict.rename(
    columns={
        "Previsao_Incidentes": "Incidentes"
    }
)

predict_plot = pd.concat(
    [
        hist_predict,
        prev_predict
    ],
    ignore_index=True
)

fig = px.line(
    predict_plot,
    x="Data",
    y="Incidentes",
    color="Tipo",
    markers=True,
    title="Histórico recente e projeção D+7"
)

fig.update_layout(
    xaxis_title="Data",
    yaxis_title="Incidentes",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

    st.dataframe(
        metricas_forecast,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "A Média Móvel de 7 dias foi mantida porque "
        "superou Ridge, Random Forest, Prophet e baseline D-7 "
        "no MAE do período de validação."
    )


# =========================
# OLA RISK
# =========================

elif pagina == "OLA Risk":

    st.title("OLA Risk")

    st.caption(
        "Priorização de incidentes com maior risco operacional"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Threshold crítico",
        "92,6"
    )

    col2.metric(
        "Precision no threshold",
        "20,8%"
    )

    col3.metric(
        "Recall no threshold",
        "22,0%"
    )

    st.warning(
        "Risk Score é utilizado para priorização relativa. "
        "Não deve ser interpretado como probabilidade calibrada."
    )

    prioridade = st.multiselect(
        "Prioridade",
        sorted(
            ola["Prioridade"]
            .dropna()
            .unique()
        )
    )

    faixa = st.multiselect(
        "Faixa de risco",
        [
            "CRÍTICO",
            "ALTO",
            "ATENÇÃO",
            "BAIXO"
        ],
        default=[
            "CRÍTICO",
            "ALTO"
        ]
    )

    tabela_ola = ola.copy()

    if prioridade:
        tabela_ola = tabela_ola[
            tabela_ola["Prioridade"].isin(
                prioridade
            )
        ]

    if faixa:
        tabela_ola = tabela_ola[
            tabela_ola["Faixa_Risco"].isin(
                faixa
            )
        ]

    st.dataframe(
        tabela_ola[
            [
                "Número",
                "Prioridade",
                "Produto",
                "Categoria",
                "Grupo designado",
                "Aberto por",
                "Risk_Score",
                "Faixa_Risco"
            ]
        ].head(100),
        use_container_width=True,
        hide_index=True
    )
    st.subheader(
        "Comparação inicial dos modelos"
    )

    st.dataframe(
        metricas_ola,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "A comparação acima representa a etapa inicial de seleção dos modelos. "
        "Após a escolha da Logistic Regression com Produto e Categoria, "
        "o threshold operacional foi ajustado para 92,6. "
        "Nesse ponto de corte, o modelo alcançou Precision de 20,8% "
        "e Recall de 22,0%, priorizando uma quantidade menor de registros "
        "para investigação operacional."
    )
 
# =========================
# PATTERNS
# =========================

elif pagina == "Patterns":

    st.title("Patterns")

    st.caption(
        "Recorrência e concentração operacional"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Principal equipe",
        "Team14"
    )

    col2.metric(
        "Concentração Team14",
        "87,47%"
    )

    col3.metric(
        "IC mais recorrente",
        "IC00014"
    )

    st.subheader(
        "Principais itens de configuração"
    )

    patterns_top = patterns.head(15)

    fig = px.bar(
        patterns_top,
        x="Incidentes",
        y="Item de configuração",
        orientation="h"
    )

    fig.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "Concentração por equipe"
    )

    st.dataframe(
        grupos,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Hipótese investigada: P4/P5 e eventos de monitoramento "
        "como precursores de P2/P3. "
        "No teste de janela de 24h, o sinal simples não apresentou "
        "capacidade discriminativa e não foi incorporado ao mecanismo "
        "preditivo do MVP."
    )
