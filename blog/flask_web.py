import os
import click
from blog.app.factory import create_app,db
from blog.app.db_models import Role,User
from flask_migrate import Migrate

app=create_app(os.environ.get('CONFIG') or 'default')
migrate=Migrate(app,db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,Role=Role,User=User)

