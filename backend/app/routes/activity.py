from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from backend.app import db
from backend.app.models.workout import Workout, MET_VALUES
from backend.app.models.gamification import GamificationState
from datetime import datetime

activity_bp = Blueprint('activity', __name__, url_prefix='/activity')

@activity_bp.route('/')
@login_required
def index():
    """View all workouts."""
    page = request.args.get('page', 1, type=int)
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(
        Workout.logged_at.desc()
    ).paginate(page=page, per_page=10)
    
    return render_template('activity/index.html', workouts=workouts)

@activity_bp.route('/log', methods=['GET', 'POST'])
@login_required
def log_activity():
    """Log a new workout."""
    if request.method == 'POST':
        exercise_type = request.form.get('exercise_type', '').strip()
        activity_name = request.form.get('activity_name', '').strip()
        duration = request.form.get('duration_minutes', type=int)
        intensity = request.form.get('intensity', 'moderate')
        distance = request.form.get('distance_km', type=float)
        heart_rate_avg = request.form.get('heart_rate_avg', type=int)
        notes = request.form.get('notes', '').strip()
        
        # Validation
        if not exercise_type or not activity_name or not duration or duration <= 0:
            flash('Please fill in all required fields correctly.', 'danger')
            return redirect(url_for('activity.log_activity'))
        
        # Create workout
        workout = Workout(
            user=current_user,
            exercise_type=exercise_type,
            activity_name=activity_name,
            duration_minutes=duration,
            intensity=intensity,
            distance_km=distance,
            heart_rate_avg=heart_rate_avg,
            notes=notes
        )
        
        # Calculate calories burned
        workout.calculate_calories_burned()
        
        db.session.add(workout)
        db.session.commit()
        
        # Award XP and update streak
        gamification = current_user.gamification_state
        if gamification:
            xp_awarded = duration * 5  # 5 XP per minute of activity
            gamification.add_xp(xp_awarded)
            gamification.update_streak()
            db.session.commit()
            
            flash(f'Workout logged! You earned {xp_awarded} XP.', 'success')
        else:
            flash('Workout logged successfully.', 'success')
        
        return redirect(url_for('activity.index'))
    
    # Pass available activities to template
    return render_template('activity/log.html', activities=list(MET_VALUES.keys()))

@activity_bp.route('/<int:workout_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_activity(workout_id):
    """Edit an existing workout."""
    workout = Workout.query.get_or_404(workout_id)
    
    # Check authorization
    if workout.user_id != current_user.id:
        flash('You do not have permission to edit this workout.', 'danger')
        return redirect(url_for('activity.index'))
    
    if request.method == 'POST':
        workout.exercise_type = request.form.get('exercise_type', '').strip()
        workout.activity_name = request.form.get('activity_name', '').strip()
        workout.duration_minutes = request.form.get('duration_minutes', type=int)
        workout.intensity = request.form.get('intensity', 'moderate')
        workout.distance_km = request.form.get('distance_km', type=float)
        workout.heart_rate_avg = request.form.get('heart_rate_avg', type=int)
        workout.notes = request.form.get('notes', '').strip()
        
        # Recalculate calories
        workout.calculate_calories_burned()
        
        db.session.commit()
        flash('Workout updated successfully.', 'success')
        return redirect(url_for('activity.index'))
    
    return render_template('activity/edit.html', workout=workout, activities=list(MET_VALUES.keys()))

@activity_bp.route('/<int:workout_id>/delete', methods=['POST'])
@login_required
def delete_activity(workout_id):
    """Delete a workout."""
    workout = Workout.query.get_or_404(workout_id)
    
    # Check authorization
    if workout.user_id != current_user.id:
        flash('You do not have permission to delete this workout.', 'danger')
        return redirect(url_for('activity.index'))
    
    db.session.delete(workout)
    db.session.commit()
    flash('Workout deleted successfully.', 'success')
    return redirect(url_for('activity.index'))

@activity_bp.route('/api/mets')
@login_required
def get_mets():
    """API endpoint to get MET values."""
    return jsonify(MET_VALUES)
