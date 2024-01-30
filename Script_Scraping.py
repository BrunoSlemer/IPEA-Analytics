import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

link_IPEA = "http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view"
requisicao = requests.get(link_IPEA)

path_git = 'https://raw.githubusercontent.com/BrunoSlemer/IPEA-Analytics/main/ipea.csv'
path = 'D:/Fiap/TechChallenge/04/ipea.csv'

def update_dataframe(df, new_data):
    df['Data'] = pd.to_datetime(df['Data'], dayfirst= True)
    new_data['Data'] = pd.to_datetime(new_data['Data'], dayfirst=True)
    
    last_date = df['Data'].max()
    
    new_rows = new_data[new_data['Data'] > last_date]
    
    if not new_rows.empty:
        updated_df = pd.concat([df, new_rows], ignore_index=True)
    else:
        updated_df = df
    return updated_df


if requisicao.status_code == 200:
    html_ipea = BeautifulSoup(requisicao.text, "html.parser")
    tabela_ipea = html_ipea.find('table', {"id":"grd_DXMainTable"})
    
    df_ipea = pd.read_html(str(tabela_ipea), header=0)[0]
    
    try:
        existing_df = pd.read_csv(path_git)
    except FileNotFoundError:
        existing_df = df_ipea
        
    updated_df = update_dataframe(existing_df, df_ipea)
    updated_df.to_csv(path,sep=',', header= True, index=False)
    
    updated_df.head(10)
else:
    print("Erro na requisição: ",requisicao.status_code)