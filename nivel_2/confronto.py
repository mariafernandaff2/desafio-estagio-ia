import json
from pathlib import Path

import pandas as pd


PASTA_OUTPUTS = (
    Path(__file__).resolve().parent.parent
    / "outputs"
)


ORDEM_RISCO = {
    "baixo": 0,
    "médio": 1,
    "alto": 2
}


def classificar_risco_deterministico(
    sinalizacoes_regra_1,
    sinalizacoes_regra_2
):
    regra_1 = sinalizacoes_regra_1 > 0
    regra_2 = sinalizacoes_regra_2 > 0

    if regra_1 and regra_2:
        return "alto"

    if regra_1 or regra_2:
        return "médio"

    return "baixo"


def carregar_resultados():
    resultados = []

    caminhos = PASTA_OUTPUTS.glob(
        "nivel_2_CLI-*.json"
    )

    for caminho in caminhos:
        with open(
            caminho,
            "r",
            encoding="utf-8"
        ) as arquivo:
            resultados.append(
                json.load(arquivo)
            )

    return resultados


def gerar_confronto():
    resultados = carregar_resultados()

    registros = []

    for resultado in resultados:
        regras = resultado[
            "regras_deterministicas"
        ]

        risco_deterministico = (
            classificar_risco_deterministico(
                regras[
                    "sinalizacoes_regra_1"
                ],
                regras[
                    "sinalizacoes_regra_2"
                ]
            )
        )

        risco_agente = resultado[
            "parecer"
        ]["nivel_risco"]

        concorda = (
            risco_agente
            == risco_deterministico
        )

        diferenca_niveis = (
            ORDEM_RISCO[risco_agente]
            - ORDEM_RISCO[risco_deterministico]
        )

        registros.append({
            "cliente_id": resultado["cliente_id"],
            "sinalizacoes_regra_1": regras[
                "sinalizacoes_regra_1"
            ],
            "sinalizacoes_regra_2": regras[
                "sinalizacoes_regra_2"
            ],
            "risco_deterministico": (
                risco_deterministico
            ),
            "risco_agente": risco_agente,
            "concorda": concorda,
            "diferenca_niveis": diferenca_niveis,
            "justificativa_agente": resultado[
                "parecer"
            ]["justificativa"]
        })

    confronto = pd.DataFrame(registros)

    if confronto.empty:
        raise ValueError(
            "Nenhum resultado foi encontrado."
        )

    taxa_concordancia = (
        confronto["concorda"].mean()
    )

    resumo = {
        "criterio": (
            "Risco alto quando as duas regras "
            "sinalizam; médio quando apenas uma "
            "regra sinaliza; baixo quando nenhuma "
            "regra sinaliza."
        ),
        "quantidade_clientes": int(
            len(confronto)
        ),
        "quantidade_concordancias": int(
            confronto["concorda"].sum()
        ),
        "quantidade_divergencias": int(
            (~confronto["concorda"]).sum()
        ),
        "taxa_concordancia": round(
            float(taxa_concordancia),
            4
        )
    }

    confronto.to_csv(
        PASTA_OUTPUTS
        / "nivel_2_confronto.csv",
        index=False
    )

    with open(
        PASTA_OUTPUTS
        / "nivel_2_confronto_resumo.json",
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            resumo,
            arquivo,
            ensure_ascii=False,
            indent=2
        )

    return confronto, resumo