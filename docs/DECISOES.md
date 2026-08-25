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

### 4.1 Organização das ferramentas
### 4.2 Estrutura do agente
### 4.3 Estratégia de confronto
### 4.4 Tratamento de erros
### 4.5 Registro das saídas

## 5. Trade-offs

## 6. Limitações conhecidas

## 7. Itens parciais ou não implementados

## 8. Plano de implementação e validação