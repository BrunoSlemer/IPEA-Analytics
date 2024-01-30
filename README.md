# Análise de dados sobre o Petroleo do tipo Brent

## Fonte dos dados [IPEA](http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view)

### MVP do modelo no [streamlit](https://ipea-analytics-fiap-1dtat.streamlit.app/?embed_options=dark_theme)

#### [Github](https://github.com/BrunoSlemer/IPEA-Analytics)

A raspagem dos dados foi feita manualmente a cada 7 dias utilizando o beutifulsoup, está incluso no Script_Scraping.

O dataframe estatistiscas_por_ano foi derivado do ipea.csv e foi utilizado para aperfeiçoar a análise.

O arquivo requirements.txt foi adicionado como requisito para instalar as bibliotecas utilizadas no projeto.

O Analise_IPEA.ipynb foi o notebook utilizado para a realização do EDA e dos testes com o modelo.

Obs: o modelo foi gerado com picle. Obtivemos sucesso com o modelo no notebook, porém na hora de utiliza-lo no streamlit não funcionou.

Integrantes

Bianca Cerqueira | RM 348764

Bruno Slemer | RM 349451

Pedro Garcia | RM 349104
