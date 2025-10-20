from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .gemini_client import suggest_recipe


main_bp = Blueprint('main', __name__, template_folder='templates')


@main_bp.route('/')
def index():
return render_template('index.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
return render_template('dashboard.html')


@main_bp.route('/api/suggest', methods=['POST'])
@login_required
def api_suggest():
data = request.get_json() or {}
ingredients_raw = data.get('ingredients', '')
ingredients = [i.strip() for i in ingredients_raw.split(',') if i.strip()]
if not ingredients:
return jsonify({'error': 'Informe ao menos um ingrediente.'}), 400
suggestion = suggest_recipe(ingredients)
return jsonify({'suggestion': suggestion})