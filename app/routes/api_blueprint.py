
# importar cada blueprint, exemplo:
# from . import products_blueprint, orders_blueprint
from flask import Blueprint

bp = Blueprint('api_bp', __name__, url_prefix='/api')

# registrar cada blueprint, exemplo:
# bp.register_blueprint(products_blueprint.bp)
# bp.register_blueprint(orders_blueprint.bp)
