import plotly_express as px
import streamlit as st
import pandas as pd
import numpy as np
from dateutil import parser
import plotly.graph_objects as go


df = pd.read_excel(
    io="mes.xlsx",
    engine="openpyxl",
    sheet_name= "mes",
    skiprows=0,
    usecols="A:J",
    nrows=4000
)

df= df.drop(columns=['A. BORGES DO AMARAL, Lda.'])

novos_nomes = {
    'Unnamed: 1': 'Data',
    'Unnamed: 2': 'CodigoCliente',
    'Unnamed: 3': 'Cliente',
    'Unnamed: 4': 'DescontoCliente',
    'Unnamed: 5': 'DescontoArtigo',
    'Unnamed: 6': 'NomeArtigo',
    'Unnamed: 7': 'ValorArtigo',
    'Unnamed: 8': 'Vendedor',
    'Unnamed: 9': 'CodigoVendedor'
}

df.rename(columns=novos_nomes, inplace=True)
df = df.dropna(subset=['ValorArtigo'])
print(df.columns)

df2 = pd.read_excel(
    io="2022.xlsx",
    engine="openpyxl",
    sheet_name= "2022",
    skiprows=0,
    usecols="A:J",
    nrows=4000
)

df2= df2.drop(columns=['A. BORGES DO AMARAL, Lda.'])

novos_nomes2 = {
    'Unnamed: 1': 'Data',
    'Unnamed: 2': 'CodigoCliente',
    'Unnamed: 3': 'Cliente',
    'Unnamed: 4': 'NomeArtigo',
    'Unnamed: 5': 'ValorArtigo',
    'Unnamed: 6': 'Vendedor',
}

df2.rename(columns=novos_nomes2, inplace=True)
df2 = df2.dropna(subset=['ValorArtigo'])

st.set_page_config(page_title="Sales",
                   page_icon=":bar_chart:",
                   layout="wide"
)

def formatar_euro(valor):
    return '{:,.2f}€'.format(valor)

df['Data'] = pd.to_datetime(df['Data'], format='%d-%m-%Y', errors='coerce')
df['Mes_Ano'] = df['Data'].dt.strftime('%m-%Y')
#df = df.sort_values(by='Cliente')

df2['Data'] = pd.to_datetime(df2['Data'], format='%d-%m-%Y', errors='coerce')
df2['Mes_Ano'] = df2['Data'].dt.strftime('%m-%Y')

data = pd.read_excel('listagens.xlsx', sheet_name='Fornecedores')
data.loc[1:, 'Artigo'] = data['Artigo'][1:].astype(str)
dicionario_fornecedores = dict(zip(data['Artigo'], data['Fornecedor']))
df['Marca'] = df['NomeArtigo'].str[:3].map(dicionario_fornecedores)
df2['Marca'] = df2['NomeArtigo'].str[:3].map(dicionario_fornecedores)
#side bar

st.sidebar.header("Filtros de análise:")
vendedor = st.sidebar.multiselect(
    "selecione o vendedor:",
    options=df["Vendedor"].unique(),
    default=df["Vendedor"].unique()
)

marca = st.sidebar.multiselect(
    "selecione a Marca",
    options=df["Marca"].unique(),
    default=df["Marca"].unique()
)
mes_Ano = st.sidebar.multiselect(
    "selecione o Mês Ano",
    options=df["Mes_Ano"].unique(),
    default=df["Mes_Ano"].unique()
)

cliente = st.sidebar.multiselect(
    "selecione o Cliente:",
    options=df["Cliente"].unique(),
    default=df["Cliente"].unique()
)
df_selection =df.query(
    "Vendedor == @vendedor & Cliente==@cliente & Mes_Ano==@mes_Ano & Marca==@marca"
)


# --- MAINPAGE ---


st.title(":bar_chart: Dashboard de vendas")
st.markdown("##")

df = df.iloc[1:]
df['ValorArtigo'] = pd.to_numeric(df['ValorArtigo'], errors='coerce')
df_selection['ValorArtigo'] = pd.to_numeric(df_selection['ValorArtigo'], errors='coerce')
total_sales = df_selection["ValorArtigo"].sum(skipna=True)

df2 = df2.iloc[1:]
df2['ValorArtigo'] = pd.to_numeric(df['ValorArtigo'], errors='coerce')
df_selection['ValorArtigo'] = pd.to_numeric(df_selection['ValorArtigo'], errors='coerce')
total_sales = df_selection["ValorArtigo"].sum(skipna=True)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total de vendas:")
    st.subheader(f"{total_sales:,.2f}€")



with right_column:
    st.subheader("")

st.markdown("---")



# --- sales graphic ---

# Sales by client
sales_client = df_selection.groupby(by=["Cliente"])["ValorArtigo"].sum().reset_index()
sales_client = sales_client.sort_values(by="ValorArtigo", ascending=True)
sales_client["ValorArtigo"] = sales_client["ValorArtigo"].apply(formatar_euro)

altura_desejada_por_cliente = 20  # Defina a altura desejada por cliente em pixels
altura_desejada = max(len(sales_client) * altura_desejada_por_cliente, 400)  # Defina uma altura mínima

# Sales last year
sales_last = df_selection.groupby(by=["Cliente"])["ValorArtigo"].sum().reset_index()
sales_last = sales_last.sort_values(by="ValorArtigo", ascending=True)
sales_last["ValorArtigo"] = sales_last["ValorArtigo"].apply(formatar_euro)

# -- grafico comparativo --

fig = go.Figure()

fig.add_trace(go.Bar(
    y=sales_last["Cliente"],
    x=sales_last["ValorArtigo"],
    name="Meta",
    orientation='h',
    marker=dict(color='red'),  
    width=0.5

))

fig.add_trace(go.Bar(
    y=sales_client["Cliente"],
    x=sales_client["ValorArtigo"],
    name="Valor atual",
    orientation='h',
    marker=dict(color='blue'),  
    width=0.5
    
))

fig.update_layout(
    title="Gráfico de Barras Sobreposto Horizontal",
    xaxis_title="Valores",
    yaxis_title="Cliente",
    barmode="overlay",
    width=800,
    height=len(sales_client) * 15
)
fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")

st.plotly_chart(fig)

hide_st_style = """
    <style>
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)