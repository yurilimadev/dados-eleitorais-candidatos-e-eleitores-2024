import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

from dados_eleitorais import calculo, localidades
from dados_eleitorais import carregar_eleitores


@st.cache_data
def _dados_eleitores():
    return carregar_eleitores()


def app_eleitores():

    rae_24 = _dados_eleitores()
    dados_agrupados = calculo.agregar_registros_rae(rae_24)

    st.title('Dados Eleitorais - Eleitores - 2024')
    st.subheader("""Tem curisiodade para saber as características principais dos eleitores brasileiros? Ao lado tem filtros para você saber os valores mais frequentes relacionados a sua cidade ou estado.""")

    container_oculto = st.container()

    def filtrar_opcoes(df, filtro_mes=None, filtro_uf=None):
        if filtro_mes:
            df = df[df['DT_GERACAO_MES'] == filtro_mes]
        if filtro_uf:
            df = df[df['SG_UF'] == filtro_uf]
        if filtro_mes and filtro_uf:
            df = df[(df['SG_UF'] == filtro_uf) & (
                df['DT_GERACAO_MES'] == filtro_mes)]
        return df

    with st.sidebar:

        st.title('Menu')
        st.write('Escolha uma opção abaixo')

        mes = st.selectbox(
            'Mês', dados_agrupados['DT_GERACAO_MES'].unique(), index=None, placeholder="Selecione o Mês...")
        df_filtrado_mes = filtrar_opcoes(dados_agrupados, filtro_mes=mes)
        uf = st.selectbox(
            'UF', df_filtrado_mes['SG_UF'].unique(), index=None, placeholder="Selecione o Estado...")
        df_filtrado_uf = filtrar_opcoes(
            df_filtrado_mes, filtro_mes=mes, filtro_uf=uf)
        municipio = st.selectbox(
            'Munícipio', df_filtrado_uf['NM_MUNICIPIO'].unique(), index=None, placeholder="Selecione o Município...")

        col3, col4 = st.columns(2, gap='small')
        with col3:
            if st.button('Filtrar', type='primary', use_container_width=True):
                with container_oculto:
                    if mes and uf and municipio:
                        # Filtra pelos três critérios: mês, UF e município
                        data_filtrada = dados_agrupados[
                            (dados_agrupados['DT_GERACAO_MES'] == mes) &
                            (dados_agrupados['SG_UF'] == uf) &
                            (dados_agrupados['NM_MUNICIPIO'] == municipio)
                        ]
                    elif mes and uf:
                        # Filtra pelos critérios: mês e UF
                        data_filtrada = dados_agrupados[
                            (dados_agrupados['DT_GERACAO_MES'] == mes) &
                            (dados_agrupados['SG_UF'] == uf)
                        ]
                    elif mes and municipio:
                        # Filtra pelos critérios: mês e município
                        data_filtrada = dados_agrupados[
                            (dados_agrupados['DT_GERACAO_MES'] == mes) &
                            (dados_agrupados['NM_MUNICIPIO'] == municipio)
                        ]
                    elif uf and municipio:
                        # Filtra pelos critérios: UF e município
                        data_filtrada = dados_agrupados[
                            (dados_agrupados['SG_UF'] == uf) &
                            (dados_agrupados['NM_MUNICIPIO'] == municipio)
                        ]
                    elif mes:
                        # Filtra apenas pelo critério: mês
                        data_filtrada = dados_agrupados[dados_agrupados['DT_GERACAO_MES'] == mes]
                    elif uf:
                        # Filtra apenas pelo critério: UF
                        data_filtrada = dados_agrupados[dados_agrupados['SG_UF'] == uf]
                    elif municipio:
                        # Filtra apenas pelo critério: município
                        data_filtrada = dados_agrupados[dados_agrupados['NM_MUNICIPIO'] == municipio]

                    tabela = pd.DataFrame({
                        'Mês': [data_filtrada['DT_GERACAO_MES'].value_counts().idxmax()],
                        'UF': [data_filtrada['SG_UF'].value_counts().idxmax()],
                        'Munícipio': [data_filtrada['NM_MUNICIPIO'].value_counts().idxmax()],
                        'Gênero': [data_filtrada['DS_GENERO'].value_counts().idxmax()],
                        'Estado Civil': [data_filtrada['DS_ESTADO_CIVIL'].value_counts().idxmax()],
                        'Escolaridade': [data_filtrada['DS_GRAU_ESCOLARIDADE'].value_counts().idxmax()],
                        'Operação': [data_filtrada['DS_TIPO_OPERACAO'].value_counts().idxmax()]
                    })

                    st.session_state.data_filtrada = tabela

                    data_agrupada = data_filtrada.groupby(
                        'DS_TIPO_OPERACAO', as_index=False).agg({'total_registros': 'sum'})
                    st.session_state.titulo_bar = st.title(
                        'Total de Registros Por Operação Filtrados')
                    st.session_state.fig_bar = st.bar_chart(data_agrupada,
                                                            x='DS_TIPO_OPERACAO',
                                                            y='total_registros',
                                                            color='DS_TIPO_OPERACAO',
                                                            use_container_width=True)
        with col4:
            if st.button('Limpar'):
                st.session_state.data_filtrada = None
                st.session_state.fig_bar = None
                st.session_state.titulo_bar = None

    with container_oculto:

        if 'data_filtrada' not in st.session_state:
            st.session_state.data_filtrada = None
        if st.session_state.data_filtrada is not None:
            st.dataframe(st.session_state.data_filtrada,
                         use_container_width=True)
        else:
            st.caption(
                "Escolha os filtros de Mês, Estado e Cidade no Menu ao Lado.")

        if 'fig_bar' not in st.session_state and 'titulo_bar' not in st.session_state:
            st.session_state.fig_bar = None
            st.session_state.titulo_bar = None
        st.session_state.titulo_bar = st.session_state.titulo_bar
        st.session_state.fig_bar = st.session_state.fig_bar

    contagem_uf_municipio = calculo.contagem_por_municipio(rae_24)
    if 'ZZ' in contagem_uf_municipio.index.get_level_values(0):
        contagem_zz = contagem_uf_municipio.loc['ZZ']
    else:
        contagem_zz = pd.Series(dtype=int)

    mapa_ufs = folium.Map(
        location=localidades.COORDENADAS_UF['TO'], zoom_start=5, control_scale=True)
    folium.TileLayer(tiles='https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',
                     attr='<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                     name='CyclOSM').add_to(mapa_ufs)
    folium.LayerControl().add_to(mapa_ufs)

    for cidade, coordenada in localidades.CIDADES_ZZ.items():
        registros = int(contagem_zz.get(cidade, 0))
        folium.Marker(coordenada,
                      popup=f'{cidade} tem {registros} registros',
                      icon=folium.Icon(icon="glyphicon glyphicon-tasks", prefix="glyphicon")).add_to(mapa_ufs)
    st.header('Distribuição Geográfica dos Eleitores Ao Redor do Mundo')
    st_folium(mapa_ufs, height=500, width=1920)
