from pathlib import Path

import pytest

from dados_eleitorais import carregar_candidatos, carregar_eleitores

FIXTURES = Path(__file__).parent / 'fixtures'


def test_carrega_todas_as_eleicoes_do_registro():
    df = carregar_candidatos(base_dir=FIXTURES)
    assert len(df) == 9
    assert set(df['Ano de eleição'].unique()) == {2020, 2024}
    assert str(df['Ano de eleição'].dtype) == 'int16'


def test_filtra_por_ano():
    df = carregar_candidatos(anos=[2024], base_dir=FIXTURES)
    assert len(df) == 5
    assert set(df['Ano de eleição'].unique()) == {2024}


def test_filtra_por_tipo_de_eleicao():
    df = carregar_candidatos(tipo_eleicao='municipal', base_dir=FIXTURES)
    assert len(df) == 9
    with pytest.raises(ValueError, match='federal'):
        carregar_candidatos(tipo_eleicao='federal', base_dir=FIXTURES)


def test_erro_ano_fora_do_registro_lista_disponiveis():
    with pytest.raises(ValueError, match=r'2020.*2024'):
        carregar_candidatos(anos=[2018], base_dir=FIXTURES)


def test_erro_tipo_desconhecido_lista_disponiveis():
    with pytest.raises(ValueError, match=r"'municipal'"):
        carregar_candidatos(tipo_eleicao='estadual', base_dir=FIXTURES)


def test_erro_schema_divergente_nomeia_a_coluna(tmp_path):
    import pandas as pd
    original = pd.read_csv(FIXTURES / 'candidatos_2024.csv', sep=';',
                           encoding='latin-1')
    original.drop(columns=['Cor/raça']).to_csv(
        tmp_path / 'candidatos_2024.csv', sep=';', encoding='latin-1', index=False)
    with pytest.raises(ValueError, match='Cor/raça'):
        carregar_candidatos(anos=[2024], base_dir=tmp_path)


def test_carregar_eleitores_trata_datas():
    df = carregar_eleitores(base_dir=FIXTURES)
    assert len(df) == 3
    assert list(df['DT_GERACAO_MES'].unique()) == [3]
    assert df['DT_GERACAO'].dt.day.tolist() == [5, 6, 10]


def test_arquivo_ausente_erro_claro(tmp_path):
    with pytest.raises(FileNotFoundError):
        carregar_candidatos(anos=[2024], base_dir=tmp_path)
