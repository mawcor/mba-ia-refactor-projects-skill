from flask import request, jsonify
from database import db
from models.user import User
from models.task import Task
from utils.error_handler import APIError
import re

class UserController:
    @staticmethod
    def get_users():
        users = User.query.all()
        result = []
        for u in users:
            user_data = {
                'id': u.id,
                'name': u.name,
                'email': u.email,
                'role': u.role,
                'active': u.active,
                'created_at': str(u.created_at),
                'task_count': len(u.tasks)
            }
            result.append(user_data)
        return jsonify(result), 200

    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:
            raise APIError('Usuário não encontrado', 404)
        
        data = user.to_dict()
        tasks = Task.query.filter_by(user_id=user_id).all()
        data['tasks'] = [t.to_dict() for t in tasks]
        return jsonify(data), 200

    @staticmethod
    def create_user():
        data = request.get_json()
        if not data:
            raise APIError('Dados inválidos', 400)

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')

        if not name:
            raise APIError('Nome é obrigatório', 400)
        if not email:
            raise APIError('Email é obrigatório', 400)
        if not password:
            raise APIError('Senha é obrigatória', 400)

        if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', email):
            raise APIError('Email inválido', 400)

        if len(password) < 4:
            raise APIError('Senha deve ter no mínimo 4 caracteres', 400)

        existing = User.query.filter_by(email=email).first()
        if existing:
            raise APIError('Email já cadastrado', 409)

        if role not in ['user', 'admin', 'manager']:
            raise APIError('Role inválido', 400)

        user = User()
        user.name = name
        user.email = email
        user.set_password(password)
        user.role = role

        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201

    @staticmethod
    def update_user(user_id):
        user = User.query.get(user_id)
        if not user:
            raise APIError('Usuário não encontrado', 404)

        data = request.get_json()
        if not data:
            raise APIError('Dados inválidos', 400)

        if 'name' in data:
            user.name = data['name']

        if 'email' in data:
            if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', data['email']):
                raise APIError('Email inválido', 400)
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                raise APIError('Email já cadastrado', 409)
            user.email = data['email']

        if 'password' in data:
            if len(data['password']) < 4:
                raise APIError('Senha muito curta', 400)
            user.set_password(data['password'])

        if 'role' in data:
            if data['role'] not in ['user', 'admin', 'manager']:
                raise APIError('Role inválido', 400)
            user.role = data['role']

        if 'active' in data:
            user.active = data['active']

        db.session.commit()
        return jsonify(user.to_dict()), 200

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            raise APIError('Usuário não encontrado', 404)

        tasks = Task.query.filter_by(user_id=user_id).all()
        for t in tasks:
            db.session.delete(t)

        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Usuário deletado com sucesso'}), 200

    @staticmethod
    def get_user_tasks(user_id):
        user = User.query.get(user_id)
        if not user:
            raise APIError('Usuário não encontrado', 404)

        tasks = Task.query.filter_by(user_id=user_id).all()
        result = []
        for t in tasks:
            task_data = {
                'id': t.id,
                'title': t.title,
                'description': t.description,
                'status': t.status,
                'priority': t.priority,
                'created_at': str(t.created_at),
                'due_date': str(t.due_date) if t.due_date else None,
                'overdue': t.is_overdue()
            }
            result.append(task_data)

        return jsonify(result), 200

    @staticmethod
    def login():
        data = request.get_json()
        if not data:
            raise APIError('Dados inválidos', 400)

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise APIError('Email e senha são obrigatórios', 400)

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            raise APIError('Credenciais inválidas', 401)

        if not user.active:
            raise APIError('Usuário inativo', 403)

        return jsonify({
            'message': 'Login realizado com sucesso',
            'user': user.to_dict(),
            'token': 'fake-jwt-token-' + str(user.id)
        }), 200
