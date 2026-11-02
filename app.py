
import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Configuração do banco de dados
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql+psycopg://",
            1
        )
    elif DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1
        )
else:
    DATABASE_URL = "sqlite:///beleza_rara.db"

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Modelo de agendamento
class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    servico = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(10), nullable=False)
    horario = db.Column(db.String(5), nullable=False)
    status = db.Column(db.String(20), default="Confirmado")


# Página inicial
@app.route("/")
def inicio():
    return render_template("index.html")


# Cadastro de agendamento
@app.route("/agendar", methods=["GET", "POST"])
def agendar():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        servico = request.form.get("servico", "").strip()
        data = request.form.get("data", "").strip()
        horario = request.form.get("horario", "").strip()

        if not all([nome, telefone, servico, data, horario]):
            return "Preencha todos os campos.", 400

        conflito = Agendamento.query.filter_by(
            data=data,
            horario=horario,
            status="Confirmado"
        ).first()

        if conflito:
            return (
                "Este horário já está ocupado. Escolha outro horário.",
                400
            )

        novo_agendamento = Agendamento(
            nome=nome,
            telefone=telefone,
            servico=servico,
            data=data,
            horario=horario
        )

        db.session.add(novo_agendamento)
        db.session.commit()

        return redirect(url_for("meus_agendamentos"))

    return render_template("agendar.html")


# Consulta de agendamentos com filtro por data
@app.route("/agendamentos")
def meus_agendamentos():
    data_filtro = request.args.get("data", "").strip()

    consulta = Agendamento.query

    if data_filtro:
        consulta = consulta.filter_by(data=data_filtro)

    lista = consulta.order_by(
        Agendamento.data,
        Agendamento.horario
    ).all()

    return render_template(
        "agendamentos.html",
        agendamentos=lista
    )


# Cancelamento de agendamento
@app.route("/cancelar/<int:id>", methods=["POST"])
def cancelar(id):
    agendamento = db.session.get(Agendamento, id)

    if agendamento is None:
        return "Agendamento não encontrado.", 404

    agendamento.status = "Cancelado"
    db.session.commit()

    return redirect(url_for("meus_agendamentos"))


# Criação das tabelas do banco de dados
with app.app_context():
    db.create_all()


# Execução local
if __name__ == "__main__":
    app.run(debug=True)
