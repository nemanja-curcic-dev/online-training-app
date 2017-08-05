from app import return_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = return_app()

migrate = Migrate(app=app, db=db)

manager = Manager(app=app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
