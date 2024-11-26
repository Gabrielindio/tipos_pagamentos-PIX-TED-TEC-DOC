import requests as rq
import pandas as pd
import matplotlib
from datetime import datetime as dt, timedelta as td

#Definir api base url
api_base_bcb = 'https://olinda.bcb.gov.br/'
caminho_bcb = 'olinda/servico/MPV_DadosAbertos/versao/v1/odata/MeiosdePagamentosMensalDA(AnoMes=@AnoMes)?@AnoMes='
parametro1 = '%27'
parametro2 = '%27&$top=10000&$format=json&$select=AnoMes,'

#Definindo variaveis de anomes e quantidade de entidades retornadas.
anomes_ref = '202001'
retorno = '10000'

#Definindo variaveis para formas de pagamentos.
qtd_pagamento_1 = 'quantidadePix' 
valor_pagamento_1 = 'valorPix'
qtd_pagamento_2 = 'quantidadeTED'
valor_pagamento_2 = 'valorTED'
qtd_pagamento_3 = 'quantidadeTEC'
valor_pagamento_3 = 'valorTEC'
qtd_pagamento_4 = 'quantidadeDOC'
valor_pagamento_4 = 'valorDOC'

# Montar a URL
url = (
    f'{api_base_bcb}{caminho_bcb}{parametro1}{anomes_ref}{parametro2}'
    f'{qtd_pagamento_1},{valor_pagamento_1},{qtd_pagamento_2},{valor_pagamento_2},'
    f'{qtd_pagamento_3},{valor_pagamento_3},{qtd_pagamento_4},{valor_pagamento_4}'
)

# Fazer a requisição para a URL
response = rq.get(url)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    # Obter o JSON da resposta
    dados_json = response.json()

    # Verificar se a chave "value" está presente no JSON
    if "value" in dados_json:
        # Acessar os dados da chave "value"
        pagamento_mensal = []
        pagamento_mensal = dados_json["value"]
        df = pd.DataFrame(pagamento_mensal)

        df = df.rename(
            columns={
                'AnoMes':'ANOMES', 
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

# Garantir que a coluna 'ANOMES' está no formato string
df['ANOMES'] = df['ANOMES'].astype(str)

# Adicionar as colunas de ano e mês
df['ANO'] = df['ANOMES'].str[:4]
df['MES'] = df['ANOMES'].str[4:] 

# Mudar '.' por ','
colunas_para_alterar = ['Valor_PIX', 'QTD_PIX','Valor_TED','QTD_TED','Valor_DOC','QTD_DOC','Valor_TEC','QTD_TEC']
df[colunas_para_alterar] = df[colunas_para_alterar].astype(str).apply(lambda col: col.str.replace('.', ','))

print(df)