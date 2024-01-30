import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
import seaborn as sns
import pandas as pd
import pickle

st.set_page_config(layout="wide")

#Carremento da base de dados IPEA
dados = pd.read_csv('https://raw.githubusercontent.com/BrunoSlemer/IPEA-Analytics/main/ipea.csv')
dados['Data'] = pd.to_datetime(dados['Data'], dayfirst= True)

#Carremento da bases de dados resumo estatistico do IPEA
dados_Stats = pd.read_csv('https://raw.githubusercontent.com/BrunoSlemer/IPEA-Analytics/main/estatisticas_por_ano.csv')


tab1, tab2, tab3 = st.tabs(['📜Storytelling','📈Dashboard','💾Modelo'])

with tab2:
    st.title("Análise de dados  Mercado de Petróleo Brent - IPEA")
    st.write('#### O estudo atual tem como objetivo analisar os dados da IPEADATA com o preço por barril do petróleo bruto tipo Brent. \n Período da análise: Janeiro 1987 até Janeiro 2024.')

    st.write('a principal fonte de dados que estamos utilizando para esse projeto é a disponibilizada pela IPEA')
    st.write('fonte: http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view')
    show_table = st.checkbox('Mostrar Tabela')

    if show_table:
        st.dataframe(dados.set_index('Data'))


    #Gráfico de Série Temporal completo
    with st.container():
        st.title('Gráfico de Série Temporal')

        dados['Anos'] = dados['Data'].dt.year
        # dados default
        data_inicial_padrao = dados['Data'].min()
        data_final_padrao = dados['Data'].max()
        ano_inicial_padrao = dados['Anos'].min()
        ano_final_padrao = dados['Anos'].max()
        


        data_inicial, data_final = st.date_input('Selecione o intervalo de datas', [dados['Data'].min(), dados['Data'].max()])
        ano_inicial, ano_final = st.slider('Selecione o intervalo de anos', min_value= dados['Anos'].min(), max_value= dados['Anos'].max(), value=(dados['Anos'].min(), dados['Anos'].max()))
        col1, col2, col3, col4, col5, col6,col7,col8, col9 = st.columns(9)
        with col1:
            if st.button("Limpar filtros"):
                data_inicial = data_inicial_padrao
                data_final = data_final_padrao
                ano_inicial = ano_inicial_padrao
                ano_final = ano_final_padrao
        
        with col2:
            if st.button("Reaplicar filtros"):
                pass

        dados_filtrados = dados[(dados['Data'].dt.date >= data_inicial) & (dados['Data'].dt.date <= data_final) & (dados['Anos'] >= ano_inicial) & (dados['Anos'] <= ano_final)]

        st.write(dados_filtrados['Data'].min(), dados_filtrados['Data'].max())
        dados_filtrados = dados_filtrados.sort_values(by= 'Data', ascending= True)
        st.line_chart(dados_filtrados, x= 'Data',y='Preço - petróleo bruto - Brent (FOB)')

    st.divider()

    melhores_dias = dados.sort_values('Preço - petróleo bruto - Brent (FOB)',ascending=True).head(10)
    piores_dias = dados.sort_values('Preço - petróleo bruto - Brent (FOB)',ascending=False).head(10)

    col1, col2 = st.columns(2)
    with col1:
        st.write('Piores Anos Historicos')
        st.table(melhores_dias.set_index('Data'))
        st.write('É possivel ver que tanto a alta historica quanto a baixa ocorrem em períodos especificos mostrando pouca flutuação de preço. Também é possível notar que em 21/04/2021 foi registrado a segunda pior baixa histórica.')

    with col2:
        st.write('Melhores Anos Historicos')
        st.table(piores_dias.set_index('Data'))

    st.divider()
    #Principais Fatores que Influenciam o Preço do Petróleo Brent
    with st.container(border = True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Oferta e Demanda')
            st.write('A dinâmica fundamental de oferta e demanda desempenha um papel crucial nos preços do petróleo Brent. Se a demanda global supera a oferta, os preços tendem a subir, e vice-versa. A produção global, particularmente em países que contribuem significativamente para o mercado Brent, influencia diretamente essas condições.')
        with col2:
            st.header('Produção da OPEP')
            st.write('A Organização dos Países Exportadores de Petróleo (OPEP), que inclui grandes produtores de petróleo como Arábia Saudita, Iraque e Irã, tem um impacto direto nos preços do Brent. Decisões da OPEP sobre limites de produção e quotas de exportação afetam a oferta global.')
        with col3:
            st.header('Condições Geopolíticas')
            st.write('Tensões geopolíticas em regiões produtoras de petróleo podem levar a interrupções na produção e exportação, impactando os preços do Brent. Eventos como conflitos no Oriente Médio, problemas de segurança em regiões produtoras e sanções internacionais podem criar volatilidade nos preços.')

    st.divider()

    # linha do tempo
    st.write('### Linha do tempo dos eventos de maior impacto nos valores do Petroleo Brent')
    events = [
        {'Ano': '2007', 'Acontecimento': 'A adesão de Angola à OPEP e o aumento da demanda em países como China e Índia, que registraram um forte avanço econômico, contribuíram para que os preços do petróleo atingissem máximos históricos.'},
        {'Ano': '2008', 'Acontecimento': 'O mercado do petróleo viveu um drama em dois atos, marcado pela superação da barreira dos 100 dólares o barril e uma disparada meteórica dos preços até 147,50 dólares, antes de uma queda de uma brutalidade sem precedente. Tensões geopolíticas, do Irã à Nigéria passando pelo Paquistão, o equilíbrio tenso entre uma oferta limitada e uma demanda puxada pelos países emergentes, a conscientização de que as reservas são limitadas e de acesso cada vez mais difícil, e uma febre dos fundos de investimento por matérias-primas foram alguns dos fatores que levaram os preços às alturas.'},
        {'Ano': '2009', 'Acontecimento': 'A cotação do petróleo no mercado internacional caiu desde julho de 2008, quando atingiu o ápice de US$ 147. Seis meses depois, o barril já estava mais de US$ 100 mais barato. Preocupada com isso, a OPEP anunciou um corte recorde na produção, de 2,2 milhões de barris, que passou a vigorar em janeiro de 2009.'},
        {'Ano': '2014', 'Acontecimento': 'O preço do petróleo tipo Brent, que serve de referência no mercado europeu, caiu para 67,92 dólares, menor valor em cinco anos. A tendência reflete a reação do mercado à decisão da OPEP, tomada em novembro de 2014, de manter os atuais níveis de produção, em torno de 30 milhões de barris por dia.'},
        {'Ano': '2020', 'Acontecimento': 'A pandemia de COVID-19 prejudicou o consumo mundial de petróleo, fazendo com que os preços caíssem mais de 20% no ano. Em abril, os preços do petróleo Brent recuaram para menos de US$ 20/b.'},
        {'Ano': '2022', 'Acontecimento': 'O preço do barril de Brent ultrapassou os 90 dólares pela primeira vez desde outubro de 2014, impulsionado pelas tensões na Ucrânia e no Oriente Médio que ameaçam a oferta em um mercado já nervoso9. No entanto, os preços terminaram o ano bem longe dos mais de US$ 120 por barril registrados durante o pico da crise da guerra da Ucrânia.'}
    ]

    st.table(events)
    st.write('A escolha dos eventos foi determinada no desvio padrão ocorrido na serie temporal ao longo do ano de ocorrencia do evento')

    st.divider()

    st.write('### Maiores Produtores e Consumidores')
    st.write('Os produtores de petróleo desempenham um papel central no cenário global de energia. Países como Rússia, Estados Unidos, Arábia Saudita e membros da OPEP (Organização dos Países Exportadores de Petróleo) são alguns dos principais protagonistas na produção mundial de petróleo.')
    st.write(' \n Essas nações possuem vastas reservas e uma infraestrutura robusta para a extração e exportação desse recurso estratégico. Suas decisões sobre a produção e as políticas energéticas têm impactos diretos nos preços do petróleo, na estabilidade geopolítica e na segurança energética global.')
    col1, col2 = st.columns(2)
    with col1: 
        st.dataframe([
            {'Pais': 'Estados Unidos','Produção (milhões de barris por dia)': '16,58'},
            {'Pais': 'Arábia Saudita','Produção (milhões de barris por dia)' : '10,95'},
            {'Pais': 'Rússia','Produção (milhões de barris por dia)' : '10,94'},
            {'Pais': 'Canadá','Produção (milhões de barris por dia)': '5,42'},
            {'Pais': 'Iraque','Produção (milhões de barris por dia)' : '4,10'},
            {'Pais': 'China','Produção (milhões de barris por dia)'  : '3,99'},
            {'Pais': 'Emirados Árabes Unidos','Produção (milhões de barris por dia)': '3,66'},
            {'Pais': 'Irã','Produção (milhões de barris por dia)': '3,62'},
            {'Pais': 'Brasil','Produção (milhões de barris por dia)': '2,98'},
            {'Pais': 'Kwait','Produção (milhões de barris por dia)':'2,74'}
            ])
        

    st.title('COVID-19 e os impactos sobre o mercado de petróleo')
    st.write('A disseminação da COVID-19 em 2020, emerge como um dos principais impactos nas economias globais. Além de ser o segundo maior mercado consumidor de petróleo no mundo, também foi o ponto inicial da doença, a China experimentou o impacto mais significativo inicialmente. De acordo com a Agência Internacional de Energia (IEA, na sigla em inglês), a demanda chinesa por petróleo foi estimada em 1,8 milhão de barris por dia abaixo dos níveis de 2019 durante o primeiro quadrimestre de 2020.')
    st.markdown('- Restrições às linhas de produção (Estagnação de 1/3 da demanda industrial por GNL)')
    st.markdown('- Queda de 32% nas chamadas portuárias')
    st.markdown('- Redução no número de viagens/passageiros')
    st.markdown('- Diminuição no número de fretes')
    st.markdown('- Cancelamento de mais de 200 mil voos')
    st.markdown('Fonte: BCG, 2020 – “COVID-19: Oil and Gas Market impacts')
    st.divider()

    with st.container(border=True):
        st.header('Conclusão')
        st.write('O mercado mundial de petróleo é fundamental para a economia global, impactando diversos setores. A demanda por petróleo é impulsionada principalmente pelo transporte e indústrias. Grandes produtores, como Rússia, Estados Unidos e membros da OPEP, exercem influência significativa na oferta global. Os preços do petróleo são altamente voláteis, influenciados por eventos geopolíticos, mudanças na demanda e decisões da OPEP. ')
        st.write('A transição energética e avanços tecnológicos estão moldando a evolução do mercado. A pandemia de COVID-19 teve um impacto expressivo em 2020, reduzindo drasticamente a demanda. A diversificação de fontes de energia, preocupações ambientais e conflitos geopolíticos são fatores adicionais que afetam o mercado global de petróleo, além disso, é necessário reconhecer que o cenário do mercado de petróleo é dinâmico e está sujeito a mudanças rápidas.')
        st.divider()
        st.subheader('Principais Insights:')
        st.write('1- Apesar da baixa no preço em 2020 atingindo a segunda colocação de baixa historica, a variação acumulada anual, não foi negativa em nenhum dos anos subsequentes oque coloca o comodite como um ativo com tendencia acendente')
        st.write('2- Recurso Finito, O petróleo por ser um recurso esgotável e o mesmo enfrenta aumento de valor devido à crescente demanda e limitação de suas reservas. Essa escassez potencial impulsiona a busca por alternativas sustentáveis, contribuindo para a valorização do petróleo. A conscientização sobre sua finitude também promove a transição para fontes de energia renovável, moldando o futuro do mercado energético global.')
        st.write('3- O mercado de petróleo mostrou pontos de volatidade acentuados mas devido à flexibilidade na adaptação da oferta, respostas a estímulos econômicos, resiliência geopolítica, variações na demanda e expectativas do mercado. A capacidade de ajuste dos produtores, intervenções econômicas e mudanças nas condições geopolíticas contribuem para uma rápida recuperação dos preços, embora a velocidade possa variar dependendo das circunstâncias específicas, essa afirmação pode ser vista nos graficos de "Retorno e Variação Acumulados".')
        st.write('4- Impactos da pandemia sobre o mercado A pandemia de COVID-19 teve impactos expressivos no setor de petróleo global. O declínio acentuado na demanda devido a lockdowns resultou em uma oferta excessiva e quedas significativas nos preços do petróleo. Empresas tiveram que reduzir produção, especialmente no setor de transporte. Economias dependentes da exportação de petróleo enfrentaram desafios financeiros, levando a uma reavaliação de estratégias econômicas. A crise acelerou discussões sobre diversificação de fontes de energia e transição para práticas mais sustentáveis.')
        st.divider()
        st.write('Para investidores no mercado de petróleo, é crucial reconhecer a dinâmica única desse setor. Embora seja caracterizado por volatilidade e incerteza, o petróleo continua a ser um ativo estratégico global. A rápida recuperação após quedas e a resiliência diante de desafios são características notáveis.')
        st.write('No entanto, é necessário estar ciente dos riscos, incluindo fatores geopolíticos, mudanças nas condições econômicas e transições para fontes de energia mais sustentáveis. A compreensão da interconexão entre eventos globais, políticas energéticas e flutuações nos preços é fundamental para tomar decisões informadas. Em um cenário onde a transição para energias renováveis ganha destaque, os investidores devem monitorar de perto as tendências e considerar estratégias adaptáveis para enfrentar os desafios em constante evolução do mercado de petróleo.')

    with st.container(border=True):
        st.write('## Integrantes')
        st.write('Bianca Cerqueira | RM 348764')
        st.write('Bruno Slemer | RM 349451')
        st.write('Pedro Garcia | RM 349104')

with tab1:
    #CONFIGURACAO DA PAGINA

    #TITULO
    st.title("Mercado de Petróleo Brent - IPEA")
    #BASE
    dados = pd.read_csv('https://raw.githubusercontent.com/BrunoSlemer/IPEA-Analytics/main/ipea.csv')
    estatistica = pd.read_csv('https://raw.githubusercontent.com/BrunoSlemer/IPEA-Analytics/main/estatisticas_por_ano.csv')
    estatistica.set_index("Ano", inplace=True)
    est = pd.read_csv('https://raw.githubusercontent.com/BrunoSlemer/IPEA-Analytics/main/estatisticas_por_ano.csv')
    #dados = dados.iloc[:, 1:]

    #BIG NUMBERS
    st.divider()
    # Row A
    st.markdown('### Big Numbers')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Janeiro/2024 | Valor Médio", "80,58", "-1,96%")
    col2.metric("Janeiro/2023 | Valor Médio", "82,54", "-3,96%")
    st.divider()
    col3.metric("Maior Preço - Julho/12", "99,94", "")
    col4.metric("Menor Preço - Dezembro/98", "9,45", "")


    #ajuste de dada para datetime -> pipeline
    #ajustar para que seja dividido por 100 e arendodar os valores 
    dados['Data'] = pd.to_datetime(dados['Data'], dayfirst= True)

    ##SIDE BAR
    img = 'https://github.com/biancacerqueira/Pos/assets/73804788/d6ee59dc-7c41-4b04-a3bb-38c018047956'
    st.sidebar.image(img)
    st.sidebar.header('Filtros')

    #########################################################################

    #Gráfico de Série Temporal completo 
    with st.container(): 
        st.title('Gráfico de Série Temporal')

        if st.sidebar.button("Limpar Filtros"):
            data_inicial, data_final = [dados['Data'].min(), dados['Data'].max()]

        dados['Anos'] = dados['Data'].dt.year
        data_inicial, data_final = st.sidebar.date_input(' Selecione o intervalo de datas', [dados['Data'].min(), dados['Data'].max()])
        ano_inicial, ano_final = st.sidebar.slider(' Selecione o intervalo de anos', min_value= dados['Anos'].min(), max_value= dados['Anos'].max(), value=(dados['Anos'].min(), dados['Anos'].max()))
        dados_filtrados = dados[(dados['Data'].dt.date >= data_inicial) & (dados['Data'].dt.date <= data_final) & (dados['Anos'] >= ano_inicial) & (dados['Anos'] <= ano_final)]

        st.write(dados_filtrados['Data'].min(), dados_filtrados['Data'].max())
        dados_filtrados = dados_filtrados.sort_values(by= 'Data', ascending= True)
        st.line_chart(dados_filtrados, x= 'Data',y='Preço - petróleo bruto - Brent (FOB)')

    
    ####TABELAS - MELHORES E PIORES DIAS ###########
        melhores_dias = dados.sort_values('Preço - petróleo bruto - Brent (FOB)',ascending=True).head(10)
        piores_dias = dados.sort_values('Preço - petróleo bruto - Brent (FOB)',ascending=False).head(10)

        

    st.sidebar.markdown('-----')

    filtro_ano = st.sidebar.multiselect(
        "Selecione os anos",
        options=dados['Anos'].unique(),
        default=dados['Anos'].unique()
    )

    ####GRAFICO DE BARRA MELHORES E PIORES DIAS ######################################################
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.title('Melhores Anos')
        st.bar_chart(melhores_dias, x='Anos', y='Preço - petróleo bruto - Brent (FOB)', color='#093667')

    with col2:
        st.title('Piores Anos')
        st.bar_chart(piores_dias, x='Anos', y='Preço - petróleo bruto - Brent (FOB)', color='#093667')


    st.divider()
    ############################################################


    col1, col2 = st.columns(2)

    with col1:
        st.title('Máxima e Mínimo')
        chart_data = pd.DataFrame(estatistica, columns=["Maximo", "Minimo"])
        st.area_chart(chart_data)

    with col2:
        st.title('Desvio Padrão')
        st.line_chart(est, x='Ano', y='Desvio_Padrao', color='#093667')

    st.divider()


    ###VER DADOS COMPLETOS###############################
    show_table = st.checkbox('Ver dados completos')

    if show_table:
        #limit = st.slider('Limite de linhas da tabela', min_value=10,max_value= len(dados), value=50)
        st.dataframe(dados.set_index('Data'))

    ##########################################################
with tab3:
    st.title('Modelo') 
    st.title('EDA')
    with st.container():
        col1, col2 = st.columns(2)
        with col2:
            st.dataframe(dados_Stats.set_index('Ano'))
        with col1:
            st.write('Para melhorar a janela de observação, resolvemos criar um novo dataframe com os dados acumulados por ano com:')
            st.write('- Valores estatiscos de maxima, minima, media e devio padrão')
            st.write('- Incluimos a "Variação acumulada " para uma anlise em valor de retorno e não nominal')
            st.write('- E incluimos o retorno acumulado ao multiplicar o primeiro valor da base dividir por cada elemente do ano para medir a tendencia dos ganhos')
            st.divider()
            with st.container():
                col1, col2 = st.columns(2)
                with col1:
                    st.write('Criamos um validador binario para contabilizar os anos nos quais a varaição acumulada foi positiva')
                    st.write('A maioria dos anos são positivos mostrando uma tendencia positiva')
                with col2:
                    dados_Stats['positivo'] = np.where(dados_Stats['Variacao'] > 0,1,-1)
                    st.write(dados_Stats['positivo'].value_counts())

    
    st.divider()  
    with st.container():
        st.write('O grafico do retorno acumulado se assemelha a uma curva gausiana inclinda para direita, porem se destaca por apresentar valores de de pico sempre adjacentes aos anos de variação negativa oque implica na capacidade de recuperação de preco do ativo')
        col1, col2 = st.columns(2)
        with col1:  
            st.bar_chart(dados_Stats, x='Ano', y='Retorno_acumulado')
        with col2:
            st.bar_chart(dados_Stats, x='Ano', y='Variacao')
    st.divider() 

    st.title('Escolha do modelo')
    code = '''series = df.drop(['Ano'],axis=1)
scaler = StandardScaler()
rmse_values = []

def train_test_split(data, n_test):
    return data[:-n_test], data[-n_test:]

def model_fit_predict(model, train, test):
    train_dates = (train.index - train.index[0]).days.values.reshape(-1, 1)
    test_dates = (test.index - train.index[0]).days.values.reshape(-1, 1)
    model.fit(train_dates, train.values)
    predictions = model.predict(test_dates)
    return predictions

def measure_rmse(actual, predicted):
    return np.sqrt(mean_squared_error(actual, predicted))

def run():

    scaled_data = scaler.fit_transform(series.values.reshape(-1, 1))

    normalized_series = pd.Series(scaled_data.flatten(), index=series.index)

    train, test = train_test_split(normalized_series, 30)

    models = [ARIMA(train, order=(1,1,0)), LinearRegression(), SVR(), GradientBoostingRegressor(), XGBRegressor()]

    for model in models:
        if type(model) is ARIMA:
            model_fit = model.fit()
            predictions = model_fit.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)
        else:
            predictions = model_fit_predict(model, train, test)

        # Desnormalizar as previsões antes de calcular o RMSE
        predictions_unscaled = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
        test_unscaled = scaler.inverse_transform(test.values.reshape(-1, 1)).flatten()
        rmse = measure_rmse(test_unscaled, predictions_unscaled)
        print(f'RMSE: {rmse} para modelo {type(model).__name__}')
        
      
run()'''
    show_code = st.checkbox('Mostrar código')

    if show_code:
        st.code(code, language='python')
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.text('''
    RMSE: 4.764550447415282 para modelo ARIMA
    RMSE: 15.292711124929017 para modelo LinearRegression
    RMSE: 13.644682477086244 para modelo SVR
    RMSE: 2.9458729360723788 para modelo GradientBoostingRegressor
    RMSE: 7.4122855792082785 para modelo XGBRegressor''')
            st.write('##### objetivando o encontro do valor mais proximo de zero, o modelo mais bem adaptado e MVP escolido foi GradientBoostingRegressor')
            
        with col2:
            rmse_values = {"ARIMA": 4.522449990221025,"LinearRegression": 15.292711124929017,"SVR": 13.644682477086244,"GradientBoostingRegressor": 2.2283690885269256,"XGBRegressor": 7.4122855792082785}
            st.bar_chart(rmse_values)
    st.divider()

    with st.container():
        st.title('MVP - GradientBoostingRegressor')
        st.write('''Para otimizar o modelo focamos no hiper parametro "max_depth" e no número de "lag", para isso  
                 realizamos é o treinamento com todos as combinações alterando esses fatores de 1 a 9''')
        st.write('Apesar da perda de performace, "max_depth" mais elevando incaram maiores ganhos, sendo que a combinação')
        st.write('Melhor resultado foi: Lag: 9, Max Depth: 9, Mean Squared Error: 0.25208818617238826, Rmse: 0.5020838437675408')
    
        code_model = '''def create_features_target(data, lag=1):

    X = []
    y = []
    for i in range(len(data) - lag):
        X.append(data[i:i+lag])
        y.append(data[i+lag])
    return np.array(X), np.array(y)

def train_gb_regressor(X_train, y_train, n_estimators=100, max_depth=3, learning_rate=0.1):

    gb_model = GradientBoostingRegressor(n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate)
    gb_model.fit(X_train, y_train)
    return gb_model

lag_range = range(1, 10)
max_depth_range = range(1, 10)
n_estimators = 100
learning_rate = 0.1
prediction_days = 30

best_model = None
best_mse = float('inf')

for lag in lag_range:

    X, y = create_features_target(df_gb['Preço - petróleo bruto - Brent (FOB)'], lag=lag)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=55)
    for max_depth in max_depth_range:

        X_train_lag, y_train_lag = create_features_target(df_gb['Preço - petróleo bruto - Brent (FOB)'], lag=lag)
        X_test_lag, y_test_lag = create_features_target(df_gb['Preço - petróleo bruto - Brent (FOB)'], lag=lag)
        
        gb_model = train_gb_regressor(X_train_lag, y_train_lag, n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate)
        

        y_pred = gb_model.predict(X_test_lag)
        mse = mean_squared_error(y_test_lag, y_pred)
        rmse = np.sqrt(mse)
        print(f"Lag: {lag}, Max Depth: {max_depth}, Mean Squared Error: {mse}, Rmse: {rmse}")
        

        if mse < best_mse:
            best_mse = mse
            best_model = gb_model

X_pred = df_gb['Preço - petróleo bruto - Brent (FOB)'][-lag:].values.reshape(1, -1)  # Últimos 'lag' valores para previsão
forecast = []
for _ in range(prediction_days):
    next_day_pred = best_model.predict(X_pred)
    forecast.append(next_day_pred)
    X_pred = np.append(X_pred[:, 1:], next_day_pred).reshape(1, -1)'''
        show_code_model = st.checkbox('Mostrar código do Modelo')

        if show_code_model:
            st.code(code_model, language='python')

        if st.button("Rodar Modelo"):

            filename = 'modelo/modelo_gradientBoostRegressor.sav'
            loaded_model = pickle.load(open(filename, 'rb'))
            for i in range(1, 10):
                dados[f'lag{i}'] = dados['Preço - petróleo bruto - Brent (FOB)'].shift(i)
            df_novo = dados.dropna()
            X_novo = df_novo.drop(['Preço - petróleo bruto - Brent (FOB)','Data'], axis=1)
            X_novo = X_novo.head(1)
            previsoes = []
            N = 10
            for _ in range(N):
                proxima_previsao = loaded_model.predict(X_novo.values.reshape(1, -1))
            previsoes.append(proxima_previsao[0])
            X_novo = np.roll(X_novo, -1)
            X_novo[-1] = proxima_previsao
            st.write('Previsões para os novos dados:', previsoes)
                
            
