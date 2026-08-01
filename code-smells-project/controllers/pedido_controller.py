from flask import request
from models.pedido_model import PedidoModel
from utils.response import success_response, error_response
from config.database import get_db
from http import HTTPStatus

def criar_pedido():
    dados = request.get_json()
    if not dados:
        return error_response("Dados inválidos", HTTPStatus.BAD_REQUEST)

    usuario_id = dados.get("usuario_id")
    itens = dados.get("itens", [])

    if not usuario_id:
        return error_response("Usuario ID é obrigatório", HTTPStatus.BAD_REQUEST)
    if not itens or len(itens) == 0:
        return error_response("Pedido deve ter pelo menos 1 item", HTTPStatus.BAD_REQUEST)

    db = get_db()
    try:
        resultado = PedidoModel.criar_pedido(db, usuario_id, itens)
        return success_response(resultado, "Pedido criado com sucesso", HTTPStatus.CREATED)
    except ValueError as e:
        return error_response(str(e), HTTPStatus.BAD_REQUEST)

def listar_pedidos_usuario(usuario_id):
    db = get_db()
    pedidos = PedidoModel.get_pedidos_usuario(db, usuario_id)
    return success_response(pedidos)

def listar_todos_pedidos():
    db = get_db()
    pedidos = PedidoModel.get_todos_pedidos(db)
    return success_response(pedidos)

def atualizar_status_pedido(pedido_id):
    dados = request.get_json()
    novo_status = dados.get("status", "")

    if novo_status not in ["pendente", "aprovado", "enviado", "entregue", "cancelado"]:
        return error_response("Status inválido", HTTPStatus.BAD_REQUEST)

    db = get_db()
    PedidoModel.atualizar_status_pedido(db, pedido_id, novo_status)
    return success_response(None, "Status atualizado")

def relatorio_vendas():
    db = get_db()
    relatorio = PedidoModel.relatorio_vendas(db)
    return success_response(relatorio)
