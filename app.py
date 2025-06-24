from flask import Flask, render_template, request

nomes = [
    "Kauan",
    "pedro",
    "Henrique"
]
app = Flask(__name__)

@app.route('/')
def home():
    return render_template(
        'index.html', nomes=nomes
    ) 

@app.route("/", methods=["POST"])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email']
    return render_template("nomes.html", nomes=nomes, nome=nome, email=email)

