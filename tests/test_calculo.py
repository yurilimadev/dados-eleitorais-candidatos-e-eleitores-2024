from pathlib import Path

import pandas as pd
import pytest

from dados_eleitorais import carregar_candidatos, carregar_eleitores
from dados_eleitorais import calculo

FIXTURES = Path(__file__).parent / 'fixtures'


@pytest.fixture(scope='module')
def candidatos():
    return carregar_candidatos(base_dir=FIXTURES)


@pytest.fixture(scope='module')
def eleitores():
    return carregar_eleitores(base_dir=FIXTURES)


def test_contagem_por_ano(candidatos):
    tab = calculo.contagem_por_ano(candidatos, 'Gênero')
    assert tab.loc['Feminino', 2020] == 2
    assert tab.loc['Masculino', 2024] == 2


def test_ranking_ordem_descendente():
    df = pd.DataFrame({
        'Ano de eleição': [2020, 2020, 2020],
        'Ocupação': ['A', 'B', 'B'],
    })
    top = calculo.ranking(df, 'Ocupação', 2020)
    assert top.index[0] == 'B'
    assert top.index.tolist() == ['B', 'A']


def test_diferenca_entre_anos(candidatos):
    dif = calculo.diferenca_entre_anos(candidatos, 'Sigla partido', 2024, 2020)
    assert dif.loc['PT', 'diff'] == 2
    assert dif.loc['PL', 'diff'] == -1


def test_resumo_por_uf_maximo_do_ano_correto(candidatos):
    """Regressão do bug do mapa: o máximo de 2024 era calculado sobre 2020."""
    resumo = calculo.resumo_por_uf(candidatos).set_index(['UF', 'Ano de eleição'])
    sp_2020 = resumo.loc[('SP', 2020)]
    sp_2024 = resumo.loc[('SP', 2024)]
    assert sp_2020['sigla_max'] == 'PL'
    assert sp_2024['sigla_max'] == 'PT'


def test_resumo_por_uf_percentual_do_ano_correto(candidatos):
    """Regressão do bug dos percentuais trocados entre anos."""
    resumo = calculo.resumo_por_uf(candidatos).set_index(['UF', 'Ano de eleição'])
    sp_2020 = resumo.loc[('SP', 2020)]
    sp_2024 = resumo.loc[('SP', 2024)]
    assert sp_2020['pct'] == pytest.approx(1 / 2)
    assert sp_2024['pct'] == pytest.approx(2 / 3)


def test_resumo_por_uf_totais(candidatos):
    resumo = calculo.resumo_por_uf(candidatos).set_index(['UF', 'Ano de eleição'])
    assert resumo.loc[('SP', 2020), 'total'] == 2
    assert resumo.loc[('SP', 2024), 'total'] == 3


def test_agregar_registros_rae(eleitores):
    agregado = calculo.agregar_registros_rae(eleitores)
    assert 'total_registros' in agregado.columns
    assert agregado['total_registros'].sum() == 3


def test_contagem_por_municipio_zz(eleitores):
    contagem = calculo.contagem_por_municipio(eleitores).loc['ZZ']
    assert contagem['lisbon'] == 1
    assert contagem['miami'] == 1
