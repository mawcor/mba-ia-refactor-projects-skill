from flask import request, jsonify
from database import db
from models.task import Task
from models.user import User
from models.category import Category
from utils.error_handler import APIError
from datetime import datetime
from sqlalchemy.orm import joinedload

class TaskController:
    @staticmethod
    def get_tasks():
        tasks = Task.query.options(joinedload(Task.user), joinedload(Task.category)).all()
        result = []
        for t in tasks:
            task_data = t.to_dict()
            task_data['overdue'] = t.is_overdue()
            task_data['user_name'] = t.user.name if t.user else None
            task_data['category_name'] = t.category.name if t.category else None
            result.append(task_data)
        return jsonify(result), 200

    @staticmethod
    def get_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            raise APIError('Task não encontrada', 404)
        data = task.to_dict()
        data['overdue'] = task.is_overdue()
        return jsonify(data), 200

    @staticmethod
    def create_task():
        data = request.get_json()
        if not data:
            raise APIError('Dados inválidos', 400)

        title = data.get('title')
        if not title:
            raise APIError('Título é obrigatório', 400)
        if len(title) < 3:
            raise APIError('Título muito curto', 400)
        if len(title) > 200:
            raise APIError('Título muito longo', 400)

        status = data.get('status', 'pending')
        priority = data.get('priority', 3)
        user_id = data.get('user_id')
        category_id = data.get('category_id')
        due_date = data.get('due_date')

        task = Task()
        if not task.validate_status(status):
            raise APIError('Status inválido', 400)
        if not task.validate_priority(priority):
            raise APIError('Prioridade deve ser entre 1 e 5', 400)

        if user_id:
            user = User.query.get(user_id)
            if not user:
                raise APIError('Usuário não encontrado', 404)

        if category_id:
            cat = Category.query.get(category_id)
            if not cat:
                raise APIError('Categoria não encontrada', 404)

        task.title = title
        task.description = data.get('description', '')
        task.status = status
        task.priority = priority
        task.user_id = user_id
        task.category_id = category_id

        if due_date:
            try:
                task.due_date = datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                raise APIError('Formato de data inválido. Use YYYY-MM-DD', 400)

        tags = data.get('tags')
        if tags:
            if isinstance(tags, list):
                task.tags = ','.join(tags)
            else:
                task.tags = tags

        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201

    @staticmethod
    def update_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            raise APIError('Task não encontrada', 404)

        data = request.get_json()
        if not data:
            raise APIError('Dados inválidos', 400)

        if 'title' in data:
            if len(data['title']) < 3:
                raise APIError('Título muito curto', 400)
            if len(data['title']) > 200:
                raise APIError('Título muito longo', 400)
            task.title = data['title']

        if 'description' in data:
            task.description = data['description']

        if 'status' in data:
            if not task.validate_status(data['status']):
                raise APIError('Status inválido', 400)
            task.status = data['status']

        if 'priority' in data:
            if not task.validate_priority(data['priority']):
                raise APIError('Prioridade deve ser entre 1 e 5', 400)
            task.priority = data['priority']

        if 'user_id' in data:
            if data['user_id']:
                user = User.query.get(data['user_id'])
                if not user:
                    raise APIError('Usuário não encontrado', 404)
            task.user_id = data['user_id']

        if 'category_id' in data:
            if data['category_id']:
                cat = Category.query.get(data['category_id'])
                if not cat:
                    raise APIError('Categoria não encontrada', 404)
            task.category_id = data['category_id']

        if 'due_date' in data:
            if data['due_date']:
                try:
                    task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
                except ValueError:
                    raise APIError('Formato de data inválido', 400)
            else:
                task.due_date = None

        if 'tags' in data:
            if isinstance(data['tags'], list):
                task.tags = ','.join(data['tags'])
            else:
                task.tags = data['tags']

        task.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(task.to_dict()), 200

    @staticmethod
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            raise APIError('Task não encontrada', 404)
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deletada com sucesso'}), 200

    @staticmethod
    def search_tasks():
        query = request.args.get('q', '')
        status = request.args.get('status', '')
        priority = request.args.get('priority', '')
        user_id = request.args.get('user_id', '')

        tasks = Task.query

        if query:
            tasks = tasks.filter(
                db.or_(
                    Task.title.like(f'%{query}%'),
                    Task.description.like(f'%{query}%')
                )
            )

        if status:
            tasks = tasks.filter(Task.status == status)

        if priority:
            tasks = tasks.filter(Task.priority == int(priority))

        if user_id:
            tasks = tasks.filter(Task.user_id == int(user_id))

        results = tasks.all()
        return jsonify([t.to_dict() for t in results]), 200

    @staticmethod
    def task_stats():
        total = Task.query.count()
        pending = Task.query.filter_by(status='pending').count()
        in_progress = Task.query.filter_by(status='in_progress').count()
        done = Task.query.filter_by(status='done').count()
        cancelled = Task.query.filter_by(status='cancelled').count()

        all_tasks = Task.query.all()
        overdue_count = sum(1 for t in all_tasks if t.is_overdue())

        stats = {
            'total': total,
            'pending': pending,
            'in_progress': in_progress,
            'done': done,
            'cancelled': cancelled,
            'overdue': overdue_count,
            'completion_rate': round((done / total) * 100, 2) if total > 0 else 0
        }
        return jsonify(stats), 200
