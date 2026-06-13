# 🎬 CineMatch — Diário de Filmes (Auto-Gestão)

## 1. Descrição do Projeto

O **CineMatch** é um diário de filmes minimalista, direto e eficiente, projetado para permitir que os usuários gerenciem suas listas de produções favoritas de forma simplificada e sem a necessidade de autenticação complexa. Desenvolvido com o framework Flask em Python no back-end, o sistema integra-se diretamente com a API pública do **TMDB (The Movie Database)** para a busca de títulos em tempo real, conectando-se a uma base de dados centralizada na nuvem através do **Supabase (PostgreSQL)**.

A proposta do sistema adota uma filosofia de design *clean*, focando 100% na usabilidade e na organização clara. Ao buscar e encontrar produções, os dados são gerenciados dinamicamente via JavaScript no front-end e salvos diretamente em duas colunas ou abas na tela, permitindo monitorar o histórico e os desejos cinematográficos de forma instantânea.

---

## 2. Principais Funcionalidades e Telas

* **🔍 Tela Principal (`index.html`):** Rota inicial do sistema. Contém uma interface direta focada na barra de busca global. Ao digitar o nome de um filme, o sistema consome a API de cinema do TMDB em tempo real e exibe os resultados em cards, com botões para direcionar o filme para uma das listas.
* **📌 Tela Quero Assistir (`quero_assistir.html`):** Uma tela dedicada para listar todos os filmes que o usuário salvou com o desejo de assistir no futuro. Exibe os metadados limpos e opção para remover ou mover para assistidos.
* **⭐ Tela Já Assisti (`assistidos.html`):** Histórico completo das produções cinematográficas já visualizadas pelo usuário, integrando o sistema visual de avaliação por estrelas (nota de 1 a 5).

---

## 3. Arquitetura do Sistema e Fluxo de Dados

A arquitetura do CineMatch foi desenhada seguindo o modelo cliente-servidor assíncrono para garantir leveza e velocidade, eliminando recarregamentos desnecessários de página (F5) no navegador.

### Camadas do Sistema:
1. **Interface (Front-End):** Camada de apresentação construída em HTML5 e CSS3 (Bootstrap 5) para um visual minimalista e responsivo. Utiliza **JavaScript Vanilla** e a **Fetch API** para enviar e receber dados em segundo plano, atualizando o conteúdo da tela de forma reativa.
2. **Back-End (API Gateway):** Servidor construído em **Python com Flask** que expõe rotas RESTful. Ele intercepta as requisições do front-end, consome os metadados da API de Cinema e faz a ponte de persistência com a nuvem.
3. **Serviços Externos e Nuvem:**
   * **TMDB API:** Fornece o catálogo mundial de filmes, títulos, sinopses e imagens de capas.
   * **Supabase Cloud:** Banco de dados relacional **PostgreSQL** hospedado na nuvem que armazena as escolhas, status e notas dos usuários.

---

## 4. Tecnologias Utilizadas

| Categoria | Tecnologia |
| :--- | :--- |
| **Back-end** | Python 3.10+ / Flask |
| **Consumo de API** | Requests (Integração assíncrona com a API do TMDB) |
| **Banco de Dados** | PostgreSQL (Supabase Cloud) |
| **Frontend** | HTML5, CSS3 (Bootstrap 5 / Tailwind) e JavaScript Vanilla |
| **Garantia de Qualidade (QA)** | Pytest (Testes de rotas e integração de APIs) |
| **DevOps e Infraestrutura** | Docker (Containerização de ambiente de produção) |
| **Hospedagem / Deploy** | Render Cloud |

---

## 5. Modelagem de Dados (Banco de Dados)

```
-- Criação da tabela oficial com cláusula de restrição (CHECK) para integridade dos dados
CREATE TABLE filmes_salvos (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tmdb_id INT NOT NULL UNIQUE,
    titulo TEXT NOT NULL,
    poster_path TEXT,
    ano TEXT,
    sinopse TEXT,
    status TEXT NOT NULL CHECK (status IN ('quero', 'assistido')),
    nota INT DEFAULT 0 CHECK (nota >= 0 AND nota <= 5),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 6. Estrutura de Pastas do Projeto

```files
cinematch/
│
├── database/
│   └── schema.sql          # Script SQL de criação da tabela no banco
│
├── static/                 # Arquivos estáticos servidos pelo backend
│   ├── css/
│   │   └── style.css       # Estilizações customizadas e design minimalista
│   └── js/
│       └── main.js         # Manipulação de DOM e chamadas assíncronas (Fetch API)
│
├── templates/              # Estruturas de visualização
│   └── index.html          # Página principal unificada em HTML5
│
├── tests/                  # Suite de testes automatizados
│   └── test_app.py         # Testes lógicos e de integração com pytest 
├── .env.example            # Exemplo de variáveis de ambiente do projeto
├── .gitignore              # Arquivos ignorados pelo Git (venv, chaves, cache)
├── app.py                  # Servidor principal Flask e definição de rotas 
├── Dockerfile              # Configuração do container para ambiente de produção 
├── requirements.txt        # Lista de dependências e bibliotecas do Python
└── README.md               # Documentação técnica do repositório 
```
---

## 7. Como Executar a Aplicação Localmente

### Pré-requisitos
* Python 3.11 ou superior instalado.
* Git para controle de versão.

### Configuração do Ambiente

1. **Clone este repositório para o seu computador:**
   ```bash
   git clone [https://github.com/CamileXavierMedina/CineMatch.git](https://github.com/CamileXavierMedina/CineMatch.git)

2. **Navegue até a pasta raiz do projeto:**

   ```bash
   cd CineMatch

3. **Crie um ambiente virtual isolado para as dependências:**

   ```bash
   python -m venv venv

4. **Ative o ambiente virtual:**

   Windows:

   ```bash
   .\venv\Scripts\activate
   ```
   Linux/macOS:

   ```bash
   source venv/bin/activate
   ```

5. **Instale todas as dependências do projeto:**

   ```bash
   pip install -r requirements.txt
   
6. **Inicie o servidor local de desenvolvimento:**

   ```bash
   python app.py
   ```
   O console indicará que o servidor está rodando. Abra o seu navegador de preferência e acesse:
   ```
   http://127.0.0.1:5000
   ```
--- 
## 8. Execução via Docker (Containerização)

Caso queira compilar e executar a aplicação em um ambiente isolado idêntico ao servidor de produção, certifique-se de ter o Docker instalado.

### Compilação da imagem Docker

```bash
docker build -t cinematch-app .
```

### Execução do container

```bash
docker run -p 10000:10000 cinematch-app
```

Acesse no navegador:

```text
http://localhost:10000
```
---

## 9. Links Úteis do Projeto

### Repositório GitHub

https://github.com/CamileXavierMedina/CineMatch

### Aplicação Publicada (Deploy)

> Inserir aqui o link do Render após o deploy

---

## 10. Equipe de Desenvolvimento

| Integrante               | Responsabilidade                                                                   |
| ------------------------ | -----------------------------------------------------------------------            |
| **Camile Xavier Medina** | Proprietária do Repositório e Desenvolvedora Back-end e frontend (Python & APIs)   |
| **Leticia**              | Desenvolvedora Frontend e Tech Docs (HTML/Bootstrap 5)                             |
| **Rafael**               | Administrador de Banco de Dados (PostgreSQL & Supabase Cloud)                      |
| **Larissa**              | DevOps, Garantia de Qualidade (Pytest) e Deploy (Render & Docker)                  |


##  Licença

Este projeto foi desenvolvido para fins acadêmicos e de aprendizado.

Ceub - 14 de junho de 2026.
