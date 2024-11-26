import requests as rq
import pandas as pd
import matplotlib
from datetime import datetime as dt, timedelta as td

#Definir api base url
api_base_bcb = 'https://olinda.bcb.gov.br/'
caminho_bcb = 'olinda/servico/MPV_DadosAbertos/versao/v1/odata/MeiosdePagamentosTrimestralDA(trimestre=@trimestre)?@trimestre='
parametro1 = '%27'
parametro2 = '%27&$top=10000&$format=json&$select=datatrimestre,'

#Definindo variaveis de trimestre e quantidade de entidades retornadas.
trimestre_ref = '20201'
retorno = '10000'
qtd_pagamentos = ['quantidadePix', 'quantidadeTED', 'quantidadeTEC', 'quantidadeDOC']
valor_pagamentos = ['valorPix', 'valorTED', 'valorTEC', 'valorDOC']

# Montar a URL com todas as variáveis
variaveis = ','.join(qtd_pagamentos + valor_pagamentos)
url = f"{api_base_bcb}{caminho_bcb}{parametro1}{trimestre_ref}{parametro2}{variaveis}"
# Fazer a requisição para a URL
response = rq.get(url)

# Verificar se a requisição deu certo, caso contrario retorna else
if response.status_code == 200:
    # Adciona o response dentro de um json 
    dados_json = response.json()
    # Adciona a chave value em uma lista
    if 'value' in dados_json:
        pagamento_trimestral = []
        pagamento_trimestral = dados_json['value']
        df = pd.DataFrame(pagamento_trimestral)

        df = df.rename(
            columns={
                'datatrimestre':'DATA', 
                'valorPix':'Valor_PIX', 
                'quantidadePix':'QTD_PIX',
                'valorTED':'Valor_TED', 
                'quantidadeTED':'QTD_TED',
                'valorDOC':'Valor_DOC',
                'quantidadeDOC':'QTD_DOC',
                'valorTEC':'Valor_TEC',
                'quantidadeTEC':'QTD_TEC'})
    else:
        print("Chave 'value' ausente no JSON.")
else:
    print(f"Falha na requisição para a URL (Status: {response.status_code})")

# Garantir que a coluna 'DATA' está no formato datetime
df['DATA'] = pd.to_datetime(df['DATA'])

# Adicionar coluna de ano, mes, trimestre
df['ANO'] = df['DATA'].dt.year
df['MES'] = df['DATA'].dt.month
df['TRIMESTRE'] = df['MES'].apply(lambda x: (x - 1) // 3 + 1)

# Criar um DF com o campo valor, com o campo INDICADOR
df_valor = df.melt(
    id_vars=['DATA','ANO', 'MES','TRIMESTRE'],
    value_vars=['Valor_PIX','Valor_TED','Valor_TEC','Valor_DOC'],
    var_name='INDICADOR',
    value_name='VALOR_REAL'
)
df_volume = df.melt(
    id_vars=['DATA','ANO', 'MES','TRIMESTRE'],
    value_vars=['QTD_PIX','QTD_TED','QTD_TEC','QTD_DOC'],
    var_name='INDICADOR', 
    value_name='VOLUME_REAL'
)

# Ajustar os nomes dos indicadores em ambas as tabelas
df_valor['INDICADOR'] = df_valor['INDICADOR'].str.replace('Valor_', '')
df_volume['INDICADOR'] = df_volume['INDICADOR'].str.replace('QTD_', '')

# Combinar as tabelas VALOR_REAL e VOLUME_REAL, alinhando os indicadores
df_final = pd.merge(
    df_valor,
    df_volume,
    on=['DATA','ANO', 'MES','TRIMESTRE', 'INDICADOR'], 
    how='outer'
)

colunas_para_alterar = ['VALOR_REAL','VOLUME_REAL']
df_final[colunas_para_alterar] = df_final[colunas_para_alterar].astype(str).apply(lambda col: col.str.replace('.', ','))

print(df_final)
