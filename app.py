from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cliente.db"
db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(14), unique=True)
    password = db.Column(db.String(14), unique=True)
    name = db.Column(db.String(14))
    email = db.Column(db.String(14))

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email


class Tweets(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuario = db.Column(db.Integer, nullable=False)
    conteudo = db.Column(db.String(280))
    data = db.Column(DateTime(default = datetime.datetime.utcnow))

    def __init__(self, idUsuario, conteudo, data):
        self.idUsuario = idUsuario
        self.conteudo = conteudo
        self.data = data


class Seguidores(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUsuario = db.Column(db.Integer, nullable=False)
    idSeguido = db.Column(db.Integer, nullable=False)

    def __init__(self, idUsuario, idSeguido):
        self.idUsuario = idUsuario
        self.idSeguido = idSeguido


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    verificaUsuario = Usuario.query.filter_by(username = request.form['usuario'])
    verificaSenha = Usuario.query.filter_by(password = request.form['senha'])
    id = Usuario.id

    if verificaUsuario == True and verificaSenha == True and request.method == 'POST':
        return redirect(url_for('index'))
        return render_template('paginaPrincipal.html', id=id)
    else:
        return redirect(url_for('index'))
        return render_template('index.html')

@app.route('/cadastro', methods=['GET, POST'])
def cadastro():
    if request.method == 'POST':
        usuario = Usuario(request.form['nomeUsuario'], request.form['senha'], request.form['nomeCompleto'], request.form['email'])
        db.session.add(usuario)
        db.commit()
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/paginaPrincipal/<int:id>', methods=['GET, POST'])
def paginaPrincipal(id):
    if request.method == 'GET':
        tweets = Tweets.query.all()
        usuarios = Usuario.query.all()
        seguido = Seguidores.query.filter_by(idUsuario = id)

        return redirect(url_for('index'))
    else:
        novoTweet = Tweets(request.form['idUsuario'], request.form['conteudo'], request.form['data'])

    return render_template('paginaPrincipal.html', tweets=tweets, usuarios=usuarios, seguido=seguido.idSeguidor)

@app.route('novoTweet', methods=['GET, POST'])
def tweet():
    if request.method == 'POST':
        novoTweet = Tweets(request.form['idUsuario'], request.form['conteudo'], request.form['data'])

        return redirect(url_for('index'))

    return render_template('paginaPrincipal.html', novoTweet=novoTweet)
    
@app.route('/excluirTweet/<int:id>', methods=['GET, POST'])
def excluirTweet(id):
    tweet = Tweets.query.get(id)
    db.session.delete(tweet)
    db.session.commit()

    return redirect(url_for('index'))
    return render_template('paginaPrincipal.html')

@app.route('seguirUsuario', methods=['GET, POST'])
def seguirUsuario():
    novoSeguidor = Seguidores(request.form['idUsuario'], request.form['idSeguido'])

    return redirect(url_for('index'))
    return render_template('paginaPrincipal.html')

@app.route('/deixarSeguirUsuario/<int:id>/<int:idS>', methods=['GET, POST'])
def deixarSeguirUsuario(id, idS):
    deixarSeguir = Seguidores.query.get(id, idS)
    db.session.delete(deixarSeguir)
    db.session.commit()

    return redirect(url_for('index'))
    return render_template('paginaPrincipal.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
