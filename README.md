Petto API🐾
Um sistema de gerenciamento de pets, com autenticação de usuários, registros de doenças, vacinas e medicamentos, além de diários específicos para cada bichinho! 
------------------------------------------------------------------------------------
Estrutura do projeto:
Petto/
│
├── app/                     # Pasta principal da aplicação
│   │
│   ├── database/            # Configurações do banco de dados
│   │   └── connection.py    # Configurações de conexão com SQLAlchemy
│   │
│   ├── migrations/          # Migrações do banco de dados (Alembic)
│   │   ├── versions/        # Arquivos de versão das migrações
│   │   └── env.py           # Configuração do ambiente de migração
│   │
│   ├── models/              # Definições de modelos de dados
│   │   ├── model.py         # Modelos SQLAlchemy (tabelas do banco)
│   │   └── schemas.py       # Schemas Pydantic para validação
│   │
│   ├── routes/              # Endpoints da API (FastAPI)
│   │   ├── auth.py          # Autenticação (login, registro, JWT)
│   │   ├── diaries.py       # Endpoints para diários dos pets
│   │   ├── medical.py       # Endpoints para registros médicos
│   │   ├── pets.py          # CRUD para gerenciamento de pets
│   │   └── users.py         # Gerenciamento de usuários
│   │
│   └── seeders/            # Scripts para popular dados iniciais
│       ├── diarios.py       # Dados iniciais de diários
│       ├── fotos.py         # Imagens padrão dos pets (armazenadas como BLOB)
│       ├── pets.py          # Cadastros iniciais de pets
│       ├── run_seeders.py   # Script principal que executa todos seeders
│       ├── saude.py         # Registros iniciais de saúde
│       └── users.py         # Usuários iniciais do sistema
│
├── seed_data/              # Arquivos de imagem para seeders
│   ├── gatoviralata_teste02.jpg  # Imagem exemplo 1
│   └── goldenretriver_teste01.jpg # Imagem exemplo 2
│
├── venv/                   # Ambiente virtual Python (gerado automaticamente)
├── .env                    # Variáveis de ambiente sensíveis
├── .env.example            # Template de variáveis de ambiente
├── alembic.ini             # Configuração do Alembic (migrations)
├── main.py                 # Ponto de entrada da aplicação FastAPI
├── petto.db                # Arquivo do banco de dados SQLite
├── README.md               # Documentação do projeto
└── requirements.txt        # Lista de dependências Python

------------------------------------------------------------------------------------
        📥 Instalação
1. Clone o repositório
    git clone https://github.com/klawwwz/Petto-API.git
    cd Petto

2. Crie e ative o ambiente virtual
    python -m venv venv

    #Windows:
    venv\Scripts\activate

    #Linux/Mac:
    source venv/bin/activate

3. Instale as dependências
    pip install -r requirements.txt

4. Configure o ambiente
    cp .env.example .env
    #Edite o .env com suas configurações

        🚀 Execução:
1. Aplique as migrations do banco
    alembic upgrade head

2. (Opcional) Carregue dados iniciais
    python app/seeders/run_seeders.py

3. Inicie o servidor
    uvicorn main:app --reload --host 0.0.0.0 --port 8000