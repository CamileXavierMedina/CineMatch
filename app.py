import os
import requests
import unicodedata
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client

# CARREGA AS CONFIGURACOES DO ARQUIVO OCULTO .ENV
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# INICIALIZACAO DO FLASK
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "cinematch_super_secreto_2026").strip()

# CONFIGURACOES DE CONEXAO VIA VARIAVEIS DE AMBIENTE (COM LIMPEZA DE CARACTERES ESPECIAIS)
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "").strip()
TMDB_ACCESS_TOKEN = os.environ.get("TMDB_ACCESS_TOKEN", "").strip()

# VERIFICACAO DE SEGURANCA DAS CREDENCIAIS OBRIGATORIAS
if not SUPABASE_URL or not SUPABASE_KEY or not TMDB_ACCESS_TOKEN:
    print("\n" + "!" * 80)
    print("AVISO DE SEGURANCA: Algumas variaveis de ambiente nao foram encontradas!")
    print("Verifique se o seu arquivo .env esta na raiz do projeto ou se as")
    print("variaveis de ambiente estao devidamente configuradas no servidor.")
    print("!" * 80 + "\n")

# INICIALIZACAO DO CLIENTE SUPABASE
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

# ROTA DA PAGINA INICIAL (PONTE DE ENTRADA)
@app.route("/")
def index():
    return render_template("index.html")

# ROTA DA TELA QUERO ASSISTIR
@app.route("/assistir")
def assistir():
    return render_template("assistir.html")

# ROTA DA TELA JA ASSISTIDOS
@app.route("/assistidos")
def assistidos():
    return render_template("assistidos.html")

# ROTA DE BUSCA DE FILMES NA API DO TMDB
@app.route("/api/buscar", methods=["GET"])
def api_buscar_filme():
    if not TMDB_ACCESS_TOKEN:
        return jsonify({"erro": "Token do TMDB nao configurado no arquivo .env"}), 500

    query_original = request.args.get("query", "")
    
    # NORMALIZACAO DA BUSCA: REMOVE ESPACOS EXTRAS NAS EXTREMIDADES E CONVERTE CARACTERES ESPECIAIS
    # GARANTE COMPATIBILIDADE DE ACENTOS E CAIXA ALTA/BAIXA ENTRE O CORPO DO FLASK E O TMDB
    query = unicodedata.normalize("NFC", query_original).strip()
    if not query:
        return jsonify([])

    try:
        url = "https://api.themoviedb.org/3/search/movie"
        
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
        }
        
        # PARAMETRO LANGUAGE DEFINIDO COMO PT-BR FORCA O TMDB A FAZER A BUSCA USANDO A COLLATION EM PORTUGUES
        # ISSO FAZ COM QUE BUSCAR "CACHORRO", "Cachorro", "CACHÓRRÓ" OU "cáchôrrô" DEVOLVA EXATAMENTE OS MESMOS RESULTADOS!
        params = {
            "query": query,
            "include_adult": "false",
            "language": "pt-BR",
            "page": "1"
        }
        
        resposta = requests.get(url, headers=headers, params=params, timeout=5)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            resultados = []
            for filme in dados.get("results", []):
                poster_url = f"https://image.tmdb.org/t/p/w300{filme.get('poster_path')}" if filme.get("poster_path") else ""
                resultados.append({
                    "tmdb_id": filme.get("id"),
                    "titulo": filme.get("title"),
                    "ano": filme.get("release_date", "").split("-")[0] if filme.get("release_date") else "N/A",
                    "sinopse": filme.get("overview", "Sem sinopse disponivel."),
                    "poster_path": poster_url
                })
            return jsonify(resultados)
        else:
            return jsonify({"erro": f"FALHA DO TMDB (Status {resposta.status_code}): {resposta.text}"}), resposta.status_code
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ROTA PARA SALVAR OU ATUALIZAR FILME NO SUPABASE
@app.route("/api/favoritar", methods=["POST"])
def api_favoritar():
    if not supabase_client:
        return jsonify({"erro": "Cliente Supabase nao inicializado. Verifique URL e KEY no seu .env"}), 500

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "DADOS DE ENTRADA INVALIDOS"}), 400

    tmdb_id = int(dados.get("tmdb_id"))
    titulo = dados.get("titulo")
    poster_path = dados.get("poster_path")
    ano = dados.get("ano")
    sinopse = dados.get("sinopse")
    status = dados.get("status")
    nota = int(dados.get("nota", 0))

    if status not in ["quero", "assistido"]:
        return jsonify({"erro": "STATUS DE SELECAO INVALIDO"}), 400

    try:
        existente = supabase_client.table("filmes_salvos").select("*").eq("tmdb_id", tmdb_id).execute()
        if existente.data:
            supabase_client.table("filmes_salvos").update({
                "status": status,
                "nota": nota,
                "sinopse": sinopse
            }).eq("tmdb_id", tmdb_id).execute()
        else:
            supabase_client.table("filmes_salvos").insert({
                "tmdb_id": tmdb_id,
                "titulo": titulo,
                "poster_path": poster_path,
                "ano": str(ano),
                "sinopse": sinopse,
                "status": status,
                "nota": nota
            }).execute()
        return jsonify({"status": "sucesso"})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ROTA PARA ATUALIZAR STATUS OU NOTA DE UM FILME SALVO
@app.route("/api/atualizar", methods=["POST"])
def api_atualizar():
    if not supabase_client:
        return jsonify({"erro": "Cliente Supabase nao inicializado"}), 500

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "DADOS INVALIDOS"}), 400

    tmdb_id = int(dados.get("tmdb_id"))
    status = dados.get("status")
    nota = int(dados.get("nota", 0))

    try:
        supabase_client.table("filmes_salvos").update({
            "status": status,
            "nota": nota
        }).eq("tmdb_id", tmdb_id).execute()
        return jsonify({"status": "sucesso"})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ROTA PARA LISTAR FILMES SALVOS
@app.route("/api/listar", methods=["GET"])
def api_listar():
    if not supabase_client:
        return jsonify({"erro": "Cliente Supabase nao inicializado. Verifique URL e KEY no .env"}), 500

    try:
        resposta = supabase_client.table("filmes_salvos").select("*").execute()
        return jsonify(resposta.data)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ROTA PARA REMOVER FILME DO SUPABASE
@app.route("/api/remover", methods=["POST"])
def api_remover():
    if not supabase_client:
        return jsonify({"erro": "Cliente Supabase nao inicializado"}), 500

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "DADOS DE ENTRADA INVALIDOS"}), 400

    tmdb_id = int(dados.get("tmdb_id"))

    try:
        supabase_client.table("filmes_salvos").delete().eq("tmdb_id", tmdb_id).execute()
        return jsonify({"status": "sucesso"})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# EXECUCAO DO SERVIDOR
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)