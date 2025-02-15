import streamlit as st
import pandas as pd
import altair as alt

# Importar o CSV da pasta 'data'
file_path = "data/acuracidade.csv"  # Substitua pelo nome correto do seu arquivo
df = pd.read_csv(file_path, parse_dates=True)

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

st.sidebar.header('Inventário Cíclico SAE')

st.sidebar.markdown('''
---
SAE Digital \n
Arco Educação
''')

# Remover espaços extras dos nomes das colunas
df.columns = df.columns.str.strip()

# Converter a coluna 'Data' para o tipo datetime
df['Data'] = pd.to_datetime(df['Data'])

# Criar uma nova coluna com o dia e o mês formatados
df['DiaMês'] = df['Data'].dt.strftime('%d-%m')

# Criar uma coluna com a data no formato YYYYMMDD para ordenação
df['DataOrdenada'] = df['Data'].dt.strftime('%Y%m%d').astype(int)

# Calcular as métricas
total_itens_contados = int(df["Fisico"].sum())  # Removendo casas decimais
diferenca_net = int(df["<>Net"].sum())  # Removendo casas decimais
diferenca_abs = int(df["<>Abs"].sum())  # Removendo casas decimais

# Ajustar formatação percentual (converter de decimal para %)
percentual_diferenca_net = df["%Net"].mean() * 100  # Convertendo decimal para percentual
percentual_diferenca_abs = df["%Abs"].mean() * 100  # Convertendo decimal para percentual

# Total em Reais (ajustar para R$)
total_custo = df["custoDif"].sum()

# Exibir as métricas
st.markdown('### Metrics')
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Total Itens Contados", f"{total_itens_contados:,}")
col2.metric("Diferença Net", f"{diferenca_net:,}")
col3.metric("Diferença Abs", f"{diferenca_abs:,}")
col4.metric("% Diferença Net", f"{percentual_diferenca_net:.2f}%")
col5.metric("% Diferença Abs", f"{percentual_diferenca_abs:.2f}%")
col6.metric("Total R$", f"R$ {total_custo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# Row B
st.markdown('### Acuracidade')

source = df

# Criação do gráfico na tab1 com %Net no eixo Y
chart1 = alt.Chart(source).mark_bar(color='#446bb4').encode(
    x=alt.X('DataOrdenada:O', axis=alt.Axis(labelAngle=0, title='Data')),  # Ordenar por DataOrdenada
    y='%Net'
).properties(height=400)

chart1 = chart1.encode(
    x=alt.X('DiaMês:N', axis=None)  # Exibir DiaMês como rótulos, sem eixo
)


# Adicionando os rótulos com valores em cima das barras
labels_tab1 = alt.Chart(source).mark_text(
    dy=-30,  # Distância do rótulo em relação à barra
    size=20,  # Tamanho da fonte
    color='black'
).encode(
    x='DataOrdenada:O',
    y='%Net:Q',
    text=alt.Text('%Net:Q', format='.2%')  # Formata os valores para duas casas decimais
)

# Criação do gráfico na tab2 com %Abs no eixo Y
chart2 = alt.Chart(source).mark_bar(color='#1d9ed9').encode(
    x=alt.X('DataOrdenada:O', axis=alt.Axis(labelAngle=0, title='Data')),  # Ordenar por DataOrdenada
    y='%Abs'
).properties(height=400)

chart2 = chart2.encode(
    x=alt.X('DiaMês:N', axis=None)  # Exibir DiaMês como rótulos, sem eixo
)

# Adicionando os rótulos para o segundo gráfico
labels_tab2 = alt.Chart(source).mark_text(
    dy=-30,
    size=20,
    color='black'
).encode(
    x='DataOrdenada:O',
    y='%Abs:Q',
    text=alt.Text('%Abs:Q', format='.2%')
)

# Criando as abas
tab1, tab2 = st.tabs(["Diferença Net", "Diferença Abs"])

with tab1:
    st.altair_chart(chart1 + labels_tab1, theme="streamlit", use_container_width=True)

with tab2:
    st.altair_chart(chart2 + labels_tab2, theme="streamlit", use_container_width=True)

# Row C - Quantidade Itens Dia
st.markdown('### Itens')

# Criando o gráfico de linha
line_chart = alt.Chart(df).mark_line(
    strokeWidth=4,  # Aumenta a grossura da linha
    color="#161B33"  # Define a cor da linha
).encode(
    x=alt.X('DataOrdenada:O', axis=alt.Axis(labelAngle=0, title='Data')),  # Ordenar por DataOrdenada
    y='Fisico:Q'
).properties(height=400)

line_chart = line_chart.encode(
    x=alt.X('DiaMês:N', axis=None)  # Exibir DiaMês como rótulos, sem eixo
)

# Adicionando os nós (pontos) nos valores da linha
points = alt.Chart(df).mark_circle(
    size=80,  # Define o tamanho do nó
    color="#161B33"  # Define a cor do nó igual à da linha
).encode(
    x='DataOrdenada:O',
    y='Fisico:Q'
)

# Adicionando labels nos pontos da linha
labels_line = alt.Chart(df).mark_text(
    dy=-30,  # Posição do label acima do ponto
    size=20,
    color='black'
).encode(
    x='DataOrdenada:O',
    y='Fisico:Q',
    text=alt.Text('Fisico:Q', format='.0f')  # Exibe o valor sem casas decimais
)

# Criando o gráfico de barras (Diferença de Contagem)
predicate = alt.datum["<>Net"] > 0
color = alt.condition(predicate, alt.value("#446bb4"), alt.value("#cd1f3b"))

bars = alt.Chart(df).mark_bar().encode(
    x=alt.X('DataOrdenada:O', axis=alt.Axis(labelAngle=0, title='Data')),  # Ordenar por DataOrdenada
    y="<>Net:Q",  # Eixo Y como quantitativo
    color=color  # Cor condicional
).properties(height=400)

bars = bars.encode(
    x=alt.X('DiaMês:N', axis=None)  # Exibir DiaMês como rótulos, sem eixo
)

# Adicionando os labels para as barras
labels_bars = alt.Chart(df).mark_text(
    align="center",
    baseline="bottom",
    dy=-30,  # Ajuste da posição vertical
    fontSize=20,
    color="black"
).encode(
    x='DataOrdenada:O',
    y="<>Net:Q",
    text=alt.Text("<>Net:Q", format=".0f")  # Exibe o valor sem casas decimais
)

# Criando as abas
tab1, tab2 = st.tabs(["Itens por Dia", "Diferença de Contagem"])

with tab1:
    st.altair_chart(line_chart + points + labels_line, use_container_width=True)

with tab2:
    st.altair_chart(bars + labels_bars, use_container_width=True)