import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import nltk
from nltk import tokenize
from processando_texto import text_process
st.set_page_config(layout="wide")

def frequency_graph_plotly(df, column, number):
    all_word = ' '.join([texto for texto in df[column]])

    space_token = tokenize.WhitespaceTokenizer()
    text_token = space_token.tokenize(all_word)
    frequency = nltk.FreqDist(text_token)

    df_frequency = pd.DataFrame({
        'word': list(frequency.keys()),
        'frequency': list(frequency.values())
    })

    top_words = df_frequency.nlargest(number, 'frequency')

    fig = px.bar(
        top_words,
        x='word',
        y='frequency',
        color='frequency',
        color_continuous_scale='Oranges'
    )

    fig.update_layout(height=400)

    st.plotly_chart(fig, use_container_width=True)

df = pd.read_excel('data/Case - Base de Dados.xlsx',sheet_name='Base')
df_brutos = df

# TRATANDO OS DADOS
df = df.dropna(subset=['Nota'])

df['Versão APP'] = df['Versão APP'].fillna('Desconhecido')

category = {1: 'Ruim',
            2: 'Ruim',
            3: 'Neutro',
            4: 'Boa',
            5: 'Boa'}

df['category'] = df['Nota'].map(category)

df['Comentário'] = df['Comentário'].str.lower()

tp = text_process()
df['processingWhiteSpace'] = tp.processingWhiteSpace(df,'Comentário')
df['stopWordsUnidecode'] = tp.stopWordsUnidecode(df,'processingWhiteSpace')



tab1, tab2, tab3 = st.tabs(["Dados Brutos", "📈 Dashboard", "Tomada de decisão"])

with tab1:
    st.dataframe(df_brutos)
with tab2:

    # FILTROS LATERAIS
    st.sidebar.header("Filtros")

    versoes = st.sidebar.multiselect(
        "Versão do App",
        df['Versão APP'].unique(),
        default=df['Versão APP'].unique()
    )

    df_filtrado = df[df['Versão APP'].isin(versoes)]

    # KPIs
    st.markdown("## Visão Geral")

    total_comentarios = len(df_filtrado)
    nota_media = round(df_filtrado['Nota'].mean(), 2)
    percentual_ruim = round((df_filtrado['category'] == 'Ruim').mean() * 100, 1)

    k1, k2, k3 = st.columns(3)

    k1.metric("Total de Comentários", total_comentarios)
    k2.metric("Nota Média Geral", nota_media)
    k3.metric("% Avaliações Ruins", f"{percentual_ruim}%")

    st.divider()

    # DASHBOARD TEMÁTICO
    st.markdown("## Análise por Tema")

    col1, col2, col3 = st.columns(3)

    def pie_tema(df_base, regex, titulo):
        dados = df_base[df_base['stopWordsUnidecode'].str.contains(
            regex, case=False, regex=True, na=False
        )]

        if len(dados) == 0:
            st.warning("Sem dados para este tema.")
            return

        categoria = dados['category'].value_counts().reset_index()
        categoria.columns = ['category', 'count']

        fig = px.pie(
            categoria,
            values='count',
            names='category',
            color_discrete_sequence=["#FB8C82", "#9FDDA2", "#FDE47E"]
        )

        fig.update_traces(
            textinfo='percent+label',
            textposition='inside'
        )

        fig.update_layout(
            width=350,
            height=350,
            showlegend=False
        )

        st.markdown(f"### {titulo}")
        st.caption(f"Total de comentários: {len(dados)}")
        st.plotly_chart(fig, use_container_width=True)


    with col1:
        pie_tema(df_filtrado,
                 "pix|dinheiro|transferencia|emprestimo",
                 "Pix e Transações")

    with col2:
        pie_tema(df_filtrado,
                 "atendimento|contato|suporte|ligar",
                 "Atendimento")

    with col3:
        pie_tema(df_filtrado,
                 "erro|trava|problema|cadastro",
                 "Falhas Operacionais")

    st.divider()

    # EVOLUÇÃO TEMPORAL
    st.markdown("## Distribuição de Categorias por Versão do App")

    agrupado = (
    df.groupby(['Versão APP', 'category'])
      .size()
      .reset_index(name='count')
    ).sort_values('Versão APP')

    fig = px.bar(
        agrupado,
        x='Versão APP',
        y='count',
        color='category',
        barmode='group',
        color_discrete_map={
            'Boa': "#58D458",
            'Ruim': "#B44040",
            'Neutro': "#BBAA48"
        }
    )

    fig.update_layout(
        xaxis_title='Versão do App',
        yaxis_title='Quantidade de Comentários'
    )
    st.plotly_chart(fig)

    st.divider()

    # TOP PALAVRAS
    st.markdown("## Top 20 Palavras Mais Frequentes")

    frequency_graph_plotly(df_filtrado, 'stopWordsUnidecode', 20)
with tab3:
    st.markdown("""
        # Tomada de Decisão 

        ## Visão geral
        Atualmente, o aplicativo apresenta uma média geral de 4.09, restando uma lacuna de 0.91 pontos para atingirmos a nota máxima. Com base em uma amostragem de 702 comentários, identificamos que 80,6% das avaliações são positivas; no entanto, o índice de 19,4% de avaliações negativas revela uma oportunidade clara de melhoria para elevar o patamar da experiência do usuário.

        ## Seção de Temas mais frequentes
        Com a analise de palavras-chave, foi possível identificar os principais temas abordados nas avaliações - Pix e Transações, Atendimento e Falhas Operacionais:
        
        - Pix e Transações : Apresentou um volume significativo de comentários com 85 comentários ao todo, 51.8% são comentarios de insatisfação,31.8% bons comentários e 16.4% neutros, indicando uma preocupação dos usuários com esse aspecto do aplicativo.
        - Atendimento:  Se destacou com 40 comentários, dos quais 55% são negativos, 35% positivos e 10% neutros.
        - Falhas Operacionais: Obteve 58 comentários, com 63.8% sendo negativos, 22.4% positivos e 13.8% neutros.

        ## Seção Distribuição de Categorias por Versão do App
        Nas versões iniciais do aplicativo, versão 1.37.7, as avaliações boas são dominantes com 113 comentários, enquanto as avaliações ruins são significativamente menores, com apenas 12 comentários e 8 comentários neutros.
        A partir das versões 1.45.5, 1.47.2 e 1.47.3, houve uma baixa nas avaliações boas, com 62, 81 e 27 comentários respectivamente, enquanto as avaliações ruins aumentaram para 20, 17 e 17 comentários.
        Isso indica a possibilidade de um bug, impacto do surgimento do pix ou novas mudanças na interface do aplicativo que impactaram a experiência do usuário. É preciso investigar mais a fundo para entender as causas dessa mudança.

        ## Decisão
        - Investigar se o surgimento do pix foi um fator que contribuiu para a queda nas avaliações boas e o aumento nas avaliações ruins.
        - Fazer uma revisão técnica sobre o pix e as mudanças nas versões do aplicativo, para identificar possíveis problemas que possam ter impactado a experiência do usuário.
        - Treinar a equipe de suporte para lidar melhor com as reclamações relacionadas ao pix e às mudanças no aplicativo.

        *Observação: A inteligência artificial foi utilizada como ferramenta de apoio para relembrar o uso de determinadas funções e auxiliar com sugestões de debugging.*

    """)