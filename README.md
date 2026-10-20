
# Sistema de Agendamento — Salão Beleza Rara

## Sobre o projeto

O Sistema de Agendamento do Salão Beleza Rara é uma aplicação web desenvolvida para facilitar o cadastro e a organização de horários de atendimento do salão.

O projeto busca reduzir conflitos de horários e facilitar a consulta e o cancelamento de agendamentos.

## Objetivos

- Cadastrar agendamentos de clientes.
- Consultar a lista de agendamentos.
- Impedir agendamentos confirmados no mesmo dia e horário.
- Permitir o cancelamento de agendamentos.
- Validar o preenchimento dos campos obrigatórios.

## Tecnologias utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML
- CSS
- pytest
- Git e GitHub

## Funcionalidades implementadas

- Página inicial do sistema.
- Formulário de agendamento.
- Listagem de agendamentos.
- Cancelamento de agendamentos.
- Bloqueio de horários já ocupados.
- Persistência dos dados em banco SQLite.

## Como executar o projeto

### 1. Pré-requisitos

Tenha o Python instalado e o Git disponível no computador.

### 2. Clonar o repositório

```bash
git clone https://github.com/lidianesilva12/sistema-agendamento-beleza-rara.git
cd sistema-agendamento-beleza-rara
```

### 3. Criar e ativar o ambiente virtual

No Windows, usando PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```bash
python -m pip install Flask Flask-SQLAlchemy pytest
```

### 5. Executar a aplicação

```bash
python app.py
```

Abra o navegador no endereço:

http://127.0.0.1:5000

## Testes automatizados

Para executar os testes:

```bash
python -m pytest -v
```

Os testes verificam a página inicial, o cadastro, o bloqueio de horários duplicados, o cancelamento e os campos obrigatórios.

## Organização do projeto

```text
sistema-agendamento-beleza-rara/
├── app.py
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── index.html
│   ├── agendar.html
│   └── agendamentos.html
├── tests/
│   └── test_app.py
├── .gitignore
└── README.md
```

## Contexto do projeto

O projeto foi pensado para apoiar a organização dos atendimentos do Salão Beleza Rara, contribuindo para melhorar o gerenciamento da agenda e reduzir conflitos de horários.

## Status

Projeto em desenvolvimento acadêmico. Novas melhorias e validações poderão ser incorporadas nas próximas etapas.
