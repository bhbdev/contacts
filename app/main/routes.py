from flask import session, request, redirect, url_for, render_template, abort
from jinja2 import TemplateNotFound
from app.models import Page, Contact
from app.helpers import  t_path
from app.main import bp
import random

# index/homepage route
@bp.route("/")
def index():
    return redirect('/contacts')


@bp.route("/theme")
def theme_toggle():
    cur_theme = session.get("theme")
    if cur_theme == "dark":
        session["theme"] = "light"
    else:
        session["theme"] = "dark"
    return redirect(request.referrer or url_for('index'))

# simple page routes
@bp.route('/<path>')
def page(path):
    pg = path.split('/')[-1]
    
    page = Page()
    page.title = pg
    page.template = t_path(f"pages/{pg}.html")
    try:
        content = page.render()
    except TemplateNotFound:
        abort(404)
        
    return content

