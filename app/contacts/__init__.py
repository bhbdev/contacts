from flask import Blueprint

bp = Blueprint('contacts', __name__, template_folder='../templates/contacts')

from app.contacts import routes
