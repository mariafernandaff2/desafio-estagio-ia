# Uso de Inteligência Artificial

## 1. Ferramentas utilizadas

| Ferramenta | Finalidade |
|---|---|
| ChatGPT | Interpretação do enunciado, organização do raciocínio, estruturação do repositório, apoio na implementação, investigação de erros e revisão da documentação |
| Gemini | Análise contextual dos clientes, seleção das ferramentas do agente e geração dos pareceres estruturados |

## 2. Uso do ChatGPT durante o desenvolvimento

O ChatGPT foi utilizado como ferramenta de apoio ao longo do desenvolvimento do projeto.

Na etapa inicial, auxiliou na interpretação do desafio, na divisão do trabalho em etapas menores e na organização da estrutura do repositório. Também foi utilizado para orientar a preparação do ambiente virtual e a elaboração dos arquivos:

- `README.md`;
- `DECISOES.md`;
- `USO_DE_IA.md`;
- `ENTREGA.yaml`;
- `.env.example`;
- `requirements.txt`.

Durante a implementação dos Níveis 1 e 2, o ChatGPT também foi utilizado para:

- esclarecer conceitos de Pandas e processamento de dados;
- estruturar a sequência de limpeza e normalização;
- apoiar a construção das regras determinísticas;
- revisar prompts enviados ao modelo;
- investigar mensagens de erro;
- organizar o agente e suas ferramentas;
- estruturar a execução em lote;
- apoiar o cálculo e o registro das métricas;
- analisar o confronto entre regras e agente;
- revisar a redação da documentação final.

As orientações não foram aplicadas automaticamente. Cada sugestão foi adaptada ao projeto e verificada com base no enunciado, na execução do código, nas respostas do terminal, nas saídas dos notebooks e na inspeção manual dos resultados.

## 3. Uso do Gemini na solução

O Gemini foi utilizado como componente da solução implementada.

No Nível 1, o modelo recebeu os dados de um cliente previamente sinalizado pelas regras determinísticas e produziu um parecer estruturado contendo:

- nível de risco;
- possível tipologia;
- sinais de alerta;
- justificativa.

No Nível 2, o Gemini foi utilizado em duas etapas:

1. planejamento e seleção das ferramentas necessárias;
2. geração do parecer após o recebimento dos resultados das ferramentas.

O modelo não realizou os cálculos determinísticos. A limpeza, a conversão cambial, as agregações, as medianas, o ranking e as regras de sinalização foram executados com Pandas.

O Gemini foi utilizado somente para interpretar os dados fornecidos, selecionar as consultas consideradas necessárias e redigir os pareceres estruturados.

## 4. Comparação dos prompts

No Nível 1, foram comparadas duas versões de prompt.

A Versão 1 solicitou um parecer estruturado e objetivo sobre o cliente sinalizado.

A Versão 2 tornou as restrições mais explícitas, exigindo que:

- as conclusões fossem sustentadas diretamente pelos dados;
- o modelo não atribuísse intenção ao cliente;
- nenhuma informação ausente fosse inventada;
- a sinalização não fosse tratada como comprovação de irregularidade;
- a resposta respeitasse a estrutura JSON solicitada.

A comparação mostrou que instruções mais específicas ajudam a limitar conclusões indevidas e tornam a resposta mais adequada para auditoria.

**Cliente analisado no Nível 1:** `CLI-A-1`  
**Modelo utilizado:** verificar o mesmo identificador registrado no código e nos notebooks.

## 5. Validação das respostas

As respostas do modelo foram verificadas por meio de:

- validação da estrutura JSON;
- conferência dos campos obrigatórios;
- comparação com os dados enviados ao modelo;
- verificação de que o parecer não apresentava informações ausentes na base;
- análise manual das justificativas;
- confronto entre o risco determinístico e o risco atribuído pelo agente;
- inspeção individual das divergências.

Também foram registrados, quando disponíveis:

- tokens de entrada;
- tokens de saída;
- tokens totais;
- latência;
- quantidade de tentativas;
- etapa da chamada;
- modelo utilizado.

Os pareceres foram tratados como análises preliminares. Eles não representam comprovação de fraude ou irregularidade e não substituem a avaliação de um especialista.

## 6. Exemplo de validação das orientações da IA

Durante a criação do `requirements.txt`, uma primeira consulta foi realizada com o ambiente Anaconda ativo, em vez do ambiente virtual específico do projeto.

O problema foi identificado pelos caminhos exibidos no terminal e pela versão do Python utilizada. Após a reativação da `.venv`, as dependências corretas foram verificadas e registradas.

Esse caso reforçou a necessidade de conferir o ambiente de execução e validar as orientações fornecidas pela IA antes de incorporá-las ao projeto.

## 7. Limitações do uso de IA

As principais limitações consideradas foram:

- o modelo pode produzir respostas diferentes entre execuções;
- a seleção das ferramentas pode variar conforme a resposta do modelo;
- uma resposta válida em JSON não é necessariamente correta em seu conteúdo;
- o modelo depende exclusivamente das informações fornecidas;
- o agente pode escolher ferramentas insuficientes ou desnecessárias;
- os pareceres podem reproduzir limitações presentes nos dados e nos prompts;
- a IA não substitui validação técnica nem revisão humana;
- as classificações não foram calibradas com uma base histórica rotulada;
- os pareceres não foram validados por especialista em prevenção a fraudes.

Por essas razões, os cálculos e as regras permaneceram determinísticos, e as respostas da LLM foram utilizadas somente como apoio contextual.

## 8. Responsabilidade sobre a entrega

A responsabilidade pelas decisões, pelo código executado e pelo conteúdo entregue permanece com a candidata.

A IA foi utilizada como ferramenta de apoio, mas os resultados foram revisados por meio de:

- execução dos notebooks;
- inspeção das saídas;
- verificações com Pandas;
- análise das mensagens do terminal;
- conferência manual dos resultados;
- comparação com os requisitos do desafio.

Somente funcionalidades efetivamente implementadas e verificadas foram declaradas como concluídas.

O Nível 3 não foi implementado. As possibilidades apresentadas para essa etapa são apenas propostas teóricas de evolução e não foram descritas como funcionalidades executadas.