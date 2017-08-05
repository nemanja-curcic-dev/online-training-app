from app import return_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models import Users

app = return_app('development')

migrate = Migrate(app=app, db=db)


def make_shell_context():
    return dict(app=app, db=db, Users=Users)


manager = Manager(app=app)
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
