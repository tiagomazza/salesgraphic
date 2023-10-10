import pandas as pd

# Crie os DataFrames df1 e df2
data1 = {'Cliente': ['Alice', 'Bob', 'Fred'],'ID': [1, 2, 3]}
df1 = pd.DataFrame(data1)

data2 = {'Cliente': ['Bob', 'David', 'Eve']}
df2 = pd.DataFrame(data2)

# Use o método concat para combinar os DataFrames e manter apenas os valores únicos
df_resultado = pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)

# Imprima o DataFrame resultante
print(df_resultado)



