
import pytest

from app import app, db, Agendamento


@pytest.fixture
def cliente_teste(tmp_path):
    banco_teste = tmp_path / "teste.db"

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///" + str(banco_teste).replace("\\", "/")
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.test_client() as cliente:
        yield cliente

    with app.app_context():
        db.session.remove()
        db.drop_all()


def dados_agendamento(**alteracoes):
    dados = {
        "nome": "Maria Silva",
        "telefone": "11999999999",
        "servico": "Corte",
        "data": "2026-11-10",
        "horario": "10:00",
    }
    dados.update(alteracoes)
    return dados


def test_pagina_inicial_abre(cliente_teste):
    resposta = cliente_teste.get("/")
    assert resposta.status_code == 200


def test_cadastrar_agendamento(cliente_teste):
    resposta = cliente_teste.post(
        "/agendar",
        data=dados_agendamento(),
        follow_redirects=True,
    )

    assert resposta.status_code == 200

    with app.app_context():
        agendamento = Agendamento.query.first()
        assert agendamento is not None
        assert agendamento.nome == "Maria Silva"
        assert agendamento.status == "Confirmado"


def test_impedir_horario_duplicado(cliente_teste):
    cliente_teste.post("/agendar", data=dados_agendamento())

    resposta = cliente_teste.post(
        "/agendar",
        data=dados_agendamento(nome="Ana Souza"),
    )

    assert resposta.status_code == 400
    assert b"hor" in resposta.data.lower()

    with app.app_context():
        assert Agendamento.query.count() == 1


def test_cancelar_agendamento(cliente_teste):
    cliente_teste.post("/agendar", data=dados_agendamento())

    with app.app_context():
        agendamento = Agendamento.query.first()
        agendamento_id = agendamento.id

    resposta = cliente_teste.post(
        f"/cancelar/{agendamento_id}",
        follow_redirects=True,
    )

    assert resposta.status_code == 200

    with app.app_context():
        agendamento = db.session.get(Agendamento, agendamento_id)
        assert agendamento.status == "Cancelado"


def test_campos_obrigatorios(cliente_teste):
    resposta = cliente_teste.post(
        "/agendar",
        data={"nome": "Maria Silva"},
    )

    assert resposta.status_code == 400
    assert b"Preencha todos os campos" in resposta.data
