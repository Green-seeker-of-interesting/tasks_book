from flask_script import Shell, Manager

from app import app
from logic import db, migrate
import api

manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, migrate=migrate)

manager.add_command('shell', Shell(make_context=make_shell_context))


if __name__ == "__main__":
    manager.run()