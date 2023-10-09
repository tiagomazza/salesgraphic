import pandas as pd
caminho_arquivo_xls = 'mes.xls'
df = pd.read_excel(caminho_arquivo_xls)

df= df.drop(columns=['A. BORGES DO AMARAL, Lda.'])

novos_nomes = {
    'Unnamed: 1': 'Data',
    'Unnamed: 2': 'CodigoCliente',
    'Unnamed: 3': 'NomeCliente',
    'Unnamed: 4': 'DescontoCliente',
    'Unnamed: 5': 'DescontoArtigo',
    'Unnamed: 6': 'NomeArtigo',
    'Unnamed: 7': 'ValorArtigo',
    'Unnamed: 8': 'NomeVendedor',
    'Unnamed: 9': 'CodigoVendedor'

}

df.rename(columns=novos_nomes, inplace=True)
df = df.dropna(subset=['ValorArtigo'])
print(df.columns)



