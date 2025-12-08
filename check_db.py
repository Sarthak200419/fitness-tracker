from backend.app import create_app, db
from backend.app.models.user import User

app = create_app()

with app.app_context():
    users = User.query.all()
    print(f"Total Users: {len(users)}")
    for user in users:
        print(f" - ID: {user.id}, Username: {user.username}, Email: {user.email}")
