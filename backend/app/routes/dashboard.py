from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from backend.app import db
from backend.app.models.workout import Workout
from backend.app.models.food import FoodEntry, Food
from backend.app.models.goal import Goal
from backend.app.models.gamification import GamificationState
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    """Main dashboard view."""
    # Get user's gamification state
    gamification = current_user.gamification_state or GamificationState(user_id=current_user.id)
    
    # Get today's activity
    today = datetime.utcnow().date()
    today_workouts = Workout.query.filter(
        Workout.user_id == current_user.id,
        db.func.date(Workout.logged_at) == today
    ).all()
    
    today_food = FoodEntry.query.filter(
        FoodEntry.user_id == current_user.id,
        db.func.date(FoodEntry.logged_at) == today
    ).all()
    
    # Calculate totals
    total_calories_burned = sum(w.calories_burned or 0 for w in today_workouts)
    total_calories_eaten = sum(f.calories for f in today_food)
    total_workouts = len(today_workouts)
    
    # Get active goals
    active_goals = Goal.query.filter_by(user_id=current_user.id, is_active=True).all()
    
    # Get recent activity
    recent_workouts = Workout.query.filter_by(user_id=current_user.id).order_by(
        Workout.logged_at.desc()
    ).limit(5).all()
    
    return render_template('dashboard/index.html',
                         gamification=gamification,
                         today_stats={
                             'workouts': total_workouts,
                             'calories_burned': total_calories_burned,
                             'calories_eaten': total_calories_eaten,
                         },
                         active_goals=active_goals,
                         recent_workouts=recent_workouts)

@dashboard_bp.route('/stats')
@login_required
def stats():
    """Detailed statistics view."""
    # Get last 30 days of data
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    workouts = Workout.query.filter(
        Workout.user_id == current_user.id,
        Workout.logged_at >= thirty_days_ago
    ).order_by(Workout.logged_at.desc()).all()
    
    # Calculate weekly stats
    weekly_stats = {}
    for workout in workouts:
        week_key = workout.logged_at.strftime('%Y-W%W')
        if week_key not in weekly_stats:
            weekly_stats[week_key] = {
                'workouts': 0,
                'calories': 0,
                'duration': 0
            }
        weekly_stats[week_key]['workouts'] += 1
        weekly_stats[week_key]['calories'] += workout.calories_burned or 0
        weekly_stats[week_key]['duration'] += workout.duration_minutes
    
    return render_template('dashboard/stats.html', 
                         weekly_stats=weekly_stats,
                         recent_workouts=workouts)
