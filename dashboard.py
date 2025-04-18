import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# =====================
# DASHBOARD
# =====================
st.title("Dashboard Brasileirão 2023")

# Carregar dados
try:
    classificacao = pd.read_csv('brasileirao_2023_classificacao.csv')
    artilharia = pd.read_csv('brasileirao_2023_artilharia.csv')
    jogos = pd.read_csv('brasileirao_2023_jogos.csv')

    # Formatar datas para visualização amigável
    jogos['Date'] = pd.to_datetime(jogos['Date']).dt.strftime('%d/%m/%Y')

    # Filtros interativos
    st.sidebar.header("Filtros")
    times = classificacao['Time'].unique()
    time_selecionado = st.sidebar.selectbox("Selecione um time para ver os seus jogos", options=times)
    rodada_datas = jogos['Date'].unique()
    data_selecionada = st.sidebar.selectbox("Selecione uma data para ver os jogos do dia", options=rodada_datas)

    # Classificação
    st.header("Classificação")
    st.dataframe(classificacao)
    st.download_button("Baixar classificação", classificacao.to_csv(index=False), "classificacao.csv")

    # Gráfico de pontos por time
    fig1, ax1 = plt.subplots()
    ax1.bar(classificacao['Time'], classificacao['Pontos'], color='royalblue')
    plt.xticks(rotation=90)
    st.pyplot(fig1)

    # Saldo de gols por time
    st.subheader("Saldo de Gols por Time")
    fig_saldo, ax_saldo = plt.subplots()
    ax_saldo.bar(classificacao['Time'], classificacao['Saldo'], color='orange')
    plt.xticks(rotation=90)
    st.pyplot(fig_saldo)

    # Artilharia
    st.header("Top 10 Artilheiros")
    top10 = artilharia.sort_values('Gols', ascending=False).head(10)
    st.dataframe(top10)
    st.download_button("Baixar artilharia", artilharia.to_csv(index=False), "artilharia.csv")

    fig2, ax2 = plt.subplots()
    ax2.barh(top10['Jogador'], top10['Gols'], color='darkgreen')
    plt.gca().invert_yaxis()
    st.pyplot(fig2)

    # Jogos
    st.header("Jogos")
    st.dataframe(jogos)
    st.download_button("Baixar jogos", jogos.to_csv(index=False), "jogos.csv")

    # Filtro de jogos por time
    st.subheader(f"Jogos do {time_selecionado}")
    jogos_time = jogos[(jogos['Home Team'] == time_selecionado) | (jogos['Away Team'] == time_selecionado)]
    st.dataframe(jogos_time)

    # Filtro de jogos por data
    st.subheader(f"Jogos na data {data_selecionada}")
    jogos_data = jogos[jogos['Date'] == data_selecionada]
    st.dataframe(jogos_data)

    # Destaques
    st.header("Destaques")
    # Maior goleada
    jogos['Diff'] = jogos['Score'].apply(lambda x: abs(int(x.split('-')[0].strip()) - int(x.split('-')[1].strip())) if '-' in x else 0)
    maior_goleada = jogos.loc[jogos['Diff'].idxmax()]
    st.markdown(f"**Maior goleada:** {maior_goleada['Home Team']} {maior_goleada['Score']} {maior_goleada['Away Team']} em {maior_goleada['Date']}")

except FileNotFoundError as e:
    st.error(f"Erro ao carregar os dados: {e}")