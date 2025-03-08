import os
from app import db
from config.seed import seed_database
from app.models.user import User

def create_admin():
    admin = User.query.filter_by(username=os.getenv('ADMIN_USERNAME')).first()
    if not admin:
        admin = User(
            username=os.getenv('ADMIN_USERNAME'),
            fullname="Quiz Master Admin",
            is_admin=True
        )
        admin.set_password(os.getenv('ADMIN_PASSWORD'))
        db.session.add(admin)
        db.session.commit()
        print("Admin created!")
    else:
        print("Admin already exists!")


def register_commands(app):
    @app.cli.group('db')
    def db_group():
        pass

    @db_group.command('create')
    def create_db():
        db.create_all()
        create_admin()
        print("Database created!")

    @db_group.command('seed')
    def seed_db():
        seed_database()
        print("Database seeded successfully!")