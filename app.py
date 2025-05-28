from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
DICTIONARY_FILE = 'dictionary.txt'

# --- Utilitários para dicionário ---

def ler_termos():
    if not os.path.exists(DICTIONARY_FILE):
        return {}
    with open(DICTIONARY_FILE, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    termos = {}
    for linha in linhas:
        if ':' in linha:
            termo, definicao = linha.strip().split(':', 1)
            termos[termo] = definicao
    return termos

def salvar_termos(termos):
    with open(DICTIONARY_FILE, 'w', encoding='utf-8') as f:
        for termo, definicao in termos.items():
            f.write(f"{termo}:{definicao}\n")

# --- Rotas ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/equipe')
def equipe():
    return render_template('equipe.html')

@app.route('/fundamentos')
def fundamentos():
    return render_template('fundamentos.html')

@app.route('/perguntas', methods=['GET', 'POST'])
def perguntas():
    resposta = None
    if request.method == 'POST':
        from gemini_api import perguntar_gemini
        pergunta = request.form['pergunta']
        resposta = perguntar_gemini(pergunta)
    return render_template('perguntas.html', resposta=resposta)

@app.route('/dicionario')
def dicionario():
    termos = ler_termos()
    return render_template('dicionario.html', termos=termos)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    termo = request.form['termo']
    definicao = request.form['definicao']
    termos = ler_termos()
    termos[termo] = definicao
    salvar_termos(termos)
    return redirect(url_for('dicionario'))

@app.route('/editar/<termo>', methods=['GET', 'POST'])
def editar(termo):
    termos = ler_termos()
    if request.method == 'POST':
        nova_definicao = request.form['definicao']
        termos[termo] = nova_definicao
        salvar_termos(termos)
        return redirect(url_for('dicionario'))
    return render_template('editar_termo.html', termo=termo, definicao=termos[termo])

@app.route('/deletar/<termo>')
def deletar(termo):
    termos = ler_termos()
    if termo in termos:
        del termos[termo]
        salvar_termos(termos)
    return redirect(url_for('dicionario'))

if __name__ == '__main__':
    app.run(debug=True)
