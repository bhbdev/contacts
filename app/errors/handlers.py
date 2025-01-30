from app.models import Page
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    page = Page({ "title": "404", "template": "errors/404.html" })
    return page.render(), 404


@bp.app_errorhandler(500)
def internal_error(error):
    page = Page({ "title": "404", "template": "errors/500.html" })
    return page.render(), 500

