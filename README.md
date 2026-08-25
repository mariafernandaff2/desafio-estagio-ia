# Desafio Técnico — Estágio em Engenharia de Inteligência Artificial

**Candidata:** Maria Fernanda  
**Linguagem principal:** Python 3.12.2  
**Status:** Em desenvolvimento

## 1. Sobre o projeto

Este repositório contém a implementação do Desafio Técnico para Estágio em Engenharia de Inteligência Artificial.

A entrega está organizada em níveis progressivos e reúne os dados fornecidos, o código-fonte, o notebook executado, as saídas geradas e a documentação das decisões adotadas durante o desenvolvimento.

O projeto está sendo desenvolvido com foco em:

- organização e reprodutibilidade;
- separação clara entre os níveis;
- validação explícita dos resultados;
- segurança no uso de credenciais;
- transparência sobre decisões, limitações e uso de Inteligência Artificial.

## 2. Status da implementação

| Etapa | Status |
|---|---|
| Estrutura e configuração do repositório | Concluída |
| Nível 1 | Não iniciado |
| Nível 2 | Não iniciado |
| Nível 3 | Não realizado — opcional |
| Documentação final | Em desenvolvimento |

Os status serão atualizados conforme cada etapa for implementada e validada.

## 3. Estrutura do repositório

```text
desafio-estagio-ia/
├── dados/                         # Arquivos de entrada fornecidos no desafio
│   ├── dados_nivel_1.json
│   └── dados_nivel_2.json
├── docs/                          # Documentação complementar do projeto
│   ├── DECISOES.md
│   └── USO_DE_IA.md               # Registro das ferramentas de IA utilizadas
├── nivel_1/                       # Implementação do Nível 1
│   └── nivel_1.ipynb
├── nivel_2/                       # Implementação do Nível 2
│   ├── agente.py                  # Implementação principal do agente
│   ├── confronto.py               # Implementação do confronto entre agentes
│   └── tools.py                   # Ferramentas utilizadas pelos agentes
├── outputs/
│   └── .gitkeep
├── .env.example
├── .gitignore                     # Impede o versionamento de arquivos sensíveis
├── ENTREGA.yaml                   # Autodeclaração do conteúdo entregue
├── README.md                      # Visão geral e instruções do projeto
└── requirements.txt               # Dependências Python do projeto
```
## 4. Requisitos

Para configurar e executar o projeto, são necessários:

- Python 3.12;
- Git;
- ambiente virtual Python;
- Jupyter Notebook ou VS Code com as extensões Python e Jupyter.

A versão utilizada durante o desenvolvimento é o Python 3.12.2.

## 5. Configuração do ambiente

### 5.1 Criar o ambiente virtual

No Windows, execute:

```powershell
py -3.12 -m venv .venv
```

### 5.2 Ativar o ambiente virtual

No PowerShell, execute:

```powershell
.\.venv\Scripts\Activate.ps1
```

Caso a execução de scripts esteja bloqueada no terminal atual, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Em seguida, tente novamente a ativação do ambiente.

### 5.3 Instalar as dependências

Com o ambiente virtual ativado, execute:

```powershell
python -m pip install -r requirements.txt
```

### 5.4 Configurar as variáveis de ambiente

As credenciais necessárias serão armazenadas localmente em um arquivo chamado `.env`.

O arquivo `.env.example` apresentará os nomes das variáveis necessárias, sem conter credenciais reais. A configuração exata será adicionada após a definição do provedor de LLM utilizado no projeto.

O arquivo `.env` não deve ser enviado ao GitHub.

## 6. Execução

### Nível 1

O Nível 1 será desenvolvido no notebook:

```text
nivel_1/nivel_1.ipynb
```

As instruções de execução serão adicionadas após a implementação e validação dessa etapa. Na entrega final, o notebook será mantido executado, com suas saídas visíveis.

### Nível 2

O Nível 2 será organizado nos seguintes arquivos:

```text
nivel_2/tools.py
nivel_2/agente.py
nivel_2/confronto.py
```

As instruções de execução serão adicionadas após a implementação e validação dessa etapa.

### Nível 3

O Nível 3 é opcional e somente será documentado caso seja efetivamente implementado.

## 7. Resultados e saídas

Os resultados produzidos durante a execução serão armazenados no diretório:

```text
outputs/
```

As saídas relevantes serão incluídas no repositório para permitir a avaliação direta dos resultados, sem depender da execução local do código.

Esta seção será atualizada com a descrição e a localização de cada saída após a conclusão dos níveis implementados.

## 8. Documentação complementar

A documentação detalhada está disponível nos seguintes arquivos:

- [Decisões técnicas](docs/DECISOES.md)
- [Uso de Inteligência Artificial](docs/USO_DE_IA.md)

## 9. Segurança

Nenhuma chave de API, senha ou credencial será incluída no código, nos notebooks, nas saídas ou na documentação.

As credenciais serão armazenadas somente no arquivo local `.env`, que está ignorado pelo Git. O arquivo `.env.example` conterá apenas os nomes das variáveis necessárias, sem valores sensíveis.

## 10. Observação sobre a entrega

O arquivo `ENTREGA.yaml` será atualizado ao final do desenvolvimento com:

- identificação da candidata;
- provedor e modelo utilizados;
- tempo dedicado ao desafio;
- status de cada item;
- localização das implementações e saídas;
- plano para itens parciais ou não realizados.

Somente funcionalidades efetivamente implementadas e verificadas serão declaradas como completas.


## Nível 1

O Nível 1 realiza a limpeza e normalização das operações, conversão dos valores para BRL, agregações por cliente e canal e aplicação de duas regras determinísticas de sinalização.

Um cliente sinalizado é analisado por uma LLM, utilizada somente para interpretação e redação de um parecer estruturado. Os cálculos permanecem sob responsabilidade do Pandas.

O notebook está disponível em:

`nivel_1/nivel_1.ipynb`

Os resultados gerados estão disponíveis em:

`outputs/`