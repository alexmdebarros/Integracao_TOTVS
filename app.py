import pandas as pd
from datetime import datetime


df = pd.read_csv('bhan2.csv', sep=';', encoding='latin1')

#escrever arquivo com os dados das colunas separando por pipe

with open('comissoes.txt', 'w', encoding='utf-8') as f:
    for i in range(len(df)):
        # Define as variáveis com os valores das colunas
        data = datetime.now().strftime('%d/%m/%Y')
        cnpj = '79124079000201'
        conta_deb = '4.2.01.02.01'
        conta_cred = '2.1.05.04.01'
        valor = df['COMISSAO'][i].replace('.', '').replace(',', '.')  # Garante que está no formato correto
        cod_hist = df['COD_HIST'][i]

        # Formata o valor para garantir a vírgula como separador decimal
        valor_formatado = f"{float(valor):.2f}".replace('.', ',')  # Converte para float e formata com vírgula

        # Formata a string de saída com os valores
        linha = f"||{data}|{cnpj}|{conta_deb}||{valor_formatado}|D|{cod_hist}||\n"
        linha += f"||{data}|{cnpj}|{conta_cred}||{valor_formatado}|C|{cod_hist}||\n"

        # Escreve a linha no arquivo
        f.write(linha)

with open('adiantamentos.txt', 'w', encoding='utf-8') as f:

    for i in range(len(df)):
        adiantamento = df['ADIANTAMENTO'][i].strip()
        vendedor = df['VENDEDOR'][i].strip()
        
        if adiantamento in["", "0", "0,00", "0.00"]:
            continue
        elif vendedor in["ROITE REPRESENTACOES"]:
            continue

        data = datetime.now().strftime('%d/%m/%Y')
        cnpj = '79124079000201'
        adt_conta_deb = '4.2.01.02.01'
        adt_conta_cred = '2.1.05.04.01'
        adiantamento = df['ADIANTAMENTO'][i].replace('.', '').replace(',', '.')
        vendedor = df['VENDEDOR'][i]

        # Formata o valor para garantir a vírgula como separador decimal
        valor_adt_formatado = f"{float(adiantamento):.2f}".replace('.', ',')  # Converte para float e formata com vírgula

        # Formata a string de saída com os valores
        linha = f"||{data}|{cnpj}|{conta_deb}||{valor_adt_formatado}|D|1990|{vendedor}|\n"
        linha += f"||{data}|{cnpj}|{conta_cred}||{valor_adt_formatado}|C|1990|{vendedor}|\n"

        # Escreve a linha no arquivo
        f.write(linha)
print('Arquivos salvos com sucesso!')