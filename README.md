# CineMatch — Diário de Filmes (Auto-Gestão)

## 1. Descrição do Projeto

O **CineMatch** é um diário de filmes minimalista, direto e eficiente, projetado para permitir que os utilizadores gerenciem as suas listas de produções favoritas de forma simplificada e sem a necessidade de autenticação complexa.

Desenvolvido com o framework **Flask** em Python no back-end, o sistema integra-se diretamente com a API pública do **TMDB (The Movie Database)** para a busca de títulos em tempo real, conectando-se a uma base de dados centralizada na nuvem através do **Supabase (PostgreSQL)**.

A proposta do sistema adota um estilo visual inspirado na Netflix (Dark Mode com tons vermelhos vibrantes), focando 100% na usabilidade e na organização clara. Ao buscar e encontrar produções, os dados são gerenciados dinamicamente via JavaScript no front-end por meio de requisições assíncronas, permitindo monitorizar o histórico e os desejos cinematográficos de forma instantânea.

---

# 2. Principais Funcionalidades e Telas

## Tela Principal (`index.html`)

Interface inicial limpa e focada nos cards de ponte para as listas. Os utilizadores podem aceder diretamente à lista de desejos ou ao histórico de críticas.

## Tela Quero Assistir (`assistir.html`)

Uma lista de desejos dedicada para guardar produções que planeia ver no futuro, permitindo mover o filme para a lista de assistidos ou removê-lo a qualquer momento.

## Tela Já Assisti (`assistidos.html`)

Histórico completo das produções cinematográficas já visualizadas pelo utilizador.

Conta com:

- Sistema visual de avaliação por estrelas (1 a 5)
- Criação de críticas pessoais
- Visualização de críticas
- Edição de críticas
- Exclusão de críticas
- Persistência dos dados diretamente na nuvem

---

# 3. Arquitetura do Sistema e Fluxo de Dados

A arquitetura do CineMatch foi desenhada seguindo o modelo cliente-servidor assíncrono para garantir leveza e velocidade, eliminando recarregamentos desnecessários de página (F5) no navegador.

## Camadas do Sistema

### Interface (Front-End)

Camada de apresentação estruturada em:

- HTML5
- CSS3
- Bootstrap 5
- JavaScript Vanilla

Utiliza a Fetch API para enviar e receber dados em segundo plano, atualizando tabelas e modais dinamicamente.

### Back-End (API Gateway)

Servidor desenvolvido em Python com Flask que:

- Expõe rotas RESTful
- Recebe requisições assíncronas
- Consome a API do TMDB
- Filtra dados
- Realiza a persistência no banco de dados

### Serviços Externos e Nuvem

#### TMDB API

Fornece:

- Títulos
- Sinopses
- Anos de lançamento
- Posters
- Metadados dos filmes

#### Supabase Cloud

Banco de dados PostgreSQL hospedado na nuvem responsável pelo armazenamento de:

- Filmes salvos
- Status de acompanhamento
- Notas
- Críticas

---

# 4. Tecnologias Utilizadas

| Categoria | Tecnologia |
|------------|------------|
| Back-end | Python 3.11+ / Flask |
| Consumo de API | Requests |
| Banco de Dados | PostgreSQL (Supabase Cloud) |
| Front-end | HTML5, CSS3, Bootstrap 5 e JavaScript Vanilla |
| Garantia de Qualidade (QA) | Pytest |
| DevOps e Infraestrutura | Docker |
| Hospedagem / Deploy | Render Cloud |

---

# 5. Modelagem de Dados (Banco de Dados)

O script SQL abaixo define a tabela oficial de persistência do projeto.

```sql
CREATE TABLE filmes_salvos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
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

> **Aviso:** O arquivo localizado em `database/schema.sql` serve como documentação e referência. O script deve ser executado diretamente no SQL Editor do Supabase.

---

# 6. Estrutura de Pastas do Projeto

```text
cinematch/
│
├── database/
│   └── schema.sql
│
│
├── templates/
│   ├── index.html
│   ├── assistir.html
│   └── assistidos.html
│
├── tests/
│   └── test_app.py
│
├── .env.example
├── .gitignore
├── app.py
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# 7. Como Executar a Aplicação Localmente

## Pré-requisitos

- Python 3.11 ou superior
- Git instalado

## Clone o Repositório

```bash
git clone https://github.com/CamileXavierMedina/CineMatch.git
```

## Acesse a Pasta do Projeto

```bash
cd CineMatch
```

## Crie um Ambiente Virtual

```bash
python -m venv venv
```

## Ative o Ambiente Virtual

### Windows

```bash
.\venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

## Instale as Dependências

```bash
pip install -r requirements.txt
```

## Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com base no arquivo `.env.example`.

```env
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_anon_do_supabase
TMDB_ACCESS_TOKEN=seu_access_token_do_tmdb
```

## Execute o Servidor

```bash
python app.py
```

## Abra no Navegador

```text
http://127.0.0.1:10000
```

ou

```text
http://127.0.0.1:5000
```

(conforme configuração da aplicação)

---

# 8. Execução via Docker

## Construir a Imagem

```bash
docker build -t cinematch-app .
```

## Executar o Container

```bash
docker run -p 10000:10000 --env-file .env cinematch-app
```

## Acessar a Aplicação

```text
http://localhost:10000
```

---

# 9. Links Úteis do Projeto

## Repositório Oficial

```text
https://github.com/CamileXavierMedina/CineMatch
```

## Aplicação Publicada

```text
Link disponível após conclusão do deploy no Render
```

---

# 10. Equipe de Desenvolvimento

| Integrante | Responsabilidade |
|------------|------------------|
| Camile Xavier Medina | Proprietária do Repositório, Engenharia de Software, Desenvolvimento Back-end e Integrações de API |
| Leticia | Desenvolvimento Front-end, Estruturação de Telas, UX/UI Core e Documentação Técnica |
| Rafael | Administração e Modelagem de Banco de Dados Relacional (PostgreSQL e Supabase Cloud) |
| Larissa | Arquitetura DevOps, Testes Automatizados (Pytest), Docker e Pipeline de Deploy |

---

# Licença

Este projeto foi desenvolvido estritamente para fins académicos, de portfólio pessoal e de aprendizagem contínua.

**Centro Universitário de Brasília (CEUB)**  
**14 de Junho de 2026**
