#!/usr/bin/env python
"""Initialize the database with seed data."""

import sys
sys.path.insert(0, '/backend')

from backend.app import create_app, db
from backend.app.models.food import Food
from backend.app.models.gamification import Badge

def init_db():
    """Initialize database with tables and seed data."""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created")
        
        # Add common foods if not already present
        common_foods = [
            ('Chicken Breast', 165, 31, 3.6, 0),
            ('Salmon', 208, 20, 13, 0),
            ('Egg', 155, 13, 11, 1.1),
            ('Rice', 130, 2.7, 0.3, 28),
            ('Broccoli', 34, 2.8, 0.4, 7),
            ('Apple', 52, 0.3, 0.2, 14),
            ('Banana', 89, 1.1, 0.3, 23),
            ('Milk (1% fat)', 42, 3.4, 1, 4.8),
            ('Greek Yogurt', 59, 10, 0.5, 3.25),
            ('Almonds', 579, 21, 50, 22),
            ('Bread (whole wheat)', 92, 3.6, 1.1, 17),
            ('Peanut Butter', 588, 25, 50, 20),
            ('Olive Oil', 884, 0, 100, 0),
            ('Pasta', 131, 5, 1.1, 25),
            ('Chicken Thigh', 209, 26, 11, 0),
        ]
        
        for name, cal, protein, fat, carbs in common_foods:
            if not Food.query.filter_by(name=name).first():
                food = Food(
                    name=name,
                    calories_per_100g=cal,
                    protein_g=protein,
                    fat_g=fat,
                    carbs_g=carbs
                )
                db.session.add(food)
        
        db.session.commit()
        print(f"✓ Added {len(common_foods)} common foods to database")
        
        # Add badge templates
        badge_templates = [
            ('7-Day Streak', 'Completed 7 consecutive days of activity', 'streak', 7),
            ('14-Day Streak', 'Completed 14 consecutive days of activity', 'streak', 14),
            ('30-Day Streak', 'Completed 30 consecutive days of activity', 'streak', 30),
            ('1000 XP', 'Earned 1000 total experience points', 'total_xp', 1000),
            ('5000 XP', 'Earned 5000 total experience points', 'total_xp', 5000),
            ('10000 XP', 'Earned 10000 total experience points', 'total_xp', 10000),
            ('Level 5', 'Reached level 5', 'level', 5),
            ('Level 10', 'Reached level 10', 'level', 10),
        ]
        
        for name, desc, cond_type, cond_val in badge_templates:
            if not Badge.query.filter_by(name=name).first():
                badge = Badge(
                    name=name,
                    description=desc,
                    condition_type=cond_type,
                    condition_value=cond_val
                )
                db.session.add(badge)
        
        db.session.commit()
        print(f"✓ Added {len(badge_templates)} badge templates")
        
        print("\n✅ Database initialization complete!")

if __name__ == '__main__':
    init_db()
