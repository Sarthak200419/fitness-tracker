from backend.app import db
from datetime import datetime, timedelta

class GamificationState(db.Model):
    """User's gamification progress (XP, Levels, Streaks)."""
    __tablename__ = 'gamification_state'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    
    # XP and Level system
    total_xp = db.Column(db.Integer, default=0)
    current_level = db.Column(db.Integer, default=1)
    xp_in_current_level = db.Column(db.Integer, default=0)
    
    # Streak tracking
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_activity_date = db.Column(db.Date, nullable=True)
    
    # Milestone tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_xp_for_next_level(self):
        """Calculate XP required for next level."""
        # Simple exponential scaling: Level N requires 1000 * N XP
        return 1000 * (self.current_level + 1)
    
    def add_xp(self, amount):
        """Add XP and handle level ups."""
        self.total_xp += amount
        self.xp_in_current_level += amount
        
        xp_required = self.get_xp_for_next_level()
        
        # Check for level ups
        while self.xp_in_current_level >= xp_required:
            self.current_level += 1
            self.xp_in_current_level -= xp_required
            xp_required = self.get_xp_for_next_level()
        
        return self.current_level
    
    def update_streak(self):
        """Update streak based on last activity."""
        today = datetime.utcnow().date()
        
        if self.last_activity_date is None:
            self.current_streak = 1
        elif self.last_activity_date == today:
            # Already active today
            pass
        elif self.last_activity_date == today - timedelta(days=1):
            # Consecutive day
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
        else:
            # Streak broken
            self.current_streak = 1
        
        self.last_activity_date = today
    
    def to_dict(self):
        """Convert to dictionary for JSON responses."""
        return {
            'total_xp': self.total_xp,
            'current_level': self.current_level,
            'xp_in_current_level': self.xp_in_current_level,
            'xp_for_next_level': self.get_xp_for_next_level(),
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'last_activity_date': self.last_activity_date.isoformat() if self.last_activity_date else None,
        }
    
    def __repr__(self):
        return f'<GamificationState Level {self.current_level} - {self.total_xp} XP>'

class Badge(db.Model):
    """Badge templates for achievements."""
    __tablename__ = 'badges'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    icon_path = db.Column(db.String(255), nullable=True)  # Path to badge image
    
    # Badge unlock conditions
    condition_type = db.Column(db.String(50), nullable=False)  # 'streak', 'total_xp', 'workouts', 'weight_loss'
    condition_value = db.Column(db.Integer, nullable=False)  # e.g., '7' for 7-day streak
    
    # Relationships
    user_badges = db.relationship('UserBadge', backref='badge', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary for JSON responses."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon_path': self.icon_path,
            'condition_type': self.condition_type,
            'condition_value': self.condition_value,
        }
    
    def __repr__(self):
        return f'<Badge {self.name}>'

class UserBadge(db.Model):
    """User's earned badges."""
    __tablename__ = 'user_badges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'badge_id', name='unique_user_badge'),)
    
    def to_dict(self):
        """Convert to dictionary for JSON responses."""
        return {
            'badge_id': self.badge_id,
            'badge_name': self.badge.name,
            'badge_icon': self.badge.icon_path,
            'earned_at': self.earned_at.isoformat(),
        }
    
    def __repr__(self):
        return f'<UserBadge {self.badge.name}>'
