from backend.app import db
from datetime import datetime

class Food(db.Model):
    """Food database model for storing food information."""
    __tablename__ = 'foods'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True, index=True)
    calories_per_100g = db.Column(db.Float, nullable=False)
    protein_g = db.Column(db.Float, nullable=True)
    fat_g = db.Column(db.Float, nullable=True)
    carbs_g = db.Column(db.Float, nullable=True)
    
    # Relationships
    food_entries = db.relationship('FoodEntry', backref='food', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary for JSON responses."""
        return {
            'id': self.id,
            'name': self.name,
            'calories_per_100g': self.calories_per_100g,
            'protein_g': self.protein_g,
            'fat_g': self.fat_g,
            'carbs_g': self.carbs_g,
        }
    
    def __repr__(self):
        return f'<Food {self.name}>'

class FoodEntry(db.Model):
    """User's food consumption log."""
    __tablename__ = 'food_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)
    
    # Serving information
    quantity_grams = db.Column(db.Float, nullable=False)  # Weight in grams
    meal_type = db.Column(db.String(20), nullable=True)  # 'breakfast', 'lunch', 'dinner', 'snack'
    
    # Calculated nutritional values for this serving
    calories = db.Column(db.Float, nullable=False)
    protein_g = db.Column(db.Float, nullable=True)
    fat_g = db.Column(db.Float, nullable=True)
    carbs_g = db.Column(db.Float, nullable=True)
    
    # Metadata
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def calculate_macros(self):
        """Calculate nutritional values based on serving size."""
        if not self.food:
            return False
        
        factor = self.quantity_grams / 100.0
        self.calories = round(self.food.calories_per_100g * factor, 2)
        
        if self.food.protein_g:
            self.protein_g = round(self.food.protein_g * factor, 2)
        if self.food.fat_g:
            self.fat_g = round(self.food.fat_g * factor, 2)
        if self.food.carbs_g:
            self.carbs_g = round(self.food.carbs_g * factor, 2)
        
        return True
    
    def to_dict(self):
        """Convert to dictionary for JSON responses."""
        return {
            'id': self.id,
            'food_name': self.food.name,
            'quantity_grams': self.quantity_grams,
            'meal_type': self.meal_type,
            'calories': self.calories,
            'protein_g': self.protein_g,
            'fat_g': self.fat_g,
            'carbs_g': self.carbs_g,
            'logged_at': self.logged_at.isoformat(),
        }
    
    def __repr__(self):
        return f'<FoodEntry {self.food.name} - {self.quantity_grams}g>'
