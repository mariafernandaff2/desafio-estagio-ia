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