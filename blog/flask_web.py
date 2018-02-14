import os,sys
sys.path.append('/home/jx/flask_web')
from blog.app.factory import create_app,db
from blog.app.db_models import Role,User,Article
from flask_migrate import Migrate
from flask_login import current_user


app=create_app(os.environ.get('CONFIG') or 'default')
migrate=Migrate(app,db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,Role=Role,User=User,Article=Article,current_user=current_user)

@app.cli.command()
def deploy():
    from flask_migrate import upgrade
    upgrade()
    Role.insert_roles()