from backend.app import db
from datetime import datetime

class Goal(db.Model):
    """User goals for health objectives."""
    __tablename__ = 'goals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Goal details
    goal_type = db.Column(db.String(50), nullable=False)  # 'weight_loss', 'calorie_intake', 'activity_minutes'
    target_value = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float, nullable=True)
    unit = db.Column(db.String(50), nullable=False)  # 'kg', 'calories', 'minutes', etc.
    
    # Timeframe
    goal_period = db.Column(db.String(20), nullable=False)  # 'daily', 'weekly', 'monthly', 'overall'
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    target_date = db.Column(db.DateTime, nullable=True)
    
    # Metadata
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def progress_percentage(self):
        """Calculate progress as percentage of target."""
        if not self.target_value or self.target_value == 0:
            return 0
        
        if self.current_value is None:
            return 0
        
        # For weight loss goals, we calculate inversely
        if self.goal_type == 'weight_loss':
            progress = ((self.current_value - self.target_value) / self.current_value) * 100
        else:
            progress = (self.current_value / self.target_value) * 100
        
        return min(100, max(0, progress))  # Clamp between 0-100
    
    def is_completed(self):
        """Check if goal has been achieved."""
        if self.current_value is None:
            return False
        
        if self.goal_type == 'weight_loss':
            return self.current_value <= self.target_value
        else:
            return self.current_value >= self.target_value
    
    def to_dict(self):
        """Convert to dictionary for JSON responses."""
        return {
            'id': self.id,
            'goal_type': self.goal_type,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'unit': self.unit,
            'goal_period': self.goal_period,
            'progress_percentage': self.progress_percentage(),
            'is_completed': self.is_completed(),
            'is_active': self.is_active,
            'target_date': self.target_date.isoformat() if self.target_date else None,
        }
    
    def __repr__(self):
        return f'<Goal {self.goal_type} - {self.target_value}{self.unit}>'
