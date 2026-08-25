# Uso de Inteligência Artificial

## 1. Ferramenta utilizada

| Ferramenta | Finalidade |
|---|---|
| ChatGPT | Estruturação do raciocínio, interpretação do desafio, organização do repositório e orientação sobre documentação e Git/GitHub |

## 2. Uso na etapa inicial

Nesta etapa, o ChatGPT foi utilizado para organizar minha linha de raciocínio e dividir o desafio em etapas menores antes do desenvolvimento técnico.

A IA auxiliou na preparação do ambiente, na estruturação do repositório e no planejamento dos arquivos `README.md`, `DECISOES.md`, `USO_DE_IA.md` e `ENTREGA.yaml`.

As orientações foram aplicadas manualmente e verificadas com base no enunciado, nas respostas do terminal e no conteúdo enviado ao GitHub.

## 3. Ajuste realizado

Durante a criação do `requirements.txt`, uma primeira consulta apresentou dependências do ambiente Anaconda, em vez do ambiente virtual do projeto.

O problema foi identificado pelos caminhos e pela versão do Python. Após a reativação da `.venv`, as dependências corretas foram verificadas e registradas.

Esse caso reforçou a necessidade de validar as orientações da IA antes de aplicá-las.

## 4. Próximas atualizações

### Comparação dos prompts

A Versão 1 solicitou um parecer estruturado e objetivo. A Versão 2 tornou as restrições mais explícitas, exigindo evidências diretamente sustentadas pelos dados, impedindo atribuição de intenção e reforçando que a sinalização não comprova irregularidade.

Os cálculos, a conversão cambial, as agregações, as medianas e as regras de sinalização foram executados exclusivamente com Pandas. A LLM foi utilizada apenas na interpretação textual do caso.

**Modelo:** gemini-3.5-flash-lite  
**Cliente analisado:** CLI-A-1

