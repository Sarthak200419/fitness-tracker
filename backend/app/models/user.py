from backend.app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    """User model for authentication and profile management."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Physical attributes for BMR calculation
    height_cm = db.Column(db.Float, nullable=True)  # Height in centimeters
    weight_kg = db.Column(db.Float, nullable=True)  # Current weight in kg
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)  # 'M', 'F', or 'Other'
    
    # Account timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workouts = db.relationship('Workout', backref='user', lazy=True, cascade='all, delete-orphan')
    food_entries = db.relationship('FoodEntry', backref='user', lazy=True, cascade='all, delete-orphan')
    goals = db.relationship('Goal', backref='user', lazy=True, cascade='all, delete-orphan')
    gamification_state = db.relationship('GamificationState', backref='user', uselist=False, cascade='all, delete-orphan')
    user_badges = db.relationship('UserBadge', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def calculate_bmr(self):
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor equation."""
        if not all([self.weight_kg, self.height_cm, self.age, self.gender]):
            return None
        
        if self.gender.upper() == 'M':
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age + 5
        elif self.gender.upper() == 'F':
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age - 161
        else:
            return None
        
        return bmr
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))
