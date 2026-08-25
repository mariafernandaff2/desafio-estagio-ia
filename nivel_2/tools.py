import json
from pathlib import Path

import pandas as pd


CAMINHO_DADOS = (
    Path(__file__).resolve().parent.parent
    / "dados"
    / "dados_nivel_2.json"
)


def _carregar_e_tratar_dados():
    """
    Carrega e normaliza a base do Nível 2.

    O sublinhado indica que esta é uma função interna,
    usada pelas ferramentas.
    """

    with open(
        CAMINHO_DADOS,
        "r",
        encoding="utf-8"
    ) as arquivo:
        dados = json.load(arquivo)

    taxa_cambio_usd_brl = float(
        dados["taxa_cambio_usd_brl"]
    )

    df = pd.DataFrame(dados["operacoes"])

    df = df.drop_duplicates().copy()

    df["data"] = pd.to_datetime(
        df["data"],
        errors="coerce"
    )

    df["data_ausente"] = df["data"].isna()

    for coluna in ["canal", "tipo"]:
        df[coluna] = (
            df[coluna]
            .astype("string")
            .str.strip()
            .str.lower()
        )

    df["moeda"] = (
        df["moeda"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    df["valor"] = pd.to_numeric(
        df["valor"],
        errors="coerce"
    )

    df["valor_brl"] = df["valor"]

    mascara_usd = df["moeda"] == "USD"

    df.loc[mascara_usd, "valor_brl"] = (
        df.loc[mascara_usd, "valor"]
        * taxa_cambio_usd_brl
    )

    return df


df_operacoes = _carregar_e_tratar_dados()


def _validar_cliente(cliente_id):
    clientes_validos = set(
        df_operacoes["cliente_id"].unique()
    )

    if cliente_id not in clientes_validos:
        raise ValueError(
            f"Cliente não encontrado: {cliente_id}"
        )


def historico_cliente(cliente_id):
    """
    Retorna o resumo agregado das operações do cliente.
    """

    _validar_cliente(cliente_id)

    operacoes = df_operacoes[
        df_operacoes["cliente_id"] == cliente_id
    ].copy()

    datas_validas = operacoes["data"].dropna()

    return {
        "cliente_id": cliente_id,
        "quantidade_operacoes": int(len(operacoes)),
        "volume_total_brl": round(
            float(operacoes["valor_brl"].sum()),
            2
        ),
        "valor_medio_brl": round(
            float(operacoes["valor_brl"].mean()),
            2
        ),
        "mediana_brl": round(
            float(operacoes["valor_brl"].median()),
            2
        ),
        "maior_operacao_brl": round(
            float(operacoes["valor_brl"].max()),
            2
        ),
        "primeira_data": (
            datas_validas.min().strftime("%Y-%m-%d")
            if not datas_validas.empty
            else None
        ),
        "ultima_data": (
            datas_validas.max().strftime("%Y-%m-%d")
            if not datas_validas.empty
            else None
        )
    }


def operacoes_do_dia(cliente_id, data):
    """
    Retorna as operações do cliente em uma data específica.
    """

    _validar_cliente(cliente_id)

    data_consulta = pd.to_datetime(
        data,
        errors="coerce"
    )

    if pd.isna(data_consulta):
        raise ValueError(
            f"Data inválida: {data}"
        )

    mascara_cliente = (
        df_operacoes["cliente_id"] == cliente_id
    )

    mascara_data = (
        df_operacoes["data"].dt.normalize()
        == data_consulta.normalize()
    )

    operacoes = df_operacoes[
        mascara_cliente & mascara_data
    ].copy()

    operacoes["data"] = (
        operacoes["data"]
        .dt.strftime("%Y-%m-%d")
    )

    colunas_retorno = [
        "id",
        "data",
        "valor_brl",
        "canal",
        "tipo",
        "contraparte",
        "observacao"
    ]

    operacoes = operacoes[colunas_retorno]

    operacoes = operacoes.where(
        operacoes.notna(),
        None
    )

    return operacoes.to_dict(
        orient="records"
    )


def perfil_canal(cliente_id):
    """
    Retorna a distribuição das operações por canal.
    """

    _validar_cliente(cliente_id)

    operacoes = df_operacoes[
        df_operacoes["cliente_id"] == cliente_id
    ].copy()

    perfil = (
        operacoes
        .groupby(
            "canal",
            dropna=False,
            as_index=False
        )
        .agg(
            quantidade_operacoes=("id", "count"),
            volume_total_brl=("valor_brl", "sum")
        )
    )

    perfil["percentual_operacoes"] = (
        perfil["quantidade_operacoes"]
        / perfil["quantidade_operacoes"].sum()
        * 100
    ).round(2)

    perfil["volume_total_brl"] = (
        perfil["volume_total_brl"].round(2)
    )

    perfil = perfil.where(
        perfil.notna(),
        None
    )

    return perfil.to_dict(
        orient="records"
    )


FERRAMENTAS_DISPONIVEIS = {
    "historico_cliente": historico_cliente,
    "operacoes_do_dia": operacoes_do_dia,
    "perfil_canal": perfil_canal
}