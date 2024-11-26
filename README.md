# Projeto de Análise de Meios de Pagamento (Mensal e Trimestral)  

Este repositório contém um projeto desenvolvido em Python para a coleta, transformação e análise de dados de meios de pagamento utilizando a API aberta do Banco Central do Brasil (BCB). Ele foi projetado para processar informações mensais e trimestrais, transformando os dados brutos da API em um DataFrame consolidado (`DF_FINAL`) para facilitar análises detalhadas e visualizações.  

---

## 🔎 **Descrição do Projeto**  

O projeto abrange dois principais cenários de análise:  

### **1. Dados Mensais de Pagamentos**  
- **Objetivo**: Coletar e transformar dados mensais de transações realizadas com as formas de pagamento PIX, TED, TEC e DOC.  
- **Destaques**:  
  - Organização dos dados por ano e mês a partir da coluna `AnoMes`.  
  - Renomeação de colunas para facilitar a leitura.  
  - Conversão dos valores numéricos para o formato com separador decimal brasileiro (`,`).  

### **2. Dados Trimestrais de Pagamentos**  
- **Objetivo**: Coletar e transformar dados trimestrais das mesmas formas de pagamento, com foco em análises comparativas por períodos mais longos.  
- **Destaques**:  
  - Criação de colunas adicionais para identificar o trimestre de cada registro.  
  - Consolidação de diferentes conjuntos de dados (quantidades e valores) em um único DataFrame.  
  - Geração do DataFrame final (`DF_FINAL`) com todas as informações necessárias.  

---

## ⚙️ **Tecnologias Utilizadas**  

- **Python 3**  
- **Bibliotecas Principais**:  
  - `requests`: Para consumir a API do Banco Central.  
  - `pandas`: Para manipulação e transformação dos dados.  
  - `datetime`: Para operações com datas.  

---

## 🧩 **Como Funciona o Projeto?**  

### **Coleta de Dados Mensais**  
1. O código utiliza a API aberta do Banco Central, parametrizando o mês de interesse com a variável `AnoMes`.  
2. Após a coleta, os dados brutos são processados e organizados em um DataFrame:  
   - Renomeação de colunas (`AnoMes` para `ANOMES`, `quantidadePix` para `QTD_PIX`, etc.).  
   - Criação de colunas auxiliares:  
     - `ANO` (os quatro primeiros dígitos de `ANOMES`).  
     - `MES` (os dois últimos dígitos de `ANOMES`).  
   - Conversão de valores numéricos para o formato brasileiro (`.` para `,`).  

### **Coleta de Dados Trimestrais**  
1. A API é parametrizada para coletar informações trimestrais de transações.  
2. Após a coleta, as etapas de processamento incluem:  
   - Separação dos dados em dois DataFrames:  
     - Um com as quantidades (`QTD_PIX`, `QTD_TED`, etc.).  
     - Outro com os valores transacionados (`VALOR_PIX`, `VALOR_TED`, etc.).  
   - Criação de colunas auxiliares para identificar o trimestre e ano do registro.  
   - Combinação dos DataFrames em uma única tabela consolidada (`DF_FINAL`).  

### **Transformação para DF_FINAL**  
- **Etapas de Transformação**:  
  1. Dados de quantidades e valores de transações são separados em tabelas intermediárias.  
  2. Cada tabela é renomeada para uniformizar os rótulos das colunas.  
  3. As tabelas são mescladas com base no identificador do período (`ANOMES` para dados mensais ou `TRIMESTRE` para trimestrais).  
  4. Colunas como `ANO`, `MES` e `TRIMESTRE` são adicionadas para facilitar análises temporais.  

- **Exemplo do DF_FINAL**:  
  ```plaintext
     ANO  MES  TRIMESTRE   QTD_PIX   VALOR_PIX  QTD_TED   VALOR_TED  
  0  2023   01         1     1000      1.000,00     500     5.000,00  
  1  2023   02         1     1500      1.500,00     600     6.500,00  
  2  2023   03         1     2000      2.000,00     700     7.000,00  
  ```

---

## 📂 **Estrutura do Repositório**  

```
.
├── pagamentos_mensais.py    # Código para coleta e transformação de dados mensais.
├── pagamentos_trimestrais.py # Código para coleta e transformação de dados trimestrais.
├── requirements.txt         # Lista de dependências do projeto.
├── README.md                # Documentação do projeto.
├── dados/                   # Diretório opcional para armazenamento de dados exportados.
└── gráficos/                # Diretório opcional para armazenar visualizações geradas.
```

---

## 🛠️ **Como Usar?**  

### **Pré-requisitos**  
1. Instalar o Python 3.8 ou superior.  
2. Instalar as dependências:  
   ```bash
   pip install -r requirements.txt
   ```

### **Passo a Passo**  
1. Clone este repositório:  
   ```bash
   git clone https://github.com/seu-usuario/repositorio-meios-de-pagamento.git
   cd repositorio-meios-de-pagamento
   ```

2. Execute o código desejado:  
   - Para dados mensais:  
     ```bash
     python pagamentos_mensais.py
     ```  
   - Para dados trimestrais:  
     ```bash
     python pagamentos_trimestrais.py
     ```  

3. O resultado será exibido no terminal ou salvo como CSV.  

---

## 📊 **Análises Visuais**  

Os dados do `DF_FINAL` podem ser utilizados para análises gráficas. Um exemplo de visualização:  
```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.barplot(data=df_final, x='TRIMESTRE', y='VALOR_PIX', ci=None)
plt.title('Valores Transacionados via PIX por Trimestre')
plt.xlabel('Trimestre')
plt.ylabel('Valor em R$')
plt.show()
```

---

## 📬 **Contato e Contribuição**  

Dúvidas, sugestões ou colaborações são bem-vindas!  
- **E-mail**: gabrielindio.i.c.2000@outlook.com  
- **LinkedIn**: https://www.linkedin.com/in/gabriel-%C3%A2ndreas-16a649285 

Contribua com este projeto enviando pull requests ou abrindo issues. 😊  
