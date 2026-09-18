from pathlib import Path

import pandas as pd

# Convenções de arquivos do TSE: separador ponto-e-vírgula, codificação Latin-1
# e vírgula como decimal.
CSV_TSE = {
    'sep': ';',
    'encoding': 'latin-1',
    'decimal': ',',
}

# Diretório padrão dos arquivos de dados: raiz do repositório.
_BASE_PADRAO = Path(__file__).resolve().parent.parent

# Registro de eleições: nova eleição (municipal ou federal) é uma nova entrada
# aqui. As páginas e os testes não precisam saber nomes de arquivos.
ELEICOES = {
    2020: {
        'tipo': 'municipal',
        'cargos': ('Vereador', 'Prefeito'),
        'arquivos': ('candidatos_2020.csv',),
    },
    2024: {
        'tipo': 'municipal',
        'cargos': ('Vereador', 'Prefeito'),
        'arquivos': ('candidatos_2024.csv',),
    },
}

DTYPES_CANDIDATOS = {
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
    'Data de carga': 'category',
}

DTYPES_ELEITORES = {
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
    'QT_RAE': 'int16',
}


def _ler_csv(caminho, dtypes, contexto):
    df = pd.read_csv(caminho, dtype=dtypes, **CSV_TSE)
    faltando = [coluna for coluna in dtypes if coluna not in df.columns]
    if faltando:
        raise ValueError(
            f'Colunas ausentes em {caminho.name} ({contexto}): {faltando}. '
            'O schema do arquivo diverge do esperado pela Ingestão.'
        )
    return df


def _selecionar_eleicoes(anos=None, tipo_eleicao=None):
    tipos_disponiveis = sorted({eleicao['tipo'] for eleicao in ELEICOES.values()})
    if tipo_eleicao is not None and tipo_eleicao not in tipos_disponiveis:
        raise ValueError(
            f'Tipo de eleição desconhecido: {tipo_eleicao!r}. '
            f'Disponíveis: {tipos_disponiveis}'
        )

    anos_disponiveis = sorted(ELEICOES)
    if anos is None:
        selecionadas = list(ELEICOES)
    else:
        faltando = [ano for ano in anos if ano not in ELEICOES]
        if faltando:
            raise ValueError(
                f'Eleições não catalogadas no registro: {faltando}. '
                f'Disponíveis: {anos_disponiveis}. '
                'Para suportar uma nova eleição, adicione uma entrada em ELEICOES.'
            )
        selecionadas = list(anos)

    if tipo_eleicao is not None:
        selecionadas = [
            ano for ano in selecionadas
            if ELEICOES[ano]['tipo'] == tipo_eleicao
        ]
    if not selecionadas:
        raise ValueError(
            f'Nenhuma eleição no registro para tipo={tipo_eleicao!r}. '
            f'Disponíveis: {anos_disponiveis}'
        )
    return sorted(selecionadas)


def carregar_candidatos(anos=None, tipo_eleicao=None, base_dir=None):
    """Carrega os registros de candidatos das Eleições do registro.

    anos: lista de anos a carregar (None = todas as Eleições catalogadas).
    tipo_eleicao: 'municipal' ou 'federal' (None = todos os tipos).
    base_dir: pasta onde ficam os arquivos (padrão: raiz do repositório;
    os testes apontam para fixtures sintéticas).

    Devolve um único DataFrame com 'Ano de eleição' convertido para inteiro.
    """
    raiz = Path(base_dir) if base_dir is not None else _BASE_PADRAO
    dfs = []
    for ano in _selecionar_eleicoes(anos, tipo_eleicao):
        for nome in ELEICOES[ano]['arquivos']:
            df = _ler_csv(raiz / nome, DTYPES_CANDIDATOS, f'candidatos {ano}')
            df['Ano de eleição'] = df['Ano de eleição'].astype('int16')
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


def carregar_eleitores(base_dir=None):
    """Carrega a base RAE (Perfil de Eleitores) já tratada.

    Adiciona 'DT_GERACAO' como data e 'DT_GERACAO_MES' como mês (int).
    """
    raiz = Path(base_dir) if base_dir is not None else _BASE_PADRAO
    df = _ler_csv(raiz / 'perfil_rae_2024.csv', DTYPES_ELEITORES, 'eleitores (RAE)')
    df['DT_GERACAO'] = pd.to_datetime(
        df['DT_GERACAO'].str.replace('/', '-'), dayfirst=True)
    df['DT_GERACAO_MES'] = df['DT_GERACAO'].dt.month
    return df
