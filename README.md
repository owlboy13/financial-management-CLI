# FlowFinance

Sistema de gestão financeira pessoal via CLI, desenvolvido em Python com SQLite.

## Sobre

Ferramenta de linha de comando para registrar e acompanhar contas a pagar e a receber, com suporte a múltiplas tabelas por período (ex: `gastos_outubro`, `receita_outubro`), visualização de KPIs e geração de gráficos interativos.

## Funcionalidades

- Autenticação com usuário e senha (senha armazenada com SHA-256)
- Criação de tabelas por período
- Inserção de contas a pagar e receber
- Atualização de registros: marcar como pago, editar valor, adicionar observação
- Visualização da tabela com total, média, mínimo e máximo
- Estatísticas com gráficos interativos (Plotly)
- Cálculo do valor líquido entre duas tabelas (receita - gastos)
- Exclusão de registros
- Logs em arquivo

## Tecnologias

- Python 3.12
- SQLite3
- Pandas
- Plotly
- python-dotenv
- pwinput

## Estrutura

```
gestao-financeira/
├── main.py               # Ponto de entrada e menu principal
├── utils.py              # Funções de manipulação, exibição e gráficos
├── config/
│   ├── auth.py           # Função de autenticação
│   ├── login.py          # Classe Login
│   └── register.py       # Classe Register (cadastro de usuários)
├── database/
│   └── database.py       # Classes DataBase e Table (camada de dados)
├── logs/                 # Logs gerados em execução
└── .env                  # Configurações de ambiente
```

## Configuração

1. Clone o repositório
2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. Crie o arquivo `.env` na raiz:
```env
DATABASE="gestao_financeira_2026.db"
TABLE_ACCOUNT="table_account"
```
5. Crie a pasta de logs:
```bash
mkdir logs
```
6. Cadastre um usuário pelo `Register` em `config/register.py` antes do primeiro acesso.

## Execução

```bash
python main.py
```

## Variáveis de ambiente

| Variável        | Descrição                        |
|-----------------|----------------------------------|
| `DATABASE`      | Nome do arquivo do banco SQLite  |
| `TABLE_ACCOUNT` | Nome da tabela de usuários       |
