import json
import os
import time

from dotenv import load_dotenv
from google import genai

from tools import FERRAMENTAS_DISPONIVEIS


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY não encontrada no arquivo .env."
    )

client = genai.Client(api_key=api_key)

MODELO = "gemini-3.5-flash-lite"


def _converter_json(resposta):
    texto = resposta.text.strip()

    texto = (
        texto
        .removeprefix("```json")
        .removeprefix("```")
        .removesuffix("```")
        .strip()
    )

    return json.loads(texto)


def _extrair_metricas(
    resposta,
    latencia_segundos,
    etapa
):
    uso = getattr(
        resposta,
        "usage_metadata",
        None
    )

    return {
        "etapa": etapa,
        "latencia_segundos": round(
            latencia_segundos,
            3
        ),
        "tokens_entrada": getattr(
            uso,
            "prompt_token_count",
            0
        ) or 0,
        "tokens_saida": getattr(
            uso,
            "candidates_token_count",
            0
        ) or 0,
        "tokens_total": getattr(
            uso,
            "total_token_count",
            0
        ) or 0
    }


def planejar_ferramentas(
    cliente_id,
    alertas_regras
):
    prompt = f"""
Você planeja uma análise preliminar de risco financeiro.

Escolha somente as ferramentas necessárias para analisar o
cliente. Não escolha automaticamente todas as ferramentas.

Ferramentas disponíveis:

1. historico_cliente
Use para consultar quantidade, volume, média, mediana,
maior operação e período analisado.

2. operacoes_do_dia
Use somente quando houver uma data específica relevante
nos alertas determinísticos.

3. perfil_canal
Use quando a distribuição das operações por canal puder
ajudar a avaliar o comportamento.

Cliente:
{cliente_id}

Alertas determinísticos:
{json.dumps(
    alertas_regras,
    ensure_ascii=False,
    indent=2,
    default=str
)}

Responda exclusivamente em JSON válido:

{{
  "ferramentas": [
    {{
      "nome": "nome da ferramenta",
      "data": "YYYY-MM-DD ou null",
      "motivo": "motivo objetivo da escolha"
    }}
  ]
}}
"""

    inicio = time.perf_counter()

    resposta = client.models.generate_content(
        model=MODELO,
        contents=prompt
    )

    latencia = (
        time.perf_counter() - inicio
    )

    plano = _converter_json(resposta)

    metricas = _extrair_metricas(
        resposta=resposta,
        latencia_segundos=latencia,
        etapa="planejamento"
    )

    return plano, metricas


def executar_ferramentas(
    cliente_id,
    plano
):
    resultados = {}
    ferramentas_executadas = []

    for escolha in plano["ferramentas"]:
        nome = escolha["nome"]
        data = escolha.get("data")

        if nome not in FERRAMENTAS_DISPONIVEIS:
            continue

        if nome in resultados:
            continue

        if nome == "operacoes_do_dia":
            if not data:
                continue

            resultado = (
                FERRAMENTAS_DISPONIVEIS[nome](
                    cliente_id,
                    data
                )
            )

        else:
            resultado = (
                FERRAMENTAS_DISPONIVEIS[nome](
                    cliente_id
                )
            )

        resultados[nome] = resultado

        ferramentas_executadas.append({
            "nome": nome,
            "data": data,
            "motivo": escolha["motivo"]
        })

    return resultados, ferramentas_executadas


def gerar_parecer(
    cliente_id,
    alertas_regras,
    resultados_ferramentas
):
    prompt = f"""
Você atua como analista de prevenção a riscos financeiros.

Produza um parecer preliminar usando exclusivamente os dados
fornecidos. Não invente informações, não atribua intenção ao
cliente e não afirme que ocorreu fraude, crime ou irregularidade.

As regras determinísticas são simples e podem gerar falsos
positivos. Analise se os resultados das ferramentas sustentam
ou enfraquecem os alertas.

Cliente:
{cliente_id}

Alertas determinísticos:
{json.dumps(
    alertas_regras,
    ensure_ascii=False,
    indent=2,
    default=str
)}

Resultados das ferramentas:
{json.dumps(
    resultados_ferramentas,
    ensure_ascii=False,
    indent=2,
    default=str
)}

Responda exclusivamente em JSON válido:

{{
  "nivel_risco": "baixo, médio ou alto",
  "tipologia_suspeita": "descrição breve da hipótese",
  "red_flags": [
    "evidência objetiva sustentada pelos dados"
  ],
  "justificativa": "parecer preliminar e objetivo"
}}

Regras:

1. nivel_risco deve ser baixo, médio ou alto;
2. apresente de 1 a 4 red flags;
3. não inclua campos adicionais;
4. indique as limitações dos dados;
5. uma sinalização não comprova irregularidade.
"""

    inicio = time.perf_counter()

    resposta = client.models.generate_content(
        model=MODELO,
        contents=prompt
    )

    latencia = (
        time.perf_counter() - inicio
    )

    parecer = _converter_json(resposta)

    metricas = _extrair_metricas(
        resposta=resposta,
        latencia_segundos=latencia,
        etapa="parecer"
    )

    return parecer, metricas


def executar_agente(
    cliente_id,
    alertas_regras
):
    plano, metricas_planejamento = (
        planejar_ferramentas(
            cliente_id,
            alertas_regras
        )
    )

    (
        resultados_ferramentas,
        ferramentas_executadas
    ) = executar_ferramentas(
        cliente_id,
        plano
    )

    parecer, metricas_parecer = (
        gerar_parecer(
            cliente_id,
            alertas_regras,
            resultados_ferramentas
        )
    )

    return {
        "cliente_id": cliente_id,
        "modelo": MODELO,
        "ferramentas_executadas": (
            ferramentas_executadas
        ),
        "resultados_ferramentas": (
            resultados_ferramentas
        ),
        "parecer": parecer,
        "metricas_chamadas": [
            metricas_planejamento,
            metricas_parecer
        ]
    }