import plotly_express as px
import streamlit as st
import pandas as pd
import numpy as np
from dateutil import parser
import plotly.graph_objects as go

df = pd.read_excel(
    io="base.xlsx",
    engine="openpyxl",
    sheet_name= "Sheet1",
    skiprows=0,
    usecols="A:F",
    nrows=8000


)
#funçao de conversao dos clientes no formato 4 digitos
st.set_page_config(page_title="Sales",
                   page_icon=":bar_chart:",
                   layout="wide"
)

def format_string_to_4_digits(input_string):
    parts = input_string.split(".")
    formatted_string = parts[0]
    while len(formatted_string) < 4:
        formatted_string = "0" + formatted_string
    return formatted_string

def formatar_euro(valor):
    return '{:,.2f} €'.format(valor)

df ['Cliente'] = df.apply(lambda row:row['Data'] if row['Artigo'] != '' else None, axis=1)
df['Cliente'] = pd.to_numeric(df['Cliente'], errors='coerce')
df['Cliente'] = df['Cliente'].apply(lambda x: x if not pd.isna(x) else np.nan).ffill()
df['Cliente'] = df['Cliente'].astype(str)
df = df[~(df['Data'] == 'Total Cliente')]
df.dropna(subset=['Valor Líquido'], inplace=True)
df['Data'] = pd.to_datetime(df['Data'])
df['Mes_Ano'] = df['Data'].dt.strftime('%m-%Y')

df = df.sort_values(by='Cliente')

data = pd.read_excel('listagens.xlsx', sheet_name='Fornecedores')
data['Artigo'][1:] = data['Artigo'][1:].astype(str)
dicionario_fornecedores = dict(zip(data['Artigo'], data['Fornecedor']))
df['Marca'] = df['Artigo'].str[:3].map(dicionario_fornecedores)



data = pd.read_excel('listagens.xlsx', sheet_name='Clientes')
data['Vendedor'][1:] = data['Vendedor'][1:].astype(str)
data['Cliente'] = data['Cliente'].astype(str).apply(format_string_to_4_digits)
dicionario_clientes = dict(zip(data['Cliente'], data['Vendedor']))
df['Cliente'] = df['Cliente'].apply(format_string_to_4_digits)
df['Vendedor'] = df['Cliente'].str[:4].map(dicionario_clientes)



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


total_sales = int(df_selection["Valor Líquido"].sum())
#average_reating = round(df_selection["Valor Líquido"].mean(),1)
#star_rating = ":star:" * int(round(average_reating, 0))
#average_sales_by_transaction = round(df_selection["Valor Líquido"].mean(),2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total de vendas:")
    st.subheader(f"{total_sales:,.2f}€")

#with middle_column:
 #   st.subheader("Avaliações:")
 #   st.subheader(f"{average_reating} {star_rating}")


with right_column:
    st.subheader("")
 #   st.subheader(f"€{average_sales_by_transaction:,}")

st.markdown("---")


# sales by product line



sales_by_product_line = (
    df_selection.groupby(by=["Marca"]).sum()[["Valor Líquido"]].sort_values(by="Valor Líquido"))
sales_by_product_line["Valor Líquido"] = sales_by_product_line["Valor Líquido"].apply(formatar_euro)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Valor Líquido",
    y=sales_by_product_line.index,
    text = "Valor Líquido",
    orientation="h",
    title= "Vendas por marca",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
     width=800,
    height=1200
    #template="plotly_white"
)
print (sales_by_product_line)
st.plotly_chart(fig_product_sales)

# Sales by client

sales_client = (df_selection.groupby(by=["Cliente"]).sum()[["Valor Líquido"]])
sales_client = sales_client.sort_values(by="Valor Líquido", ascending=True)
sales_client["Valor Líquido"] = sales_client["Valor Líquido"].apply(formatar_euro) 
altura_por_linha = 30 
altura_da_figura = len(sales_client) * altura_por_linha

fig_product_client = px.bar(
    sales_client,
    x="Valor Líquido",
    y= sales_client.index,
    text = "Valor Líquido",
    orientation="h",
    title= "Vendas por Cliente",
    color_discrete_sequence=["#0083B8"] * len(sales_client),
    width=800,
    height=altura_da_figura,
    template="plotly_white"
)
fig_product_client.update_layout()

st.plotly_chart(fig_product_client)


hide_st_style = """
    <style>
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

