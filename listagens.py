import pandas as pd

data = pd.read_excel('listagens.xlsx', sheet_name='Vendedores')
dicionario_vendedores = dict(zip(data['Vendedor'], data['Nome']))
#print(dicionario_vendedores)

data = pd.read_excel('listagens.xlsx', sheet_name='Fornecedores')
data['Artigo'][1:] = data['Artigo'][1:].astype(str)
dicionario_fornecedores = dict(zip(data['Artigo'], data['Fornecedor']))
#print(dicionario_fornecedores)


data = pd.read_excel('listagens.xlsx', sheet_name='Clientes')

dicionario_clientes = dict(zip(data['Vendedor'], data['Cliente']))
print(dicionario_clientes)