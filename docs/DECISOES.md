# Decisões Técnicas

## 1. Objetivo deste documento

## 2. Decisões gerais do projeto

## 3. Decisões do Nível 1

### 3.1 Leitura e inspeção dos dados
O arquivo JSON foi inspecionado para compreender sua estrutura e verificar dados ausentes, duplicidades e inconsistências de padronização.

A taxa de câmbio foi armazenada separadamente, enquanto a lista de operações foi transformada em um DataFrame.

A taxa é um parâmetro geral usado na conversão de USD para BRL e não representa uma operação financeira. A separação mantém uma linha por operação no DataFrame.

A separação exige uma etapa adicional, mas proporciona maior controle sobre a estrutura dos dados.

Serão conferidos os 20 registros, os 6 clientes únicos, as colunas, os tipos de dados, os valores ausentes e as duplicidades.

### 3.2 Limpeza e tratamento de inconsistências
A coluna `data` foi convertida de texto para `datetime`, permitindo validar datas inválidas e agrupar corretamente as operações realizadas no mesmo dia. A ausência da data impede determinar quando a operação `OP-0017` ocorreu.


A segunda ocorrência da operação `OP-0007` foi removida por ser integralmente duplicada. A operação `OP-0017` foi mantida com data ausente, pois seus demais dados são válidos e não há evidência para imputar uma data.
A duplicidade alteraria artificialmente as agregações e a aplicação da Regra 1. Já a operação sem data pode participar dos cálculos que não dependem de temporalidade, incluindo a Regra 2, mas será excluída da análise por mesma data exigida pela Regra 1.

Após a limpeza, a base contém 19 registros, 6 clientes únicos, nenhuma duplicidade integral e uma operação com data ausente.

### 3.3 Normalização dos dados
As categorias `canal` e `tipo` foram normalizadas em letras minúsculas e sem espaços externos. A coluna `moeda` foi padronizada em letras maiúsculas e validada para aceitar apenas BRL e USD. O valor original foi preservado, e uma nova coluna `valor_brl` foi criada utilizando a taxa fixa USD/BRL fornecida no arquivo.

A padronização evita categorias equivalentes representadas de formas diferentes. A preservação do valor e da moeda originais mantém a rastreabilidade, enquanto `valor_brl` permite realizar agregações e aplicar as regras em uma unidade monetária comum. A conversão utiliza uma taxa fixa e não considera variações cambiais por data.

Foram verificadas moedas inválidas, valores ausentes ou não positivos e a conversão da operação em USD.


### 3.4 Agregações


### 3.5 Regras determinísticas
## Implementação da Regra 1

**Contexto:**  
A Regra 1 busca identificar um conjunto de operações do mesmo cliente, na mesma data, com possível fracionamento de valores.
As operações com data válida foram agrupadas por `cliente_id` e `data`. Para cada grupo, foram calculadas a quantidade de operações, a soma em BRL e a maior operação individual. O grupo foi sinalizado quando apresentou pelo menos três operações, soma superior a R$ 50.000 e nenhuma operação individual igual ou superior a R$ 20.000.


O agrupamento por cliente e data permite aplicar diretamente os critérios determinísticos do desafio. A condição de que nenhuma operação seja igual ou superior a R$ 20.000 foi representada pela verificação de que o maior valor do grupo é inferior a R$ 20.000.

A operação `OP-0017` foi excluída somente desta regra, pois não possui data e não pode ser associada com segurança a um grupo diário. Ela foi preservada na base principal e nas análises que não dependem da data.


O cliente `CLI-A-1`, em 09/03/2026, foi validado como caso positivo, com três operações que totalizam R$ 54.200 e maior valor individual de R$ 18.800. O cliente `CLI-A-3`, em 05/03/2026, foi validado como caso semelhante negativo, pois suas três operações totalizam R$ 48.500, abaixo do limite exigido.

 
A regra depende da disponibilidade e correção das datas. Operações sem data não podem ser avaliadas quanto à ocorrência no mesmo dia.



## Implementação da Regra 2
A Regra 2 busca identificar operações com valor muito superior ao comportamento habitual do próprio cliente.

Foram calculadas a quantidade de operações e a mediana dos valores em BRL para cada cliente. Essas estatísticas foram associadas às operações, e foram sinalizados somente os valores superiores a cinco vezes a mediana de clientes com pelo menos quatro operações.

A mediana foi utilizada conforme determinado pelo desafio e apresenta menor sensibilidade a valores extremos do que a média. A conversão prévia para BRL garante que operações em moedas diferentes sejam comparadas na mesma unidade.


A operação `OP-0017` foi mantida na Regra 2 porque essa análise depende apenas do cliente e do valor, e não da data. Sua exclusão reduziria artificialmente o número de operações do cliente `CLI-A-5`.


A operação `OP-0013`, do cliente `CLI-A-4`, foi validada como caso positivo. O cliente possui quatro operações, mediana de R$ 5.450 e limite de R$ 27.250. Como a operação possui valor convertido de R$ 64.800, ela foi sinalizada. O cliente `CLI-A-5` foi validado como caso negativo elegível, pois possui quatro operações, mas nenhuma supera cinco vezes sua mediana.

A regra considera apenas a distribuição de valores do próprio conjunto analisado. Em bases pequenas, a mediana pode não representar completamente o comportamento histórico do cliente.

### 3.6 Validações
O cliente `CLI-A-1`, sinalizado pela Regra 1, foi selecionado para a análise com LLM. O cliente apresenta três operações realizadas na mesma data, com soma de R$ 54.200 e valores individuais inferiores a R$ 20.000. O caso permite avaliar como a LLM interpreta e comunica um comportamento já identificado por uma regra determinística. A maior limitação é A seleção de um único cliente não permite generalizar o parecer para todos os casos sinalizados. A LLM será utilizada apenas para interpretação e redação, sem recalcular os critérios da regra.



### 3.7 Divisão de responsabilidades entre pandas e LLM


## Integração com LLM
A LLM foi utilizada para interpretar e redigir o parecer de um cliente previamente sinalizado pelo Pandas. Foram testadas duas versões do prompt. A segunda versão adicionou restrições contra inferências não sustentadas, atribuição de intenção e conclusões definitivas.

As respostas foram convertidas de JSON para dicionário Python e validadas quanto aos campos obrigatórios, tipos e níveis de risco permitidos. Respostas malformadas são preservadas e identificadas com uma mensagem de erro, evitando que sejam utilizadas silenciosamente.

Também foram registrados modelo, tempo, número de tentativas e tokens. Indisponibilidades temporárias da API foram tratadas com novas tentativas progressivas.
### 3.8 Estrutura e validação da resposta da LLM


## 4. Decisões do Nível 2
### Reutilização do tratamento e das regras

O tratamento aplicado no Nível 1 foi reutilizado na base do Nível 2, incluindo remoção de duplicidades, conversão de datas, normalização de variáveis categóricas e conversão das operações em USD para BRL. A base passou de 322 para 317 registros após a remoção de cinco duplicidades integrais. Também foram identificadas seis operações com datas ausentes ou inválidas.

Se o projeto fosse refeito desde o início, a limpeza e as regras seriam implementadas como funções reutilizáveis já no Nível 1. Isso reduziria a repetição entre o notebook e os arquivos do Nível 2. Nesta entrega, o tratamento necessário às ferramentas foi encapsulado internamente em `tools.py`, respeitando a estrutura de arquivos solicitada.

### Critério do ranking

O número total de sinalizações foi calculado pela soma das ocorrências das duas regras. O ranking foi ordenado primeiro pelo total de sinalizações e, nos empates, pelo volume total movimentado em BRL.


O agente foi dividido em duas etapas. Na primeira chamada, o modelo recebe os alertas determinísticos e escolhe somente as ferramentas necessárias. Na segunda, utiliza os resultados consultados para elaborar o parecer. Essa separação evita chamar automaticamente todas as ferramentas para todos os clientes.

Foram realizadas duas chamadas ao modelo por cliente: uma de planejamento e outra de geração do parecer. A execução dos dez clientes resultou em 20 chamadas. Foram registrados tokens de entrada, tokens de saída e latência de cada chamada. Como a execução foi realizada na camada gratuita do provedor, o custo monetário observado foi zero, mas o consumo de tokens foi preservado como medida de utilização.

### Critério de confronto

Foi adotado risco alto quando as duas regras sinalizam o cliente, risco médio quando somente uma regra sinaliza e risco baixo quando nenhuma regra sinaliza. Esse critério representa a quantidade de evidências determinísticas, mas não considera as regras como verdade absoluta.

A taxa de concordância entre regras e agente foi de 80%, com oito concordâncias e duas divergências.

No caso `CLI-017`, a regra determinística parece mais adequada. Embora o agente tenha considerado os valores compatíveis com o histórico, essa comparação não elimina o padrão temporal de operações concentradas no mesmo dia.

No caso `CLI-029`, o agente parece mais adequado. Os valores que acionaram a regra estavam alinhados à magnitude do histórico do cliente, oferecendo uma explicação plausível para um falso positivo. A conclusão continua preliminar devido à ausência de dados qualitativos adicionais.


### 4.1 Organização das ferramentas

As ferramentas foram implementadas em `nivel_2/tools.py`, conforme a estrutura solicitada no desafio. Foram criadas três funções principais:

- `historico_cliente(cliente_id)`: retorna quantidade de operações, volume total, média, mediana, maior operação e período do histórico;
- `operacoes_do_dia(cliente_id, data)`: retorna as operações de um cliente em uma data específica;
- `perfil_canal(cliente_id)`: apresenta a distribuição das operações por canal, incluindo quantidade, percentual e volume movimentado.

O carregamento e o tratamento da base também foram encapsulados internamente em `tools.py`. Essa escolha evitou a criação de arquivos adicionais que não estavam previstos na estrutura do desafio. As ferramentas retornam dicionários ou listas de dicionários, facilitando a conversão dos resultados para JSON e o envio ao modelo.

Também foi criado um dicionário chamado `FERRAMENTAS_DISPONIVEIS`, que associa o nome de cada ferramenta à função correspondente. Isso permitiu que o agente executasse dinamicamente apenas as ferramentas escolhidas durante o planejamento.

A limpeza usada no Nível 1 foi reaplicada à base maior. O processo incluiu:

- remoção de duplicidades integrais;
- conversão das datas com tratamento de valores inválidos;
- identificação de datas ausentes;
- normalização de canal e tipo para letras minúsculas;
- normalização da moeda para letras maiúsculas;
- conversão da coluna de valor para formato numérico;
- conversão das operações em USD para BRL;
- criação da coluna padronizada `valor_brl`.

### 4.2 Estrutura do agente


O agente foi implementado em `nivel_2/agente.py` e dividido em duas chamadas ao modelo.

Na primeira etapa, chamada de planejamento, o modelo recebe:

- o identificador do cliente;
- os alertas determinísticos;
- a descrição das ferramentas disponíveis.

A partir desse contexto, o modelo escolhe quais ferramentas são necessárias. Essa etapa é importante porque chamar as três ferramentas para todos os clientes caracterizaria um fluxo fixo, e não uma decisão de agente.

Na segunda etapa, o modelo recebe:

- os alertas determinísticos;
- os resultados das ferramentas escolhidas;
- instruções para produzir um parecer preliminar e estruturado.

O parecer contém:

- `nivel_risco`;
- `tipologia_suspeita`;
- `red_flags`;
- `justificativa`.

O prompt determina que o modelo não deve inventar informações, atribuir intenção ao cliente, afirmar a ocorrência de fraude ou tratar a sinalização como prova de irregularidade.

No teste do cliente `CLI-014`, por exemplo, o agente escolheu apenas `historico_cliente`. Isso demonstrou que a seleção não estava programada para chamar todas as ferramentas automaticamente.

### 4.3 Estratégia de confronto
O confronto foi implementado em `nivel_2/confronto.py`.

Para possibilitar uma comparação objetiva, foi adotado o seguinte critério determinístico:

- risco alto: cliente sinalizado pelas duas regras;
- risco médio: cliente sinalizado por apenas uma regra;
- risco baixo: cliente não sinalizado por nenhuma regra.

Esse critério foi escolhido por representar a quantidade de evidências determinísticas existentes para cada cliente. Entretanto, ele não considera as regras como verdade absoluta, pois ambas são propositalmente simples.

A classificação determinística foi comparada ao `nivel_risco` atribuído pelo agente. A taxa de concordância foi de 80%, com oito concordâncias e duas divergências.

As divergências foram avaliadas individualmente:

- `CLI-017`: a regra determinística parece mais adequada. Embora o agente tenha considerado os valores compatíveis com o histórico, essa compatibilidade não elimina o padrão temporal de operações concentradas no mesmo dia. A classificação continua sendo apenas um alerta preliminar.
- `CLI-029`: o agente parece mais adequado. Os valores das operações estavam alinhados à magnitude do histórico de um cliente com 16 operações e aproximadamente R$ 191 mil movimentados. Isso oferece uma justificativa plausível para interpretar o alerta da regra como possível falso positivo, embora ainda exista necessidade de revisão humana.

A análise mostrou que a taxa de concordância não deve ser interpretada isoladamente. Uma divergência bem fundamentada pode representar uma análise contextual melhor do que a aplicação rígida da regra.

### 4.4 Tratamento de erros


### 4.5 Registro das saídas
Os resultados foram salvos na pasta `outputs/`.

Foram produzidos:

- ranking dos dez clientes mais sinalizados;
- um arquivo JSON estruturado por cliente;
- arquivo JSON consolidado com os dez pareceres;
- métricas individuais das chamadas ao modelo;
- resumo das métricas;
- comparação das métricas por etapa;
- confronto completo entre regra e agente;
- resumo da taxa de concordância;
- análise das divergências.

O salvamento individual foi realizado imediatamente após a conclusão de cada cliente. Essa decisão reduz o risco de perder todo o lote caso uma chamada posterior apresente erro.

## 5. Trade-offs
O tratamento de erros foi aplicado em diferentes pontos.

Em `tools.py`:

- clientes inexistentes geram `ValueError`;
- datas inválidas fornecidas à ferramenta `operacoes_do_dia` geram `ValueError`;
- datas inválidas presentes na base são convertidas para valores ausentes;
- valores numéricos inválidos são convertidos com `errors="coerce"`;
- resultados ausentes são convertidos para `None` antes da serialização.

Em `agente.py`:

- a ausência de `GEMINI_API_KEY` interrompe a execução com uma mensagem explícita;
- respostas delimitadas por blocos Markdown são limpas antes da conversão;
- a resposta é convertida com `json.loads`, permitindo identificar JSON malformado;
- nomes de ferramentas que não existem no registro são ignorados;
- chamadas duplicadas da mesma ferramenta não são executadas novamente;
- `operacoes_do_dia` não é executada quando o planejamento não apresenta uma data.

Na execução em lote:

- cada cliente é processado dentro de `try/except`;
- erros são registrados com o identificador do cliente e a mensagem correspondente;
- o erro de um cliente não impede o processamento dos clientes seguintes;
- resultados concluídos são salvos individualmente.

Em `confronto.py`:

- a ausência de arquivos de resultados gera erro explícito;
- os níveis de risco são convertidos para uma escala ordinal;
- a quantidade de concordâncias e divergências é validada antes da conclusão.

## 6. Limitações conhecidas

As regras são simples e podem gerar falsos positivos. O agente depende apenas dos dados fornecidos, pode variar entre execuções e não substitui a revisão humana. A base possui histórico limitado e algumas datas inválidas.

O critério de risco atribui o mesmo peso às duas regras. Também não foram realizados testes com dados rotulados nem validação dos pareceres por um especialista. A latência depende da API e o custo monetário foi registrado como zero por causa da camada gratuita utilizada.

## 7. Itens parciais ou não implementados

Não foram implementados retentativas automáticas, processamento paralelo, cache, validação com Pydantic ou JSON Schema, function calling nativo e testes com `pytest`.

Também ficaram fora do protótipo uma interface de revisão, banco de dados, monitoramento contínuo de custo, revisão humana integrada, calibração com dados rotulados e controles de segurança para produção.

### Plano de implementação futura

Como evolução, seriam priorizados:

1. validação estruturada das respostas e retentativas automáticas;
2. testes unitários para limpeza, regras, ferramentas e confronto;
3. cache e processamento paralelo controlado;
4. function calling nativo e monitoramento de custos;
5. auditoria de prompts, modelos e respostas;
6. revisão humana para riscos médios e altos;
7. validação e calibração com casos rotulados;
8. controles de segurança, privacidade e acesso.