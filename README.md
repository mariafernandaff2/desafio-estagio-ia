# Desafio Técnico — Estágio em Engenharia de Inteligência Artificial

**Candidata:** Maria Fernanda  
**Linguagem principal:** Python 3.12.2  
**Status:** Níveis 1 e 2 concluídos

## 1. Sobre o projeto

Este repositório contém a implementação do Desafio Técnico para Estágio em Engenharia de Inteligência Artificial.

A entrega está organizada em níveis progressivos e reúne os dados fornecidos, os códigos desenvolvidos, os notebooks executados, as saídas geradas e a documentação das decisões adotadas durante o desenvolvimento.

O projeto foi desenvolvido com foco em:

- organização e reprodutibilidade;
- separação clara entre os níveis;
- validação explícita dos resultados;
- segurança no uso de credenciais;
- transparência sobre decisões, limitações e uso de Inteligência Artificial.

A solução combina tratamento de dados com Pandas, regras determinísticas, análise contextual com modelo de linguagem e um agente capaz de selecionar ferramentas de consulta.

## 2. Status da implementação

| Etapa | Status |
|---|---|
| Estrutura e configuração do repositório | Concluída |
| Nível 1 | Concluído |
| Nível 2 | Concluído |
| Nível 3 | Não realizado — opcional |
| Documentação final | Concluída |

Os Níveis 1 e 2 foram implementados, executados e validados. O Nível 3 não foi realizado dentro do tempo disponível e está descrito somente como possibilidade de evolução teórica.

## 3. Estrutura do repositório

```text
desafio-estagio-ia/
├── dados/
│   ├── dados_nivel_1.json
│   └── dados_nivel_2.json
├── docs/
│   ├── DECISOES.md
│   └── USO_DE_IA.md
├── nivel_1/
│   └── nivel_1.ipynb
├── nivel_2/
│   ├── nivel_2.ipynb
│   ├── agente.py
│   ├── confronto.py
│   └── tools.py
├── outputs/
│   ├── resultados do Nível 1
│   └── resultados do Nível 2
├── .env.example
├── .gitignore
├── ENTREGA.yaml
├── README.md
└── requirements.txt
```

O arquivo `.env` não é versionado, pois contém a chave de acesso utilizada para realizar as chamadas ao modelo.

## 4. Tecnologias utilizadas

- Python 3.12.2;
- Pandas;
- Jupyter Notebook;
- Google GenAI SDK;
- Gemini;
- python-dotenv;
- JSON;
- Git e GitHub;
- Visual Studio Code.

## 5. Requisitos

Para configurar e executar o projeto, são necessários:

- Python 3.12;
- Git;
- ambiente virtual Python;
- Jupyter Notebook ou VS Code com as extensões Python e Jupyter;
- chave de acesso válida para a API do Gemini.

A versão utilizada durante o desenvolvimento foi o Python 3.12.2.

## 6. Configuração do ambiente

### 6.1 Criar o ambiente virtual

No Windows, execute:

```powershell
py -3.12 -m venv .venv
```

### 6.2 Ativar o ambiente virtual

No PowerShell, execute:

```powershell
.\.venv\Scripts\Activate.ps1
```

Caso a execução de scripts esteja bloqueada no terminal atual, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Depois, tente novamente a ativação do ambiente virtual.

### 6.3 Instalar as dependências

Com o ambiente virtual ativado, execute:

```powershell
python -m pip install -r requirements.txt
```

### 6.4 Configurar a variável de ambiente

As credenciais necessárias devem ser armazenadas localmente em um arquivo chamado `.env`.

Crie o arquivo `.env` na raiz do projeto e adicione:

```env
GEMINI_API_KEY=sua_chave_aqui
```

O arquivo `.env.example` apresenta o nome da variável necessária sem conter uma credencial real.

O arquivo `.env` não deve ser enviado ao GitHub, pois está incluído no `.gitignore`.

## 7. Execução

Com o ambiente virtual ativado e as dependências instaladas, abra o projeto no VS Code e selecione o interpretador da pasta `.venv`.

### 7.1 Nível 1

Abra o seguinte notebook:

```text
nivel_1/nivel_1.ipynb
```

Execute as células na ordem em que aparecem.

O notebook realiza:

- leitura e inspeção da base;
- identificação de valores ausentes;
- remoção de duplicidades;
- conversão e validação das datas;
- normalização das variáveis categóricas;
- conversão dos valores para BRL;
- agregações por cliente e canal;
- aplicação das duas regras determinísticas;
- análise de um cliente sinalizado com LLM;
- comparação entre duas versões de prompt;
- validação e salvamento das saídas.

O notebook foi mantido executado, com as principais saídas visíveis.

### 7.2 Nível 2

Abra o seguinte notebook:

```text
nivel_2/nivel_2.ipynb
```

O Nível 2 também utiliza os arquivos:

```text
nivel_2/tools.py
nivel_2/agente.py
nivel_2/confronto.py
```

Cada arquivo possui a seguinte responsabilidade:

- `tools.py`: carregamento e tratamento da base, além da implementação das ferramentas de consulta;
- `agente.py`: planejamento, seleção das ferramentas e geração do parecer;
- `confronto.py`: comparação entre o risco determinístico e o risco atribuído pelo agente;
- `nivel_2.ipynb`: aplicação das regras, construção do ranking, execução em lote, cálculo das métricas e validação dos resultados.

Para executar as chamadas ao modelo, é necessário configurar previamente a variável `GEMINI_API_KEY`.

## 8. Implementação do Nível 1

### 8.1 Tratamento dos dados

O Nível 1 realiza:

- leitura da base JSON;
- inspeção dos dados;
- identificação de valores ausentes;
- remoção de duplicidades;
- conversão e validação das datas;
- normalização de canal, tipo e moeda;
- conversão das operações em USD para BRL;
- criação da coluna `valor_brl`;
- agregação do volume por cliente;
- agregação da quantidade de operações por canal.

Os cálculos e as regras permanecem sob responsabilidade do Pandas. O modelo de linguagem é utilizado somente para contextualização e elaboração do parecer.

### 8.2 Regra 1 — Operações concentradas no mesmo dia

A primeira regra sinaliza um cliente quando, no mesmo dia:

- existem pelo menos três operações;
- a soma das operações supera R$ 50.000;
- nenhuma operação individual é igual ou superior a R$ 20.000.

Essa regra procura identificar uma possível fragmentação de valores em diferentes operações.

### 8.3 Regra 2 — Operação acima da mediana histórica

A segunda regra sinaliza uma operação quando:

- o cliente possui pelo menos quatro operações;
- o valor da operação supera cinco vezes a mediana das operações do próprio cliente.

Essa regra procura identificar operações muito superiores ao comportamento histórico observado para o cliente.

### 8.4 Análise com modelo de linguagem

Um cliente sinalizado pelas regras foi analisado pelo Gemini.

Foram comparadas duas versões de prompt, com validação da resposta estruturada em JSON e registro das seguintes informações:

- nível de risco;
- possível tipologia;
- sinais de alerta;
- justificativa;
- quantidade de tokens;
- número de tentativas;
- latência da chamada.

## 9. Implementação do Nível 2

### 9.1 Aplicação das regras em escala

No Nível 2, o tratamento dos dados e as regras determinísticas foram reaplicados a uma base maior.

A base possuía inicialmente:

- 322 registros;
- 30 clientes;
- 5 duplicidades integrais.

Depois da limpeza, permaneceram:

- 317 operações;
- 30 clientes;
- 6 operações com datas ausentes ou inválidas.

A Regra 1 gerou quatro sinalizações, distribuídas entre quatro clientes. A Regra 2 gerou 21 sinalizações, distribuídas entre 13 clientes.

### 9.2 Ranking dos clientes

Foi produzido um ranking com os dez clientes mais sinalizados.

A ordenação considera:

1. quantidade total de sinalizações;
2. volume total movimentado em BRL como critério de desempate.

Cada ocorrência das regras foi contabilizada. Dessa forma, um cliente sinalizado várias vezes recebe prioridade maior do que um cliente com apenas uma ocorrência.

### 9.3 Ferramentas implementadas

Foram implementadas três ferramentas em `nivel_2/tools.py`:

- `historico_cliente(cliente_id)`;
- `operacoes_do_dia(cliente_id, data)`;
- `perfil_canal(cliente_id)`.

O tratamento da base foi encapsulado no próprio arquivo para manter as ferramentas independentes do notebook.

### 9.4 Funcionamento do agente

O agente foi implementado em `nivel_2/agente.py` e utiliza duas etapas:

1. planejamento e escolha das ferramentas;
2. geração do parecer estruturado.

Na primeira chamada, o modelo recebe os alertas determinísticos e escolhe as ferramentas consideradas necessárias.

Na segunda chamada, o modelo recebe os resultados das ferramentas selecionadas e produz o parecer final.

Dessa forma, as três ferramentas não são executadas obrigatoriamente para todos os clientes.

O parecer contém:

- `nivel_risco`;
- `tipologia_suspeita`;
- `red_flags`;
- `justificativa`.

### 9.5 Execução em lote

O agente foi executado sobre os dez clientes presentes no ranking.

Para cada cliente, foi salvo um registro contendo:

- alertas determinísticos;
- ferramentas escolhidas;
- resultados das ferramentas;
- parecer do agente;
- métricas das chamadas.

Os resultados foram salvos após o processamento de cada cliente, reduzindo o risco de perda das análises concluídas caso ocorresse uma falha posterior.

Também foi produzido um arquivo consolidado com os resultados do lote.

### 9.6 Tokens, custo e latência

Cada cliente utilizou duas chamadas ao modelo:

1. uma chamada para planejamento;
2. uma chamada para geração do parecer.

A análise dos dez clientes resultou em 20 chamadas.

Foram registrados:

- tokens de entrada;
- tokens de saída;
- tokens totais;
- latência de cada chamada;
- etapa correspondente;
- custo observado.

A execução foi realizada na camada gratuita utilizada durante o desenvolvimento. Por isso, o custo monetário observado foi registrado como zero. Os tokens foram preservados para permitir uma estimativa futura caso a solução seja executada em uma modalidade paga.

## 10. Confronto entre regras e agente

O confronto entre o risco determinístico e o risco atribuído pelo agente foi implementado em:

```text
nivel_2/confronto.py
```

O critério determinístico adotado foi:

- risco alto quando o cliente é sinalizado pelas duas regras;
- risco médio quando o cliente é sinalizado por apenas uma regra;
- risco baixo quando o cliente não é sinalizado.

A taxa de concordância foi de 80%, com:

- 8 concordâncias;
- 2 divergências.

As divergências foram analisadas individualmente:

- `CLI-017`: a classificação determinística pareceu mais adequada, pois a compatibilidade dos valores individuais com o histórico não elimina a concentração temporal das operações;
- `CLI-029`: a classificação do agente pareceu mais adequada, pois os valores estavam alinhados à magnitude do histórico do cliente, indicando um possível falso positivo da regra.

A análise demonstrou que a taxa de concordância não deve ser interpretada isoladamente. Uma divergência fundamentada pode revelar limitações das regras determinísticas.

## 11. Resultados e arquivos de saída

Os resultados produzidos estão armazenados no diretório:

```text
outputs/
```

Entre as principais saídas estão:

- volume total por cliente;
- quantidade de operações por canal;
- casos sinalizados pelas duas regras;
- relação de clientes sinalizados;
- comparação entre os prompts do Nível 1;
- ranking dos dez clientes mais sinalizados;
- parecer estruturado de cada cliente;
- resultado consolidado da execução em lote;
- métricas de tokens, custo e latência;
- confronto entre regras e agente;
- resumo da taxa de concordância;
- análise individual das divergências.

As saídas foram incluídas no repositório para permitir a avaliação dos resultados sem exigir uma nova execução das chamadas ao modelo.

## 12. Tratamento de erros

A solução contempla:

- validação de cliente inexistente;
- validação de data inválida;
- tratamento de datas ausentes;
- tratamento de valores numéricos inválidos;
- validação da existência da chave da API;
- limpeza e conversão das respostas JSON;
- prevenção de chamadas duplicadas da mesma ferramenta;
- isolamento de erros por cliente durante a execução em lote;
- salvamento individual dos resultados concluídos.

## 13. Decisões e trade-offs

A separação entre planejamento e parecer tornou as decisões do agente mais claras e auditáveis, mas aumentou a quantidade de chamadas, a latência e o consumo de tokens.

O processamento sequencial facilitou o controle dos erros e dos limites da API, embora tenha aumentado o tempo total de execução.

Manter o tratamento da base em `tools.py` respeitou a estrutura solicitada e tornou as ferramentas independentes do notebook, mas gerou alguma repetição da lógica de preparação dos dados.

A seleção de ferramentas por linguagem natural permitiu uma escolha dinâmica e independente de framework. Como contrapartida, essa seleção pode variar entre execuções e depende da resposta estruturada produzida pelo modelo.

O critério determinístico de risco simplificou o confronto, mas atribuiu o mesmo peso às duas regras.

O salvamento de um arquivo por cliente facilitou a auditoria e a recuperação de falhas, embora tenha aumentado a quantidade de arquivos no diretório `outputs/`.

## 14. Limitações conhecidas

As principais limitações são:

- as regras são simples e podem gerar falsos positivos;
- o agente depende somente dos dados fornecidos;
- algumas operações possuem datas ausentes ou inválidas;
- o histórico disponível por cliente é limitado;
- o modelo pode apresentar variação entre execuções;
- as duas regras recebem o mesmo peso no confronto;
- o planejamento pode escolher ferramentas insuficientes ou desnecessárias;
- não houve validação com casos históricos rotulados;
- os pareceres não foram validados por especialista em prevenção a fraudes;
- os pareceres não substituem uma revisão humana;
- não foram implementados testes automatizados com `pytest`;
- a latência depende da disponibilidade externa da API;
- o custo monetário pago não foi medido porque a execução ocorreu na camada gratuita.

Mais informações estão disponíveis em [Decisões técnicas](docs/DECISOES.md).

## 15. Nível 3 — Não implementado

O Nível 3 era opcional e não foi implementado dentro do tempo disponível para a entrega.

A decisão foi priorizar a conclusão, execução e validação dos Níveis 1 e 2, garantindo:

- funcionamento das regras sobre as duas bases;
- implementação das ferramentas;
- seleção dinâmica de ferramentas pelo agente;
- processamento dos dez clientes do ranking;
- registro das métricas;
- persistência das saídas;
- confronto entre regras e agente;
- análise individual das divergências;
- documentação das decisões e limitações.

Essa limitação está registrada de forma transparente. Nenhum resultado do Nível 3 é apresentado como se tivesse sido implementado ou executado.

### 15.1 Possível evolução teórica

Como evolução da solução atual, o Nível 3 poderia incluir:

1. modularização adicional do tratamento e das regras;
2. validação das respostas com Pydantic ou JSON Schema;
3. retentativas automáticas com espera progressiva;
4. uso de function calling nativo;
5. cache para evitar chamadas repetidas;
6. processamento paralelo com limite de concorrência;
7. testes unitários e testes de integração;
8. armazenamento dos resultados em banco de dados;
9. criação de uma API ou interface de consulta;
10. revisão humana obrigatória para riscos médios e altos;
11. monitoramento contínuo de custos, latência, erros e versões;
12. calibração das regras e classificações com dados históricos rotulados;
13. implementação de controles de segurança, privacidade e acesso.

### 15.2 Possível plano de validação

Uma implementação futura poderia ser validada por meio de:

- testes com clientes conhecidos como positivos e negativos;
- testes nos valores exatos dos limites das regras;
- testes com clientes inexistentes;
- testes com datas ausentes ou inválidas;
- testes com operações duplicadas;
- testes com diferentes moedas e taxas de câmbio;
- repetição das chamadas para avaliar estabilidade;
- comparação entre diferentes modelos e prompts;
- testes de carga e latência;
- avaliação de falsos positivos e falsos negativos;
- revisão das divergências por especialista;
- validação dos controles de segurança e proteção dos dados;
- estimativa do custo antes da execução em produção.

Essa proposta é somente teórica e não representa uma funcionalidade já implementada.

## 16. Segurança

Nenhuma chave de API, senha ou credencial foi incluída no código, nos notebooks, nas saídas ou na documentação.

As credenciais são armazenadas somente no arquivo local `.env`, que está ignorado pelo Git. O arquivo `.env.example` contém apenas o nome da variável necessária, sem valores sensíveis.

Em um cenário de produção, ainda seriam necessários mecanismos adicionais de:

- autenticação;
- autorização;
- controle de acesso;
- proteção de dados;
- auditoria;
- gerenciamento seguro de credenciais.

## 17. Uso de Inteligência Artificial

A Inteligência Artificial foi utilizada como apoio para:

- interpretação do enunciado;
- organização do raciocínio;
- estruturação e revisão do código;
- investigação e correção de erros;
- construção e comparação dos prompts;
- análise das divergências;
- organização da documentação.

As sugestões foram avaliadas durante o desenvolvimento. Os resultados foram validados por meio da execução do código, de verificações com Pandas e de análise manual.

O registro detalhado está disponível em [Uso de Inteligência Artificial](docs/USO_DE_IA.md).

## 18. Documentação complementar

A documentação detalhada está disponível nos seguintes arquivos:

- [Decisões técnicas](docs/DECISOES.md);
- [Uso de Inteligência Artificial](docs/USO_DE_IA.md);
- `ENTREGA.yaml`: identificação, status e resumo da entrega;
- `outputs/`: resultados gerados durante as análises.

## 19. Observação sobre a entrega

O arquivo `ENTREGA.yaml` contém:

- identificação da candidata;
- provedor e modelo utilizados;
- tempo dedicado ao desafio;
- status dos níveis;
- localização das implementações e saídas;
- plano para itens parciais ou não realizados.

Somente funcionalidades efetivamente implementadas, executadas e verificadas foram declaradas como concluídas.

## 20. Considerações finais

A implementação combina regras determinísticas, ferramentas de consulta e análise contextual com um modelo de linguagem.

As regras fornecem critérios objetivos e reproduzíveis, enquanto o agente utiliza as ferramentas para contextualizar os alertas. O confronto mostrou que uma discordância do modelo não representa necessariamente um erro, pois também pode revelar limitações ou possíveis falsos positivos das regras.

Os pareceres gerados são preliminares e devem apoiar, e não substituir, a decisão de um especialista. Em um cenário real, classificações de risco médio ou alto deveriam passar obrigatoriamente por revisão humana.