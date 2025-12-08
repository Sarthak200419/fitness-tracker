import random
from datetime import datetime, timedelta
from backend.app import create_app, db
from backend.app.models.user import User
from backend.app.models.workout import Workout
from backend.app.models.goal import Goal

def seed_data(username="suraj"):
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if not user:
            print(f"User '{username}' not found. Please register first.")
            return

        print(f"Seeding data for user: {user.username}")

        # 1. Update Profile (Required for calorie calc)
        if not user.height_cm:
            user.height_cm = 175
            user.weight_kg = 75
            user.age = 24
            user.gender = 'M'
            print("- Updated physical attributes")

        # 2. Add Workouts (Past 7 days)
        activities = [
            # (name, type, duration_min, intensity, distance_km)
            ("Morning Run", "cardio", 30, "moderate", 5.0),
            ("HIIT Session", "cardio", 45, "vigorous", None),
            ("Upper Body Gym", "strength", 60, "moderate", None),
            ("Yoga Flow", "flexibility", 45, "light", None),
            ("Evening Cycle", "cardio", 40, "moderate", 12.0),
            ("Leg Day", "strength", 50, "vigorous", None),
            ("Sunday Hike", "cardio", 90, "light", 6.0),
        ]

        # Clear existing recent workouts to avoid duplicates if re-run
        # (Optional, but cleaner for demo)
        
        count = 0
        today = datetime.utcnow()
        
        for i, (name, w_type, duration, intensity, dist) in enumerate(activities):
            # Spread over last 7 days
            log_date = today - timedelta(days=i)
            
            # Add some randomness to heart rate
            hr = random.randint(110, 160)
            
            workout = Workout(
                user=user,  # Set relationship directly
                activity_name=name,
                exercise_type=w_type,
                duration_minutes=duration,
                intensity=intensity,
                distance_km=dist,
                heart_rate_avg=hr,
                notes=f"Auto-generated workout #{i+1}",
                logged_at=log_date
            )
            # Calculate calories
            workout.calculate_calories_burned()
            db.session.add(workout)
            count += 1

        print(f"- Added {count} workouts")

        # 3. Add Goals
        # Clear existing goals
        Goal.query.filter_by(user_id=user.id).delete()
        
        goals = [
            Goal(
                user_id=user.id,
                goal_type="activity_minutes",
                target_value=150,
                current_value=0, # Will need logic to summation this, but for now 0
                unit="min",
                goal_period="weekly",
                # Let's mock realistic progress
                is_active=True
            ),
             Goal(
                user_id=user.id,
                goal_type="weight_loss",
                target_value=72,
                current_value=75, 
                unit="kg",
                goal_period="overall",
                is_active=True
            )
        ]
        
        for g in goals:
            db.session.add(g)
        
        print(f"- Added 2 goals")

        try:
            db.session.commit()
            print("SUCCESS: Database seeded successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"ERROR: Failed to commit changes. {str(e)}")

if __name__ == "__main__":
    seed_data()
