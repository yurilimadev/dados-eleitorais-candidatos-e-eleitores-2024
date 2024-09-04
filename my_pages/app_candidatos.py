import streamlit as st
import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from streamlit_folium import st_folium
import folium
from my_pages.app_eleitores import app_eleitores


sns.set_theme('notebook')
dtypes_dict_can = {
    'Ano de eleição': 'category',
    'Cargo': 'category',
    'Coligação': 'category',
    'Cor/raça': 'category',
    'Detalhe da situação de candidatura': 'category',
    'Estado civil': 'category',
    'Etnia indígena': 'category',
    'Faixa etária': 'category',
    'Federação': 'category',
    'Gênero': 'category',
    'Grau de instrução': 'category',
    'Identidade de gênero': 'category',
    'Município': 'category',
    'Nacionalidade': 'category',
    'Nome social': 'category',
    'Ocupação': 'category',
    'Quilombola': 'category',
    'Reeleição': 'category',
    'Região': 'category',
    'Sigla partido': 'category',
    'Situação de cadastramento': 'category',
    'Situação de candidatura': 'category',
    'Situação de cassação': 'category',
    'Situação de desconstituição': 'category',
    'Situação de julgamento': 'category',
    'Situação de totalização': 'category',
    'Tipo eleição': 'category',
    'Turno': 'int16',
    'UF': 'category',
    'Quantidade de candidatos': 'float32',
    'Quantidade de candidatos eleitos': 'int16',
    'Quantidade de candidatos para o 2º turno': 'float32',
    'Quantidade de candidatos não eleitos': 'int16',
    'Quantidade de candidatos suplentes': 'int16',
    'Quantidade de candidatos não informados': 'int16',
    'Data de carga': 'category'
}

coordenadas_estados = {'AC': [-8.77, -70.55],
                       'AL': [-9.71, -35.73],
                       'AM': [-3.07, -61.66],
                       'AP': [1.41, -51.77],
                       'BA': [-12.96, -38.51],
                       'CE': [-3.71, -38.54],
                       'ES': [-19.19, -40.34],
                       'GO': [-16.64, -49.31],
                       'MA': [-2.55, -44.30],
                       'MT': [-12.64, -55.42],
                       'MS': [-20.51, -54.54],
                       'MG': [-18.10, -44.38],
                       'PA': [-5.53, -52.29],
                       'PB': [-7.06, -35.55],
                       'PR': [-24.89, -51.55],
                       'PE': [-8.28, -35.07],
                       'PI': [-8.28, -43.68],
                       'RJ': [-22.84, -43.15],
                       'RN': [-5.79, -35.21],
                       'RO': [-11.22, -62.80],
                       'RS': [-30.01, -51.22],
                       'RR': [1.89, -61.22],
                       'SC': [-27.33, -49.44],
                       'SE': [-10.90, -37.07],
                       'SP': [-23.55, -46.64],
                       'TO': [-10.25, -48.25]
                       }
candidatos_24 = pd.read_csv('candidatos_2024.csv',
                            sep=';',
                            encoding='latin-1',
                            dtype=dtypes_dict_can, decimal=',')
candidatos_20 = pd.read_csv('candidatos_2020.csv',
                            sep=';',
                            encoding='latin-1',
                            dtype=dtypes_dict_can, decimal=',')
candidatos_20_24 = pd.concat([candidatos_20, candidatos_24])


def app_candidatos():

    st.title('Dados Eleitorais - Candidatos - 2024')
    st.subheader("""Essa análise contem análise de dados inspirada em uma notícia do G1, a qual fala sobre o perfil geral dos candidatos para eleições municipais de 2024. Esse projeto tem o intuito de fazer um 'checagem de dados' tanto para treinar o pensamento analítico e quando outras habilidades para um futuro profissional estatístico.""")

    # GRÁFICO DE BARRAS MOSTRANDO ÀS DIFERENÇAS DE GÊNERO
    genero = candidatos_20_24.groupby(
        ['Ano de eleição', 'Gênero'], observed=False).agg(count=('Gênero', 'size'))
    genero = genero.reset_index()
    fig_bar = plt.figure(figsize=(20, 8))
    sns.barplot(data=genero, x='Gênero', y='count',
                hue='Ano de eleição', palette=['green', 'blue'])
    plt.title('Gênero mais presente de candidatos entre 2020 e 2024',
              fontdict={'fontsize': 20})
    plt.xlabel('Gênero', fontdict={'fontsize': 20})
    plt.ylabel('Contagem', fontdict={'fontsize': 20})
    st.markdown('Iniciamos com o gráfico demonstrando a diferenças entre 2020 e 2024 sobre a quantidade de candidatos pelo gênero. É possível notar que temos reduções de registros em ambos os gêneros. Contudo, ainda temos um número superior de homens em relação às mulheres em ambos os anos de eleições municipais. Em 2020 alguns candidatos colocaram a opção não divulgável, o que podemos supor que pode ser apenas por esquecimento na hora do registro ou porque o candidato não se identificava com nenhum dos gêneros ou porque não diz divulgar literalmente, mas em 2024 (ano dessa análise) isso não ocorreu.')
    st.pyplot(fig=fig_bar, use_container_width=True)

    # GRÁFICO DE BARRAS HORIZONTAL MOSTRANDO A QUANTIDADE DE REGISTROS POR RAÇA
    fig_barh, ax = plt.subplots(1, 2, figsize=(20, 8))

    cor_raca = candidatos_20_24.groupby(
        ['Ano de eleição', 'Cor/raça'], observed=False).agg(count=('Cor/raça', 'size'))
    custom_palette_20 = ["#3498db", "#9b59b6", "#2ecc71",
                         "#e74c3c", "#f1c40f", "#9b59b6", "#9b59b6"]
    custom_palette_24 = ["#3498db", "#9b59b6",
                         "#e74c3c", "#f1c40f", "#9b59b6", "#9b59b6"]

    sns.barplot(y=cor_raca.loc['2020'].index,
                x=cor_raca.loc['2020']['count'],
                ax=ax[0],
                palette=custom_palette_20, hue=cor_raca.loc['2020'].index)
    sns.barplot(y=cor_raca.loc['2024'].index,
                x=cor_raca.loc['2024']['count'],
                ax=ax[1],
                palette=custom_palette_24, hue=cor_raca.loc['2024'].index)

    for container in ax[0].containers:
        ax[0].bar_label(container)
        ax[0].margins(x=0.3)

    for container in ax[1].containers:
        ax[1].bar_label(container)
        ax[1].margins(x=0.3)

    fig_barh.suptitle('Contagem de Raças entre 2020 e 2024', fontsize=20)
    st.markdown('Continuando a análise, seguimos verificando quais são as raças mais frequentes nos dados de 2020 e 2024. Segundo a matéria em 2024, 53% dos candidatos se identificavam como negro ou pardo, mas como podemos ver no gráfico, a maior quantidade de registros de raça são de candidatos que se identificam como Branco. ')
    st.pyplot(fig=fig_barh, use_container_width=True)

    # GRÁFICO DE NUVENS DE PALAVRAS PARA VERIFICAR A FREQUENCIA DE ESTADO CIVIL
    estado_civil = candidatos_20_24.groupby(
        ['Ano de eleição', 'Estado civil'], observed=False).agg(count=('Estado civil', 'size'))
    counts_2020 = estado_civil.loc['2020'].to_dict()['count']
    counts_2024 = estado_civil.loc['2024'].to_dict()['count']

    fig_cloud, axes = plt.subplots(1, 2, figsize=(20, 6))

    wordcloud1 = WordCloud(width=800,
                           height=400,
                           background_color='white', min_font_size=10,
                           max_font_size=500, relative_scaling=0.8, colormap='cividis').generate_from_frequencies(counts_2020)
    wordcloud2 = WordCloud(width=800,
                           height=400,
                           background_color='white',
                           max_font_size=150, relative_scaling=0.8, colormap='plasma').generate_from_frequencies(counts_2024)

    axes[0].imshow(wordcloud1, interpolation='bilinear')
    axes[0].set_title('2020', fontsize=20)
    axes[0].axis("off")
    axes[1].imshow(wordcloud2, interpolation='bilinear')
    axes[1].set_title('2024', fontsize=20)
    axes[1].axis("off")

    fig_cloud.suptitle(
        'Nuvem de palavras - Estado Civil (2020 - 2024)', fontsize=20)
    st.markdown(
        'De acordo com a matéria do G1, o que tivemos de mais frequente são pessoas casadas. Tanto em 2020 e 2024 e as informações estão coerentes.')
    st.pyplot(fig=fig_cloud, use_container_width=True)

    # GRÁFICO DE BARRAS SOBRE A OCUPAÇÃO DOS CANDIDATOS - RANK
    ocupacao = candidatos_20_24.groupby(
        ['Ano de eleição', 'Ocupação'], observed=False).agg(count=('Ocupação', 'size'))
    ocupacao_2020 = ocupacao.loc['2020']['count'].rank(
        ascending=False).sort_values()
    ocupacao_2024 = ocupacao.loc['2024']['count'].rank(
        ascending=False).sort_values()
    fig_rank, ax = plt.subplots(1, 2, figsize=(20, 6))

    cores_2020 = ['gold' if i == 0 else 'grey' for i in range(5)]
    cores_2024 = ['gold' if i == 0 else 'grey' for i in range(5)]

    sns.barplot(x=ocupacao_2020.iloc[:5].index.to_list(
    ), y=ocupacao_2020.values[:5][::-1], ax=ax[0], palette=cores_2020, hue=ocupacao_2020.iloc[:5].index.to_list(
    ))
    sns.barplot(x=ocupacao_2024.iloc[:5].index.to_list(
    ), y=ocupacao_2024.values[:5][::-1], ax=ax[1], palette=cores_2024, hue=ocupacao_2024.iloc[:5].index.to_list(
    ))

    ranks = [1, 2, 3, 4, 5]

    ax[0].bar_label(ax[0].containers[0], labels=[1])
    ax[0].bar_label(ax[0].containers[1], labels=[2])
    ax[0].bar_label(ax[0].containers[2], labels=[3])
    ax[0].bar_label(ax[0].containers[3], labels=[4])
    ax[0].bar_label(ax[0].containers[4], labels=[5])
    ax[1].bar_label(ax[1].containers[0], labels=[1])
    ax[1].bar_label(ax[0].containers[1], labels=[2])
    ax[1].bar_label(ax[0].containers[2], labels=[3])
    ax[1].bar_label(ax[0].containers[3], labels=[4])
    ax[1].bar_label(ax[0].containers[4], labels=[5])

    ax[0].set_xticks(range(len(ax[0].get_xticklabels())))
    ax[0].set_xticklabels(ax[0].get_xticklabels(), rotation=45)
    ax[1].set_xticks(range(len(ax[1].get_xticklabels())))
    ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation=45)

    plt.margins(y=0.05)

    fig_rank.suptitle(
        'Profissões mais frequentes entre 2020 e 2024', fontsize=20)
    st.markdown('Nesse momento da análise, foi notado uma diferença de resultados relacionados a esse recorte abaixo. Na matéria do G1, foi abordado que a ocupação mais frequente entre os candidatos era empresário. Contudo, como pode ser observado no gráfico de ranking, a ocupação mais frequente é designada como "OUTROS", o que leva a pensar como questionamento porque a matéria designou "OUTRO" como empresários. Talvez possa ter considerado candidatos que tenham como ocupação um trabalho no modelo de pessoa júridica. Outra tópico importante a ser analisado é que em 2024 temos como 3° lugar servidores públicos municipais pelos dois períodos eleitorais consecutivos, podendo ser feito um mapeamento dessas funções, e como o 5° lugar vereadores, o que indica que muitas pessoas esse ano estão tentando reeleição.')
    st.pyplot(fig=fig_rank, use_container_width=True)

    # GRÁFICO DE BARRAS - FAIXA ETÁRIA
    faixa_etaria = candidatos_20_24.groupby(
        ['Ano de eleição', 'Faixa etária'], observed=False).agg(count=('Faixa etária', 'size'))
    formacao = candidatos_20_24.groupby(['Ano de eleição', 'Grau de instrução'], observed=False).agg(
        count=('Grau de instrução', 'size'))
    fig_idade, ax = plt.subplots(2, 1, figsize=(20, 10))

    sns.barplot(x=faixa_etaria.loc['2020']['count'].index,
                y=faixa_etaria.loc['2020']['count'].values,
                ax=ax[0],
                orient='v')
    sns.barplot(x=faixa_etaria.loc['2024']['count'].index,
                y=faixa_etaria.loc['2024']['count'].values,
                ax=ax[1],
                orient='v')

    for container in ax[0].containers:
        ax[0].bar_label(container)
        ax[0].margins(x=0, y=0.2)
        ax[0].axis("off")

    for container in ax[1].containers:
        ax[1].bar_label(container)
        ax[1].margins(x=0, y=0.2)
        ax[1].set_xticks(range(len(ax[1].get_xticklabels())))
        ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation=45)
    fig_idade.suptitle(
        'Faixas Etárias mais frequentes entre 2020 e 2024', fontsize=20)
    st.markdown('Continuando a checagem, em 2020 temos mais candidatos dentro da faixa etária de "40 a 44 anos" dando espaço em 2024 para a faixa etária de "45 a 49 anos". Na matéria foi feita uma média entre as duas idades do intervalo dizendo que seria 46 anos, redondando para baixo, pois calculando entre as duas temos 47 anos. Pode parecer simples, mas dizer 46 anos como mais frequente sugere que a equipe do G1 envolvida nessa matéria teve acesso às idades dos candidatos e pôde fazer uma mediana dos dados, pois, os dados obtidos para essa análise no site do TSE não mostram os dados de idades como números inteiros, mas como categorias. Só a título de curiosidade.')
    st.pyplot(fig=fig_idade, use_container_width=True)

    # GRÁFICO DE DISPERSÃO DOS DADOS SOBRE ESCOLARIDADE

    fig_scatter, ax = plt.subplots(2, 1, figsize=(20, 10))

    sns.scatterplot(x=formacao.loc['2020']['count'].index,
                    y=formacao.loc['2020']['count'].values,
                    size=formacao.loc['2020']['count'].values,
                    ax=ax[0], sizes=(50, 500), legend='brief')
    sns.scatterplot(x=formacao.loc['2024']['count'].index,
                    y=formacao.loc['2024']['count'].values,
                    size=formacao.loc['2024']['count'].values,
                    ax=ax[1], sizes=(50, 500), legend='brief')
    ax[0].set_xticks(range(len(ax[0].get_xticklabels())))
    ax[0].set_xticklabels(ax[0].get_xticklabels(), rotation=45)
    ax[1].set_xticks(range(len(ax[1].get_xticklabels())))
    ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation=45)

    ax[0].set_xlabel('Grau de Instrução', fontsize=14)
    ax[0].set_ylabel('Contagem de Candidatos', fontsize=14)
    ax[0].margins(x=0.2, y=0.2)
    ax[1].set_xlabel('Grau de Instrução', fontsize=14)
    ax[1].set_ylabel('Contagem de Candidatos', fontsize=14)
    ax[1].margins(x=0.2, y=0.2)

    fig_scatter.suptitle(
        'Distribuição de Formação de Candidatos em 2020 e 2024', fontsize=20)
    fig_scatter.text(
        0.2, 0.85, 'Análise comparativa do \n grau de instrução\n dos candidatos nos anos de 2020 e 2024', fontsize=12, ha='center')

    handles, labels = ax[0].get_legend_handles_labels()
    ax[0].legend(handles, labels, title="Tamanho das Bolhas",
                 bbox_to_anchor=(1.05, 1), loc='upper left', labelspacing=1.5)
    ax[1].legend(handles, labels, title="Tamanho das Bolhas",
                 bbox_to_anchor=(1.05, 1), loc='upper left', labelspacing=1.5)

    fig_scatter.tight_layout()
    st.markdown('Quanto a escolaridade dos candidatos, realmente temos mais registros para "ENSINO MÉDIO COMPLETO" em ambos os anos confirmando os dados dispostos na matéria. Um dado interessante a ser analisado é que o número de pessoas com ensino superior completo teve um aumento, demonstrando uma possível preocupação dos candidatos com aprimoramento técnico.(esperemos)')
    st.pyplot(fig=fig_scatter, use_container_width=True)

    # GRÁFICO DE BARRAS - DIFERENÇA DE REGISTROS POR SIGLA
    fig_siglas = plt.figure(figsize=(20, 10))
    contagem_siglas = candidatos_20_24.groupby(
        ['Ano de eleição', 'Sigla partido'], observed=False).agg(count=('Sigla partido', 'size'))
    contagem_siglas_2020 = contagem_siglas.loc[('2020')]
    contagem_siglas_2024 = contagem_siglas.loc[('2024')]
    contagem_siglas_2020.columns = ['2020']
    contagem_siglas_2024.columns = ['2024']
    diferenca = pd.concat(
        [contagem_siglas_2024, contagem_siglas_2020], axis=1).fillna(0)
    diferenca['diff'] = diferenca['2024'] - diferenca['2020']
    sns.barplot(x=diferenca['diff'],
                y=diferenca.index,
                orient='h',
                palette='viridis',
                hue=diferenca.index)

    plt.xlabel('Contagem da Diferença', fontsize=14)
    plt.ylabel('Partidos Políticos', fontsize=14)
    plt.title('Diferença de Entradas entre 2020 a 2024', fontsize=20)

    st.markdown('Para tornar um pouco mais rica a análise desse relatório, foi produzido esse gráfico mostrando a diferença de registro entre os anos de 2020 e 2024 para as principais siglas de partidos polítcos do pais. Pode ser observado que as siglas que mais tiveram entradas, respectivamente foi SOLIDARIEDADE, PP e PL.')
    st.pyplot(fig=fig_siglas, use_container_width=True)

    # gráfico folium
    st.markdown('Para entender um pouco mais das siglas que tiveram mais registro entre 2020 e 2024. Acesse o gráfico abaixo escolhendo o estado.')

    contagem_estados = candidatos_20_24.groupby(
        ['Ano de eleição', 'UF', 'Sigla partido'], observed=False).agg(count=('UF', 'size'))
    # coordenadas_estados.pop('DF')
    mapa_ufs = folium.Map(
        location=coordenadas_estados['TO'], zoom_start=5, control_scale=True)
    # folium.TileLayer('').add_to(mapa_ufs)
    folium.TileLayer(tiles='https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',
                     attr='<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                     name='CyclOSM').add_to(mapa_ufs)
    folium.LayerControl().add_to(mapa_ufs)

    for i, estado in enumerate(coordenadas_estados):
        coordenada = coordenadas_estados[estado]
        estado = estado
        sigla_max_2020 = contagem_estados.loc[('2020', estado)].idxmax()
        sigla_cont_2020 = contagem_estados.loc[('2020', estado)].max()
        sigla_max_2024 = contagem_estados.loc[('2020', estado)].idxmax()
        sigla_cont_2024 = contagem_estados.loc[('2024', estado)].max()
        total_estado_2020 = contagem_estados.loc[('2020', estado)].sum()
        total_estado_2024 = contagem_estados.loc[('2024', estado)].sum()
        porcentagem_2020 = sigla_cont_2024 / total_estado_2020
        porcentagem_2024 = sigla_cont_2020 / total_estado_2024
        folium.Marker(coordenada,
                      popup=f'O Estado de {estado} teve em 2020 {total_estado_2020.iloc[0]} registros e o partido que teve mais registros foi {sigla_max_2020.iloc[0]} representando {porcentagem_2020.iloc[0]*100:.2f}% do total de registros. Já  em 2024 ocorreram {total_estado_2024.iloc[0]} registros e o partido que teve mais registros foi {sigla_max_2024.iloc[0]} representando {porcentagem_2024.iloc[0]*100:.2f}% do total de registros',
                      icon=folium.Icon(icon="glyphicon glyphicon-tasks", prefix="glyphicon")).add_to(mapa_ufs)
    st_folium(mapa_ufs, use_container_width=True)

    st.markdown('# Conclusão')
    st.text('A matéria do G1 apresentou os dados de acordo com a realidade deles, contudo, pode-se perceber alguns viéses, provalvemente fruto da própria pauta editoral. Algumas outras insights desse projeto vão estar dispostos dentro do reposítorio do github e da apresentação em vídeo do autor do projeto. Foi de escolha do autor se manter nesse momento dentro da checagem de fatos e dados da matéria jornalística, mas está aberto a quaisquer contribuições, insights e colaborações para tornar esse projeto cada vez mais rica para as próximas eleições.')
