import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import folium
from streamlit_folium import st_folium

from dados_eleitorais import calculo, localidades
from dados_eleitorais import carregar_candidatos


sns.set_theme('notebook')


@st.cache_data
def _dados_candidatos():
    return carregar_candidatos()


def app_candidatos():

    candidatos_20_24 = _dados_candidatos()

    st.title('Dados Eleitorais - Candidatos - 2024')
    st.subheader("""Essa análise contem análise de dados inspirada em uma notícia do G1, a qual fala sobre o perfil geral dos candidatos para eleições municipais de 2024. Esse projeto tem o intuito de fazer um 'checagem de dados' tanto para treinar o pensamento analítico e quando outras habilidades para um futuro profissional estatístico.""")

    # GRÁFICO DE BARRAS MOSTRANDO ÀS DIFERENÇAS DE GÊNERO
    genero = calculo.contagem(candidatos_20_24, ['Ano de eleição', 'Gênero'])
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
    cor_raca = calculo.contagem_por_ano(candidatos_20_24, 'Cor/raça')

    custom_palette_20 = ["#3498db", "#9b59b6", "#2ecc71",
                         "#e74c3c", "#f1c40f", "#9b59b6", "#9b59b6"]
    custom_palette_24 = ["#3498db", "#9b59b6",
                         "#e74c3c", "#f1c40f", "#9b59b6", "#9b59b6"]

    sns.barplot(y=cor_raca[2020].index,
                x=cor_raca[2020].values,
                ax=ax[0],
                palette=custom_palette_20, hue=cor_raca[2020].index)
    sns.barplot(y=cor_raca[2024].index,
                x=cor_raca[2024].values,
                ax=ax[1],
                palette=custom_palette_24, hue=cor_raca[2024].index)

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
    estado_civil = calculo.contagem_por_ano(candidatos_20_24, 'Estado civil')
    counts_2020 = estado_civil[2020].to_dict()
    counts_2024 = estado_civil[2024].to_dict()

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
    ocupacao_2020 = calculo.ranking(candidatos_20_24, 'Ocupação', 2020)
    ocupacao_2024 = calculo.ranking(candidatos_20_24, 'Ocupação', 2024)
    fig_rank, ax = plt.subplots(1, 2, figsize=(20, 6))

    for eixo, top_ocupacoes in zip(ax, [ocupacao_2020, ocupacao_2024]):
        cores = ['gold' if i == 0 else 'grey' for i in range(len(top_ocupacoes))]
        sns.barplot(x=top_ocupacoes.index,
                    y=top_ocupacoes.values,
                    ax=eixo,
                    palette=cores, hue=top_ocupacoes.index)
        eixo.bar_label(eixo.containers[0],
                       labels=list(range(1, len(top_ocupacoes) + 1)))
        eixo.set_xticks(range(len(eixo.get_xticklabels())))
        eixo.set_xticklabels(eixo.get_xticklabels(), rotation=45)

    plt.margins(y=0.05)

    fig_rank.suptitle(
        'Profissões mais frequentes entre 2020 e 2024', fontsize=20)
    st.markdown('Nesse momento da análise, foi notado uma diferença de resultados relacionados a esse recorte abaixo. Na matéria do G1, foi abordado que a ocupação mais frequente entre os candidatos era empresário. Contudo, como pode ser observado no gráfico de ranking, a ocupação mais frequente é designada como "OUTROS", o que leva a pensar como questionamento porque a matéria designou "OUTRO" como empresários. Talvez possa ter considerado candidatos que tenham como ocupação um trabalho no modelo de pessoa júridica. Outra tópico importante a ser analisado é que em 2024 temos como 3° lugar servidores públicos municipais pelos dois períodos eleitorais consecutivos, podendo ser feito um mapeamento dessas funções, e como o 5° lugar vereadores, o que indica que muitas pessoas esse ano estão tentando reeleição.')
    st.pyplot(fig=fig_rank, use_container_width=True)

    # GRÁFICO DE BARRAS - FAIXA ETÁRIA
    faixa_etaria = calculo.contagem_por_ano(candidatos_20_24, 'Faixa etária')
    formacao = calculo.contagem_por_ano(candidatos_20_24, 'Grau de instrução')
    fig_idade, ax = plt.subplots(2, 1, figsize=(20, 10))

    sns.barplot(x=faixa_etaria[2020].index,
                y=faixa_etaria[2020].values,
                ax=ax[0],
                orient='v')
    sns.barplot(x=faixa_etaria[2024].index,
                y=faixa_etaria[2024].values,
                ax=ax[1],
                orient='v')

    for eixo in ax:
        for container in eixo.containers:
            eixo.bar_label(container)
        eixo.margins(x=0, y=0.2)
        eixo.set_xticks(range(len(eixo.get_xticklabels())))
        eixo.set_xticklabels(eixo.get_xticklabels(), rotation=45)
    fig_idade.suptitle(
        'Faixas Etárias mais frequentes entre 2020 e 2024', fontsize=20)
    st.markdown('Continuando a checagem, em 2020 temos mais candidatos dentro da faixa etária de "40 a 44 anos" dando espaço em 2024 para a faixa etária de "45 a 49 anos". Na matéria foi feita uma média entre as duas idades do intervalo dizendo que seria 46 anos, redondando para baixo, pois calculando entre as duas temos 47 anos. Pode parecer simples, mas dizer 46 anos como mais frequente sugere que a equipe do G1 envolvida nessa matéria teve acesso às idades dos candidatos e pôde fazer uma mediana dos dados, pois, os dados obtidos para essa análise no site do TSE não mostram os dados de idades como números inteiros, mas como categorias. Só a título de curiosidade.')
    st.pyplot(fig=fig_idade, use_container_width=True)

    # GRÁFICO DE DISPERSÃO DOS DADOS SOBRE ESCOLARIDADE

    fig_scatter, ax = plt.subplots(2, 1, figsize=(20, 10))

    sns.scatterplot(x=formacao[2020].index,
                    y=formacao[2020].values,
                    size=formacao[2020].values,
                    ax=ax[0], sizes=(50, 500), legend='brief')
    sns.scatterplot(x=formacao[2024].index,
                    y=formacao[2024].values,
                    size=formacao[2024].values,
                    ax=ax[1], sizes=(50, 500), legend='brief')
    for eixo in ax:
        eixo.set_xticks(range(len(eixo.get_xticklabels())))
        eixo.set_xticklabels(eixo.get_xticklabels(), rotation=45)
        eixo.set_xlabel('Grau de Instrução', fontsize=14)
        eixo.set_ylabel('Contagem de Candidatos', fontsize=14)
        eixo.margins(x=0.2, y=0.2)

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
    diferenca = calculo.diferenca_entre_anos(
        candidatos_20_24, 'Sigla partido', 2024, 2020)
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

    resumo_uf_ano = calculo.resumo_por_uf(
        candidatos_20_24).set_index(['UF', 'Ano de eleição'])
    mapa_ufs = folium.Map(
        location=localidades.COORDENADAS_UF['TO'], zoom_start=5, control_scale=True)
    folium.TileLayer(tiles='https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',
                     attr='<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                     name='CyclOSM').add_to(mapa_ufs)
    folium.LayerControl().add_to(mapa_ufs)

    for uf, coordenada in localidades.COORDENADAS_UF.items():
        partes = []
        for ano in (2020, 2024):
            if (uf, ano) in resumo_uf_ano.index:
                linha = resumo_uf_ano.loc[(uf, ano)]
                partes.append(
                    f'em {ano} ocorreram {linha["total"]} registros e o partido que teve mais registros foi {linha["sigla_max"]} representando {linha["pct"]*100:.2f}% do total de registros')
            else:
                partes.append(f'em {ano} não houve registros catalogados')
        popup = (f'O Estado de {uf} teve {partes[0]}. '
                 f'Já  {partes[1]}')
        folium.Marker(coordenada,
                      popup=popup,
                      icon=folium.Icon(icon="glyphicon glyphicon-tasks", prefix="glyphicon")).add_to(mapa_ufs)
    st_folium(mapa_ufs, use_container_width=True)

    st.markdown('# Conclusão')
    st.markdown('A matéria do G1 apresentou os dados de acordo com a realidade deles, contudo, pode-se perceber alguns viéses, provalvemente fruto da própria pauta editoral. Algumas outras insights desse projeto vão estar dispostos dentro do reposítorio do github e da apresentação em vídeo do autor do projeto. Foi de escolha do autor se manter nesse momento dentro da checagem de fatos e dados da matéria jornalística, mas está aberto a quaisquer contribuições, insights e colaborações para tornar esse projeto cada vez mais rica para as próximas eleições.')
