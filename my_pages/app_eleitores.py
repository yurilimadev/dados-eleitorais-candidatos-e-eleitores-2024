import streamlit as st
import pandas as pd
import folium
import os
from streamlit_folium import st_folium


# Carregando Dados Utilizados

cidades_zz = {'amsterdam': ['52.3730796', '4.8924534'],
              'amman': ['31.9515694', '35.9239625'],
              'asuncion': ['-25.2800459', '-57.6343814'],
              'atlanta': ['33.7489924', '-84.3902644'],
              'barcelona': ['41.3828939', '2.1774322'],
              'beirut': ['33.88922645', '35.50255852895232'],
              'berlin': ['52.5170365', '13.3888599'],
              'boston': ['42.3554334', '-71.060511'],
              'brussels': ['50.8465573', '4.351697'],
              'buenos_aires': ['-34.6037181', '-58.38153'],
              'guangzhou': ['23.1301964', '113.2592945'],
              'chicago': ['41.8755616', '-87.6244212'],
              'ciudad_del_este': ['-25.5169015', '-54.6168645'],
              'copenhagen': ['55.6867243', '12.5700724'],
              'dublin': ['53.3493795', '-6.2605593'],
              'stockholm': ['59.3251172', '18.0710935'],
              'faro': ['37.0162727', '-7.9351771'],
              'frankfurt': ['50.1106444', '8.6820917'],
              'geneva': ['46.2017559', '6.1466014'],
              'hamamatsu': ['34.7109786', '137.7259431'],
              'hartford': ['41.764582', '-72.6908547'],
              'houston': ['29.7589382', '-95.3676974'],
              'lisbon': ['38.7077507', '-9.1365919'],
              'london': ['51.5074456', '-0.1277653'],
              'los_angeles': ['34.0536909', '-118.242766'],
              'madrid': ['40.4167047', '-3.7035825'],
              'marseille': ['43.2961743', '5.3699525'],
              'muscat': ['23.5882019', '58.3829448'],
              'miami': ['25.7741728', '-80.19362'],
              'milan': ['45.4641943', '9.1896346'],
              'montreal': ['45.5031824', '-73.5698065'],
              'munich': ['48.1371079', '11.5753822'],
              'nagoya': ['35.1851045', '136.8998438'],
              'new_york': ['40.7127281', '-74.0060152'],
              'orlando': ['28.5421109', '-81.3790304'],
              'paris': ['48.8588897', '2.3200410217200766'],
              'porto': ['41.1494512', '-8.6107884'],
              'puerto_iguazu': ['-25.6346782', '-54.58287530604622'],
              'ramallah': ['31.9030543', '35.1952255'],
              'rio_branco': ['-9.9765362', '-67.8220778'],
              'rome': ['41.8933203', '12.4829321'],
              'santa_cruz_de_la_sierra': ['-17.7834936', '-63.1820853'],
              'santiago': ['9.8694792', '-83.7980749'],
              'sydney': ['-33.8698439', '151.2082848'],
              'santo_domingo': ['18.4801972', '-69.942111'],
              'san_francisco': ['37.7792588', '-122.4193286'],
              'san_jose': ['37.3361663', '-121.890591'],
              'tel_aviv': ['32.0852997', '34.7818064'],
              'toronto': ['43.6534817', '-79.3839347'],
              'tokyo': ['35.6821936', '139.762221'],
              'vancouver': ['49.2608724', '-123.113952'],
              'vienna': ['48.2083537', '16.3725042'],
              'washington': ['38.8950368', '-77.0365427'],
              'wellington': ['-41.2887953', '174.7772114'],
              'zurich': ['47.3744489', '8.5410422'],
              'abu_dhabi': ['24.4538352', '54.3774014'],
              'bogota': ['4.6533816', '-74.0836333'],
              'cayenne': ['4.9371544', '-52.3258736'],
              'mexico_city': ['19.4326296', '-99.1331785'],
              'paramaribo': ['5.8247628', '-55.1703941'],
              'salto_del_guaira': ['-24.0616604', '-54.305644'],
              'athens': ['37.9755648', '23.7348324'],
              'bangkok': ['13.7524938', '100.4935089'],
              'cairo': ['30.0443879', '31.2357257'],
              'cape_town': ['-33.928992', '18.417396'],
              'cordoba': ['-31.4166867', '-64.1834193'],
              'damascus': ['33.5130695', '36.3095814'],
              'oslo': ['59.9133301', '10.7389701'],
              'pretoria': ['-25.7459277', '28.1879101'],
              'edinburgh': ['55.9533456', '-3.1883749'],
              'la_paz': ['-16.4955455', '-68.1336229'],
              'ljubljana': ['46.0500268', '14.5069289'],
              'luanda': ['-8.8272699', '13.2439512'],
              'montevideo': ['-34.9058916', '-56.1913095'],
              'ottawa': ['45.4208777', '-75.6901106'],
              'panama_city': ['8.9714493', '-79.5341802'],
              'pedro_juan_caballero': ['-22.5497781', '-55.7384312'],
              'prague': ['50.0596288', '14.446459273258009'],
              'taipei': ['25.0375198', '121.5636796'],
              'canberra': ['-35.2975906', '149.1012676'],
              'cochabamba': ['-17.401245799999998', '-66.16756808852'],
              'doha': ['25.2856329', '51.5264162'],
              'maputo': ['-25.966213', '32.56745'],
              'mumbai': ['19.08157715', '72.88662753964906'],
              'hong_kong': ['22.2793278', '114.1628131'],
              'praia': ['14.9162811', '-23.5095095'],
              'shanghai': ['31.2323437', '121.4691024'],
              'helsinki': ['60.1674881', '24.9427473'],
              'lima': ['-12.0621065', '-77.0365256'],
              'rabat': ['34.02236', '-6.8340222'],
              'seoul': ['37.5666791', '126.9782914'],
              'abidjan': ['5.320357', '-4.016107'],
              'budapest': ['47.4978789', '19.0402383'],
              'nicosia': ['35.1746503', '33.3638783'],
              'singapore': ['1.357107', '103.8194992'],
              'bucharest': ['44.4361414', '26.1027202'],
              'quito': ['-0.2201641', '-78.5123274'],
              'kingston': ['17.9712148', '-76.7928128'],
              'warsaw': ['52.2319581', '21.0067249'],
              'guatemala_city': ['14.6424667', '-90.5131361'],
              'encarnacion': ['-27.3376114', '-55.8669492'],
              'istanbul': ['41.006381', '28.9758715'],
              'georgetown': ['6.8137426', '-58.1624465'],
              'manila': ['14.5906346', '120.9799964'],
              'kuala_lumpur': ['3.1516964', '101.6942371'],
              'belgrade': ['44.8178131', '20.4568974'],
              'managua': ['12.1544035', '-86.2737642'],
              'caracas': ['10.5060934', '-66.9146008'],
              'ciudad_guayana': ['8.3223763', '-62.6896622'],
              'moscow': ['55.7505412', '37.6174782'],
              'tunis': ['33.8439408', '9.400138'],
              'tallinn': ['59.4372155', '24.7453688'],
              'bratislava': ['48.1516988', '17.1093063'],
              'riyadh': ['24.638916', '46.7160104'],
              'san_salvador': ['13.6989939', '-89.1914249'],
              'paso_de_los_libres': ['-29.7136574', '-57.0861369'],
              'sofia': ['42.6977028', '23.3217359'],
              'zagreb': ['45.84264135', '15.962231476593626'],
              'bissau': ['11.861324', '-15.583055'],
              'lagos': ['6.4550575', '3.3941795'],
              'new_delhi': ['28.6138954', '77.2090057'],
              'jakarta': ['-6.175247', '106.8270488'],
              'bamako': ['12.61326555', '-7.984739136241295'],
              'nairobi': ['-1.2832533', '36.8172449'],
              'mendoza': ['-34.787093049999996', '-68.43818677312292'],
              'addis_ababa': ['9.0358287', '38.7524127'],
              'puerto_quijarro': ['-19.0044088', '-57.7157091'],
              'concepcion': ['-36.8270795', '-73.0502399'],
              'algiers': ['36.7729323', '3.0588397'],
              'castries': ['43.6779101', '3.9868904'],
              'kathmandu': ['27.708317', '85.3205817'],
              'baghdad': ['33.3061701', '44.3872213'],
              'ankara': ['39.9207759', '32.8540497'],
              'chuy': ['42.55502355', '74.62199103571582'],
              'beijing': ['39.9057136', '116.3912972'],
              'windhoek': ['-22.5776104', '17.0772739'],
              'AC': [-8.77, -70.55],
              'AL': [-9.71, -35.73],
              'AM': [-3.07, -61.66],
              'AP': [1.41, -51.77],
              'BA': [-12.96, -38.51],
              'CE': [-3.71, -38.54],
              'DF': [-15.83, -47.86],
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
              'TO': [-10.25, -48.25]}


dtypes_dict_rae = {
    'DT_GERACAO': 'category',
    'HH_GERACAO': 'category',
    'NR_ANO_REGISTRO': 'int16',
    'NR_MES_REGISTRO': 'int16',
    'SG_UF': 'category',
    'CD_MUNICIPIO': 'int16',
    'NM_MUNICIPIO': 'category',
    'NR_ZONA': 'int16',
    'CD_TIPO_OPERACAO': 'int16',
    'DS_TIPO_OPERACAO': 'category',
    'CD_GENERO': 'int16',
    'DS_GENERO': 'category',
    'CD_ESTADO_CIVIL': 'int16',
    'DS_ESTADO_CIVIL': 'category',
    'CD_FAIXA_ETARIA': 'int16',
    'DS_FAIXA_ETARIA': 'category',
    'CD_GRAU_ESCOLARIDADE': 'int16',
    'DS_GRAU_ESCOLARIDADE': 'category',
    'QT_RAE': 'int16'
}

rae_24 = pd.read_csv('perfil_rae_2024.csv',
                     sep=';',
                     encoding='latin-1',
                     dtype=dtypes_dict_rae, decimal=',')

# Alguns tratamentos

rae_24['DT_GERACAO'] = pd.to_datetime(rae_24['DT_GERACAO'].apply(
    lambda x: x.replace('/', '-')), dayfirst=True)
rae_24['DT_GERACAO_MES'] = rae_24['DT_GERACAO'].apply(lambda x: x.month)

dados_agrupados = rae_24.groupby(['DT_GERACAO_MES',
                                  'SG_UF',
                                  'NM_MUNICIPIO',
                                  'DS_GENERO',
                                  'DS_ESTADO_CIVIL',
                                  'DS_FAIXA_ETARIA',
                                  'DS_GRAU_ESCOLARIDADE', 'DS_TIPO_OPERACAO'], observed=True, as_index=False).agg(sum=('QT_RAE', 'size'))

# Criando o layout


def app_eleitores():

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
                        'DS_TIPO_OPERACAO', as_index=False).agg({'sum': 'sum'})
                    data_agrupada = data_agrupada.rename(
                        columns={'sum': 'Total'})
                    st.session_state.titulo_bar = st.title(
                        'Total de Registros Por Operação Filtrados')
                    st.session_state.fig_bar = st.bar_chart(data_agrupada,
                                                            x='DS_TIPO_OPERACAO',
                                                            y='Total',
                                                            color='DS_TIPO_OPERACAO',
                                                            use_container_width=True)
        with col4:
            if st.button('Limpar'):
                st.session_state.data_filtrada = None
                st.session_state.fig_bar = None
                st.session_state.titulo_bar = None

    # st.markdown(
    #     """
    #     <style>
    #     .container {
    #         display: flex;
    #         flex-direction: column;
    #         align-items: center;
    #         justify-content: center;
    #     }
    #     .container > div {
    #         margin: 10px;
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )

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

    contagem_estados = rae_24.groupby(['SG_UF', 'NM_MUNICIPIO'], observed=True)[
        ['NM_MUNICIPIO']].count()
    cidades_uf_zz = contagem_estados.loc[("ZZ")]

    mapa_ufs = folium.Map(
        location=cidades_zz['TO'], zoom_start=5, control_scale=True)
    # folium.TileLayer('').add_to(mapa_ufs)
    folium.TileLayer(tiles='https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',
                     attr='<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                     name='CyclOSM').add_to(mapa_ufs)
    folium.LayerControl().add_to(mapa_ufs)

    for i, estado in enumerate(cidades_zz):
        coordenada = cidades_zz[estado]
        estado = estado
        folium.Marker(coordenada,
                      popup=f'{estado} tem {contagem_estados.iloc[i].values[0]} registros',
                      icon=folium.Icon(icon="glyphicon glyphicon-tasks", prefix="glyphicon")).add_to(mapa_ufs)
    st.header('Distribuição Geográfica dos Eleitores Ao Redor do Mundo')
    st_folium(mapa_ufs, height=500, width=1920)
