from flask import request
from models.produto_model import ProdutoModel
from utils.response import success_response, error_response
from config.database import get_db
from http import HTTPStatus

def listar_produtos():
    db = get_db()
    produtos = ProdutoModel.get_todos_produtos(db)
    return success_response(produtos)

def buscar_produto(id):
    db = get_db()
    produto = ProdutoModel.get_produto_por_id(db, id)
    if produto:
        return success_response(produto)
    return error_response("Produto não encontrado", HTTPStatus.NOT_FOUND)

def criar_produto():
    dados = request.get_json()
    if not dados:
        return error_response("Dados inválidos", HTTPStatus.BAD_REQUEST)
    
    nome = dados.get("nome")
    preco = dados.get("preco")
    estoque = dados.get("estoque")
    
    if not nome: return error_response("Nome é obrigatório", HTTPStatus.BAD_REQUEST)
    if preco is None: return error_response("Preço é obrigatório", HTTPStatus.BAD_REQUEST)
    if estoque is None: return error_response("Estoque é obrigatório", HTTPStatus.BAD_REQUEST)

    descricao = dados.get("descricao", "")
    categoria = dados.get("categoria", "geral")

    if preco < 0: return error_response("Preço não pode ser negativo", HTTPStatus.BAD_REQUEST)
    if estoque < 0: return error_response("Estoque não pode ser negativo", HTTPStatus.BAD_REQUEST)
    if len(nome) < 2: return error_response("Nome muito curto", HTTPStatus.BAD_REQUEST)
    if len(nome) > 200: return error_response("Nome muito longo", HTTPStatus.BAD_REQUEST)

    categorias_validas = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]
    if categoria not in categorias_validas:
        return error_response(f"Categoria inválida. Válidas: {categorias_validas}", HTTPStatus.BAD_REQUEST)

    db = get_db()
    id = ProdutoModel.criar_produto(db, nome, descricao, preco, estoque, categoria)
    return success_response({"id": id}, "Produto criado", HTTPStatus.CREATED)

def atualizar_produto(id):
    db = get_db()
    produto_existente = ProdutoModel.get_produto_por_id(db, id)
    if not produto_existente:
        return error_response("Produto não encontrado", HTTPStatus.NOT_FOUND)

    dados = request.get_json()
    if not dados: return error_response("Dados inválidos", HTTPStatus.BAD_REQUEST)
    
    nome = dados.get("nome")
    preco = dados.get("preco")
    estoque = dados.get("estoque")

    if not nome: return error_response("Nome é obrigatório", HTTPStatus.BAD_REQUEST)
    if preco is None: return error_response("Preço é obrigatório", HTTPStatus.BAD_REQUEST)
    if estoque is None: return error_response("Estoque é obrigatório", HTTPStatus.BAD_REQUEST)

    descricao = dados.get("descricao", "")
    categoria = dados.get("categoria", "geral")

    if preco < 0: return error_response("Preço não pode ser negativo", HTTPStatus.BAD_REQUEST)
    if estoque < 0: return error_response("Estoque não pode ser negativo", HTTPStatus.BAD_REQUEST)

    ProdutoModel.atualizar_produto(db, id, nome, descricao, preco, estoque, categoria)
    return success_response(None, "Produto atualizado")

def deletar_produto(id):
    db = get_db()
    produto = ProdutoModel.get_produto_por_id(db, id)
    if not produto:
        return error_response("Produto não encontrado", HTTPStatus.NOT_FOUND)

    ProdutoModel.deletar_produto(db, id)
    return success_response(None, "Produto deletado")

def buscar_produtos():
    termo = request.args.get("q", "")
    categoria = request.args.get("categoria", None)
    preco_min = request.args.get("preco_min", None)
    preco_max = request.args.get("preco_max", None)

    if preco_min: preco_min = float(preco_min)
    if preco_max: preco_max = float(preco_max)

    db = get_db()
    resultados = ProdutoModel.buscar_produtos(db, termo, categoria, preco_min, preco_max)
    return success_response(resultados)
