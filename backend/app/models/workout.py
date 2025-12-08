from backend.app import db
from datetime import datetime

# MET (Metabolic Equivalent of Task) values for various exercises
MET_VALUES = {
    'walking': 3.5,
    'jogging': 7.0,
    'running': 9.8,
    'cycling': 7.5,
    'swimming': 8.0,
    'weight_training': 6.0,
    'yoga': 2.5,
    'pilates': 3.0,
    'hiit': 10.0,
    'rowing': 8.5,
    'elliptical': 5.5,
    'stair_climbing': 9.0,
}

class Workout(db.Model):
    """Workout model for activity tracking."""
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Activity details
    exercise_type = db.Column(db.String(50), nullable=False)  # e.g., 'cardio', 'strength', 'flexibility'
    activity_name = db.Column(db.String(100), nullable=False)  # e.g., 'running', 'bench press'
    duration_minutes = db.Column(db.Integer, nullable=False)  # Duration in minutes
    intensity = db.Column(db.String(20), nullable=True)  # 'light', 'moderate', 'vigorous'
    distance_km = db.Column(db.Float, nullable=True)  # Optional distance for cardio
    
    # Calculated fields
    calories_burned = db.Column(db.Float, nullable=True)
    heart_rate_avg = db.Column(db.Integer, nullable=True)  # Average BPM during workout
    
    # Notes and metadata
    notes = db.Column(db.Text, nullable=True)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_calories_burned(self):
        """Calculate calories burned using MET formula."""
        if not self.user.weight_kg:
            return None
        
        # Get MET value for activity
        met = MET_VALUES.get(self.activity_name.lower(), 5.0)
        
        # Adjust for intensity if provided
        if self.intensity == 'light':
            met *= 0.8
        elif self.intensity == 'vigorous':
            met *= 1.2
        
        # Formula: Calories = MET * Weight (kg) * Duration (hours)
        calories = met * self.user.weight_kg * (self.duration_minutes / 60)
        self.calories_burned = round(calories, 2)
        return self.calories_burned
    
    def to_dict(self):
        """Convert to dictionary for JSON responses."""
        return {
            'id': self.id,
            'exercise_type': self.exercise_type,
            'activity_name': self.activity_name,
            'duration_minutes': self.duration_minutes,
            'intensity': self.intensity,
            'distance_km': self.distance_km,
            'calories_burned': self.calories_burned,
            'heart_rate_avg': self.heart_rate_avg,
            'notes': self.notes,
            'logged_at': self.logged_at.isoformat(),
        }
    
    def __repr__(self):
        return f'<Workout {self.activity_name} - {self.duration_minutes}min>'
