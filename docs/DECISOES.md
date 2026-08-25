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
### 3.6 Validações
### 3.7 Divisão de responsabilidades entre pandas e LLM
### 3.8 Estrutura e validação da resposta da LLM
### 3.9 Tratamento de respostas malformadas

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