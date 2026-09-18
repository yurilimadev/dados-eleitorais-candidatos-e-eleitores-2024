# Dados Eleitorais (TSE)

Aplicativo Streamlit que apresenta perfis descritivos de candidatos e eleitores de eleições brasileiras a partir de dados públicos do TSE.

## Language

**Eleição**:
Um pleito identificado por ano, tipo (municipal ou federal) e cargos em disputa.
_Avoid_: "dados de 2024", pleito

**Tipo de eleição**:
Municipal ou federal — dimensão que define cargos e escopo dos dados de uma Eleição.
_Avoid_: nível, esfera

**Perfil**:
Recorte analítico de um conjunto de dados eleitorais — Perfil de Candidatos ou Perfil de Eleitores.
_Avoid_: página, relatório, análise

**Registro de eleições**:
Catálogo das Eleições conhecidas (ano, tipo, cargos, arquivos de origem) usado pela Ingestão.
_Avoid_: config, lista de arquivos

**Ingestão**:
Module que transforma arquivos brutos do TSE em DataFrames prontos para os Perfis.
_Avoid_: leitura, loader, camada de dados

**Cálculo**:
Funções puras sobre DataFrames que produzem as agregações usadas pelos Perfis (contagens, rankings, diferenças entre anos, resumo por UF).
_Avoid_: camada analítica, transformações

**Localidade**:
UF brasileira ou município estrangeiro (ZZ) com coordenadas conhecidas para o mapa.
_Avoid_: cidade, estado

**RAE**:
Registro de Alistamento Eleitoral — base mensal do TSE que alimenta o Perfil de Eleitores.
