# DataGuard — Sprint 4 Final

Enterprise Challenge FIAP + Locaweb 2026.

## Escopo final

O núcleo de Data Science validado na Sprint 3 foi congelado. A Sprint 4 adiciona somente uma
camada mínima de aderência ao desafio, sem reconstruir Forecast ou OLA Risk:

1. previsão D+1/D+7 explicitada para **P2 e P3**;
2. leitura das **faixas oficiais de KPI** sobre os valores observados de 2025;
3. recomendações operacionais baseadas em regras explicáveis.

## Aplicação

Páginas:
- Overview
- Predict
- OLA Risk
- Patterns
- KPI & Action

## Forecast congelado

- 6 abordagens comparadas
- método selecionado: Média Móvel de 7 dias
- MAE: 131,69
- MAPE: 14,18%
- D+1 total: 859
- D+7 total: 6.013

A previsão por prioridade usa a mesma lógica de média dos 7 últimos dias do regime recente:

- P2 D+1: 36
- P2 D+7: 254
- P3 D+1: 435
- P3 D+7: 3,047

## OLA Risk congelado

- população elegível: 25.600
- violações: 248
- modelo selecionado: Logistic Regression + Produto/Categoria
- ROC-AUC: 0,790
- PR-AUC: 0,083
- threshold: 0,926
- Precision: 20,8%
- Recall: 22,0%
- F1: 21,4%

O Risk Score é priorização relativa, não probabilidade calibrada.

## KPI 2025

Os percentuais representam as faixas oficiais de atingimento aplicadas ao histórico observado.
Eles não são probabilidades de ocorrência.

| Indicador                   | Prioridade   |   Valor_2025 | Faixa_oficial   |   Atingimento_% |
|:----------------------------|:-------------|-------------:|:----------------|----------------:|
| Volume de incidentes no KPI | P2           |         5159 | 4585 a 5388     |             125 |
| OLA quebrado                | P2           |           42 | 40 a 45         |              75 |
| Volume de incidentes no KPI | P3           |        19997 | 19489 a 22116   |             125 |
| OLA quebrado                | P3           |          196 | < 201           |             150 |

## Estrutura

```text
DataGuard_Tecnico_Sprint4_FINAL/
├── app.py
├── requirements.txt
├── requirements_notebook.txt
├── README.md
├── .gitignore
├── notebooks/
│   └── 01_DataGuard_Auditoria_EDA.ipynb
├── scripts/
│   └── 02_build_sprint4_outputs.py
└── outputs/
    ├── grupos.csv
    ├── historico_diario.csv
    ├── kpi_2025.csv
    ├── metricas_forecast.csv
    ├── metricas_ola.csv
    ├── patterns_ic.csv
    ├── previsao_d7.csv
    ├── previsao_prioridades_d7.csv
    ├── ranking_ola.csv
    └── recomendacoes_operacionais.csv
```

## Executar o app

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Reproduzir a camada Sprint 4

```bash
python scripts/02_build_sprint4_outputs.py --dataset /caminho/LW-DATASET.xlsx --outputs outputs
```

O notebook original da Sprint 3 permanece intacto em `notebooks/`.

## Limitações declaradas

- Forecast validado em janela temporal curta.
- OLA Risk validado com split estratificado aleatório; validação out-of-time é evolução futura.
- Risk Score não é probabilidade calibrada.
- O dataset não permite inferir capacidade ou headcount a partir de concentração de volume.
- A camada KPI exibe atingimento histórico de 2025; não inventa uma “probabilidade de atingimento”
  sem modelo probabilístico calibrado.
