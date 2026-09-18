import pandas as pd


def contagem(df, dimensoes):
    """Total de registros por combinação de dimensões (coluna 'count')."""
    dimensoes = list(dimensoes)
    coluna_contagem = dimensoes[-1]
    g = df.groupby(dimensoes, observed=False).agg(count=(coluna_contagem, 'size'))
    return g.reset_index()


def contagem_por_ano(df, dimensao):
    """Contagem de registros por dimensão, com uma coluna por 'Ano de eleição'."""
    g = df.groupby(['Ano de eleição', dimensao], observed=False).size()
    return g.unstack('Ano de eleição')


def ranking(df, dimensao, ano, n=5):
    """Top n registros mais frequentes de uma dimensão em um ano, do 1º ao n."""
    contagens = contagem_por_ano(df, dimensao)[ano]
    return contagens.sort_values(ascending=False, kind='stable').head(n)


def diferenca_entre_anos(df, dimensao, ano_recente, ano_anterior):
    """Diferença de registros por dimensão entre dois anos.

    Devolve DataFrame indexado pela dimensão com colunas
    [str(ano_anterior), str(ano_recente), 'diff'].
    """
    tab = contagem_por_ano(df, dimensao)
    resultado = pd.DataFrame({
        str(ano_anterior): tab[ano_anterior],
        str(ano_recente): tab[ano_recente],
    }).fillna(0)
    resultado['diff'] = resultado[str(ano_recente)] - resultado[str(ano_anterior)]
    return resultado


def resumo_por_uf(df):
    """Resumo por UF e ano: total de registros, partido com mais registros,
    sua contagem e o percentual sobre o total do mesmo ano.

    Corrige os bugs antigos do mapa: o máximo de 2024 era calculado sobre os
    dados de 2020 e os percentuais usavam o numerador do outro ano.
    """
    g = contagem(df, ['Ano de eleição', 'UF', 'Sigla partido'])
    linhas = []
    for (ano, uf), sub in g.groupby(['Ano de eleição', 'UF']):
        idx = sub['count'].idxmax()
        melhor = sub.loc[idx]
        total = int(sub['count'].sum())
        linhas.append({
            'Ano de eleição': int(ano),
            'UF': uf,
            'total': total,
            'sigla_max': melhor['Sigla partido'],
            'cont_max': int(melhor['count']),
            'pct': melhor['count'] / total,
        })
    return pd.DataFrame(linhas)


def agregar_registros_rae(rae):
    """Agrupa o RAE por mês, UF, município e perfil, contando os grupos de
    registro (mesma agregação do relatório de eleitores, coluna renomeada
    de 'sum' para 'total_registros' para descrever o que ela calcula)."""
    return rae.groupby(
        ['DT_GERACAO_MES',
         'SG_UF',
         'NM_MUNICIPIO',
         'DS_GENERO',
         'DS_ESTADO_CIVIL',
         'DS_FAIXA_ETARIA',
         'DS_GRAU_ESCOLARIDADE',
         'DS_TIPO_OPERACAO'],
        observed=True,
        as_index=False).agg(total_registros=('QT_RAE', 'size'))


def contagem_por_municipio(rae):
    """Contagem de registros do RAE por (SG_UF, NM_MUNICIPIO)."""
    return rae.groupby(['SG_UF', 'NM_MUNICIPIO'], observed=True).size()
