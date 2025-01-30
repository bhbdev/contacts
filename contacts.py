
from app import create_app, db
from app.models import Contact
from app.helpers import seeder

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'seeder': seeder, 'Contact': Contact}