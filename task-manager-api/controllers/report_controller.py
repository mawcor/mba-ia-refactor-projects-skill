from flask import request, jsonify
from database import db
from models.task import Task
from models.user import User
from models.category import Category
from utils.error_handler import APIError
from datetime import datetime, timedelta
from collections import defaultdict

class ReportController:
    @staticmethod
    def summary_report():
        total_tasks = Task.query.count()
        total_users = User.query.count()
        total_categories = Category.query.count()

        pending = Task.query.filter_by(status='pending').count()
        in_progress = Task.query.filter_by(status='in_progress').count()
        done = Task.query.filter_by(status='done').count()
        cancelled = Task.query.filter_by(status='cancelled').count()

        p1 = Task.query.filter_by(priority=1).count()
        p2 = Task.query.filter_by(priority=2).count()
        p3 = Task.query.filter_by(priority=3).count()
        p4 = Task.query.filter_by(priority=4).count()
        p5 = Task.query.filter_by(priority=5).count()

        all_tasks = Task.query.all()
        overdue_count = 0
        overdue_list = []
        user_tasks_map = defaultdict(list)
        
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_tasks = 0
        recent_done = 0

        for t in all_tasks:
            if t.user_id:
                user_tasks_map[t.user_id].append(t)
            
            if t.is_overdue():
                overdue_count += 1
                overdue_list.append({
                    'id': t.id,
                    'title': t.title,
                    'due_date': str(t.due_date),
                    'days_overdue': (datetime.utcnow() - t.due_date).days
                })
            
            if t.created_at and t.created_at >= seven_days_ago:
                recent_tasks += 1
            
            if t.status == 'done' and t.updated_at and t.updated_at >= seven_days_ago:
                recent_done += 1

        users = User.query.all()
        user_stats = []
        for u in users:
            u_tasks = user_tasks_map[u.id]
            total = len(u_tasks)
            completed = sum(1 for t in u_tasks if t.status == 'done')
            user_stats.append({
                'user_id': u.id,
                'user_name': u.name,
                'total_tasks': total,
                'completed_tasks': completed,
                'completion_rate': round((completed / total) * 100, 2) if total > 0 else 0
            })

        report = {
            'generated_at': str(datetime.utcnow()),
            'overview': {
                'total_tasks': total_tasks,
                'total_users': total_users,
                'total_categories': total_categories,
            },
            'tasks_by_status': {
                'pending': pending,
                'in_progress': in_progress,
                'done': done,
                'cancelled': cancelled,
            },
            'tasks_by_priority': {
                'critical': p1,
                'high': p2,
                'medium': p3,
                'low': p4,
                'minimal': p5,
            },
            'overdue': {
                'count': overdue_count,
                'tasks': overdue_list,
            },
            'recent_activity': {
                'tasks_created_last_7_days': recent_tasks,
                'tasks_completed_last_7_days': recent_done,
            },
            'user_productivity': user_stats,
        }
        return jsonify(report), 200

    @staticmethod
    def user_report(user_id):
        user = User.query.get(user_id)
        if not user:
            raise APIError('Usuário não encontrado', 404)

        tasks = Task.query.filter_by(user_id=user_id).all()
        total = len(tasks)
        done = sum(1 for t in tasks if t.status == 'done')
        pending = sum(1 for t in tasks if t.status == 'pending')
        in_progress = sum(1 for t in tasks if t.status == 'in_progress')
        cancelled = sum(1 for t in tasks if t.status == 'cancelled')
        overdue = sum(1 for t in tasks if t.is_overdue())
        high_priority = sum(1 for t in tasks if t.priority <= 2)

        report = {
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
            },
            'statistics': {
                'total_tasks': total,
                'done': done,
                'pending': pending,
                'in_progress': in_progress,
                'cancelled': cancelled,
                'overdue': overdue,
                'high_priority': high_priority,
                'completion_rate': round((done / total) * 100, 2) if total > 0 else 0
            }
        }
        return jsonify(report), 200

    @staticmethod
    def get_categories():
        categories = Category.query.all()
        result = []
        for c in categories:
            cat_data = c.to_dict()
            cat_data['task_count'] = Task.query.filter_by(category_id=c.id).count()
            result.append(cat_data)
        return jsonify(result), 200

    @staticmethod
    def create_category():
        data = request.get_json()
        if not data:
            raise APIError('Dados inválidos', 400)

        name = data.get('name')
        if not name:
            raise APIError('Nome é obrigatório', 400)

        category = Category()
        category.name = name
        category.description = data.get('description', '')
        category.color = data.get('color', '#000000')

        db.session.add(category)
        db.session.commit()
        return jsonify(category.to_dict()), 201

    @staticmethod
    def update_category(cat_id):
        cat = Category.query.get(cat_id)
        if not cat:
            raise APIError('Categoria não encontrada', 404)

        data = request.get_json()
        if not data:
            raise APIError('Dados inválidos', 400)

        if 'name' in data:
            cat.name = data['name']
        if 'description' in data:
            cat.description = data['description']
        if 'color' in data:
            cat.color = data['color']

        db.session.commit()
        return jsonify(cat.to_dict()), 200

    @staticmethod
    def delete_category(cat_id):
        cat = Category.query.get(cat_id)
        if not cat:
            raise APIError('Categoria não encontrada', 404)

        db.session.delete(cat)
        db.session.commit()
        return jsonify({'message': 'Categoria deletada'}), 200
