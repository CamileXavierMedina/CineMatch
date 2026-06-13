# 🎬 CineMatch — Diário de Filmes (Auto-Gestão)

## 1. Descrição do Projeto

O **CineMatch** é um diário de filmes minimalista, direto e eficiente, projetado para permitir que os usuários gerenciem suas listas de produções favoritas de forma simplificada e sem a necessidade de autenticação complexa. Desenvolvido com o framework Flask em Python no back-end, o sistema integra-se diretamente com a API pública do **TMDB (The Movie Database)** para a busca de títulos em tempo real, conectando-se a uma base de dados centralizada na nuvem através do **Supabase (PostgreSQL)**.

A proposta do sistema adota uma filosofia de design *clean*, focando 100% na usabilidade e na organização clara. Ao buscar e encontrar produções, os dados são gerenciados dinamicamente via JavaScript no front-end e salvos diretamente em duas colunas ou abas na tela, permitindo monitorar o histórico e os desejos cinematográficos de forma instantânea.

---

## 2. Principais Funcionalidades e Telas

* **🔍 Barra de Busca Global (TMDB):** Interface direta integrada ao catálogo mundial do TMDB. Ao digitar o nome de um filme, o sistema consome a API de cinema em tempo real para trazer títulos, sinopses, anos de lançamento e imagens das capas.
* **📌 Aba "Quero Assistir":** Funciona como uma lista de desejos (*wishlist*) para planejar as próximas produções que o usuário pretende ver (armazenada no banco com nota igual a 0 ou NULL).
* **⭐ Aba "Já Assisti":** Espaço focado no histórico de filmes já visualizados, contendo um sistema de avaliação interativo onde o usuário atribui uma nota de 1 a 5 estrelas.
* **📊 Painel de Gerenciamento Unificado:** Layout responsivo estruturado em duas colunas ou abas na tela principal, permitindo que o usuário gerencie e visualize suas duas listas simultaneamente sem recarregar a página (comunicação assíncrona via Fetch API).

---

## 3. Tecnologias Utilizadas

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

## 4. Estrutura de Pastas do Projeto

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
│
├── .env.example            # Exemplo de variáveis de ambiente do projeto
├── .gitignore              # Arquivos ignorados pelo Git (venv, chaves, cache)
├── app.py                  # Servidor principal Flask e definição
