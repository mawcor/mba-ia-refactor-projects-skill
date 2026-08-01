from flask import Blueprint
from controllers.user_controller import UserController

user_bp = Blueprint('users', __name__)

user_bp.route('/users', methods=['GET'])(UserController.get_users)
user_bp.route('/users/<int:user_id>', methods=['GET'])(UserController.get_user)
user_bp.route('/users', methods=['POST'])(UserController.create_user)
user_bp.route('/users/<int:user_id>', methods=['PUT'])(UserController.update_user)
user_bp.route('/users/<int:user_id>', methods=['DELETE'])(UserController.delete_user)
user_bp.route('/users/<int:user_id>/tasks', methods=['GET'])(UserController.get_user_tasks)
user_bp.route('/login', methods=['POST'])(UserController.login)
