from flask import request
from models.usuario_model import UsuarioModel
from utils.response import success_response, error_response
from config.database import get_db
from http import HTTPStatus

def listar_usuarios():
    db = get_db()
    usuarios = UsuarioModel.get_todos_usuarios(db)
    return success_response(usuarios)

def buscar_usuario(id):
    db = get_db()
    usuario = UsuarioModel.get_usuario_por_id(db, id)
    if usuario:
        return success_response(usuario)
    return error_response("Usuário não encontrado", HTTPStatus.NOT_FOUND)

def criar_usuario():
    dados = request.get_json()
    if not dados:
        return error_response("Dados inválidos", HTTPStatus.BAD_REQUEST)

    nome = dados.get("nome", "")
    email = dados.get("email", "")
    senha = dados.get("senha", "")

    if not nome or not email or not senha:
        return error_response("Nome, email e senha são obrigatórios", HTTPStatus.BAD_REQUEST)

    db = get_db()
    id = UsuarioModel.criar_usuario(db, nome, email, senha)
    return success_response({"id": id}, "Usuário criado", HTTPStatus.CREATED)

def login():
    dados = request.get_json()
    email = dados.get("email", "")
    senha = dados.get("senha", "")

    if not email or not senha:
        return error_response("Email e senha são obrigatórios", HTTPStatus.BAD_REQUEST)

    db = get_db()
    usuario = UsuarioModel.login_usuario(db, email, senha)
    if usuario:
        return success_response(usuario, "Login OK")
    return error_response("Email ou senha inválidos", HTTPStatus.UNAUTHORIZED)
