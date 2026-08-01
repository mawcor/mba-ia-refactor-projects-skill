from flask import Blueprint
from controllers.task_controller import TaskController

task_bp = Blueprint('tasks', __name__)

task_bp.route('/tasks', methods=['GET'])(TaskController.get_tasks)
task_bp.route('/tasks/<int:task_id>', methods=['GET'])(TaskController.get_task)
task_bp.route('/tasks', methods=['POST'])(TaskController.create_task)
task_bp.route('/tasks/<int:task_id>', methods=['PUT'])(TaskController.update_task)
task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])(TaskController.delete_task)
task_bp.route('/tasks/search', methods=['GET'])(TaskController.search_tasks)
task_bp.route('/tasks/stats', methods=['GET'])(TaskController.task_stats)
