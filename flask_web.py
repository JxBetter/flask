import os,sys
sys.path.append('/home/jx/flask_web')
from blog.app.factory import create_app,db
from blog.app.db_models import Role,User,Article
from flask_migrate import Migrate
from flask_login import current_user
from flask_script import Manager,Shell


app=create_app(os.environ.get('CONFIG') or 'default')
migrate=Migrate(app,db)
manager=Manager(app)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,Role=Role,User=User,Article=Article,current_user=current_user)


@manager.command
def deploy():
    from blog.app.db_models import Role
    db.drop_all()
    db.create_all()
    Role.insert_roles()
    print('ok')

if __name__ =='__main__':
    manager.run()
