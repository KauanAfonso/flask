from flask import Flask, render_template, request, redirect, url_for
from models import db,User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#inicializando o banco
db.init_app(app)

#Se não tiver o banco ele cria
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    users = User.query.all()
    return render_template(
        'index.html', users=users
    ) 

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        try:
            nome = request.form['nome']
            email = request.form['email']
            if not nome or not email:
                return render_template('register.html', erro="Por favor, preencha todos os campos.")
            new_user = User(nome=nome, email=email)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('home'))

        except Exception as e:
            # Você pode logar o erro aqui para debug:
            print(f"Erro ao registrar usuário: {e}")
            return render_template("register.html", erro='Erro ao registrar usuário.')
    
    return render_template('register.html')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    try:
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('index.html', users=User.query.all(), erro='Usuário não encontrado.')
    except Exception as e:
        print(f"Erro ao deletar usuário: {e}")
        return render_template('index.html', users=User.query.all(), erro='Erro ao deletar usuário.')

    
@app.route("/update/<int:id>", methods=["POST, GET"])
def edit_user():
    try:
        user = User.query.get_or_404(id)
        if request.method == "POST":
            user.nome = request.form['nome']
            user.email = request.form['email']
            return redirect(url_for('index'))
        return render_template('edit_user.html', user=user)

    except Exception as e:
        print(f"Erro ao atualizar usuário: {e}")
        return render_template("index.html", erro='Erro ao atualizar usuário.')