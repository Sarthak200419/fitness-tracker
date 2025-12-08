from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from backend.app import db
from backend.app.models.goal import Goal
from datetime import datetime, timedelta

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')

@goals_bp.route('/')
@login_required
def index():
    """View all goals."""
    active_goals = Goal.query.filter_by(user_id=current_user.id, is_active=True).all()
    completed_goals = Goal.query.filter_by(user_id=current_user.id, is_active=False).all()
    
    return render_template('goals/index.html',
                         active_goals=active_goals,
                         completed_goals=completed_goals)

@goals_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_goal():
    """Create a new goal."""
    if request.method == 'POST':
        goal_type = request.form.get('goal_type', '').strip()
        target_value = request.form.get('target_value', type=float)
        unit = request.form.get('unit', '').strip()
        goal_period = request.form.get('goal_period', 'monthly')
        target_date = request.form.get('target_date')
        
        # Validation
        if not goal_type or not target_value or target_value <= 0 or not unit:
            flash('Please fill in all required fields correctly.', 'danger')
            return redirect(url_for('goals.create_goal'))
        
        # Parse target date if provided
        target_datetime = None
        if target_date:
            try:
                target_datetime = datetime.strptime(target_date, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format.', 'danger')
                return redirect(url_for('goals.create_goal'))
        
        goal = Goal(
            user_id=current_user.id,
            goal_type=goal_type,
            target_value=target_value,
            unit=unit,
            goal_period=goal_period,
            target_date=target_datetime
        )
        
        db.session.add(goal)
        db.session.commit()
        
        flash(f'Goal created: {goal_type} - {target_value} {unit}', 'success')
        return redirect(url_for('goals.index'))
    
    return render_template('goals/create.html')

@goals_bp.route('/<int:goal_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_goal(goal_id):
    """Edit a goal."""
    goal = Goal.query.get_or_404(goal_id)
    
    if goal.user_id != current_user.id:
        flash('You do not have permission to edit this goal.', 'danger')
        return redirect(url_for('goals.index'))
    
    if request.method == 'POST':
        goal.goal_type = request.form.get('goal_type', '').strip()
        goal.target_value = request.form.get('target_value', type=float)
        goal.unit = request.form.get('unit', '').strip()
        goal.goal_period = request.form.get('goal_period', 'monthly')
        
        target_date = request.form.get('target_date')
        if target_date:
            try:
                goal.target_date = datetime.strptime(target_date, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format.', 'danger')
                return redirect(url_for('goals.edit_goal', goal_id=goal_id))
        
        db.session.commit()
        flash('Goal updated successfully.', 'success')
        return redirect(url_for('goals.index'))
    
    return render_template('goals/edit.html', goal=goal)

@goals_bp.route('/<int:goal_id>/delete', methods=['POST'])
@login_required
def delete_goal(goal_id):
    """Delete a goal."""
    goal = Goal.query.get_or_404(goal_id)
    
    if goal.user_id != current_user.id:
        flash('You do not have permission to delete this goal.', 'danger')
        return redirect(url_for('goals.index'))
    
    db.session.delete(goal)
    db.session.commit()
    flash('Goal deleted.', 'success')
    return redirect(url_for('goals.index'))

@goals_bp.route('/<int:goal_id>/update-progress', methods=['POST'])
@login_required
def update_progress(goal_id):
    """Update goal progress."""
    goal = Goal.query.get_or_404(goal_id)
    
    if goal.user_id != current_user.id:
        return {'error': 'Unauthorized'}, 403
    
    current_value = request.form.get('current_value', type=float)
    goal.current_value = current_value
    
    db.session.commit()
    
    return {'success': True, 'progress': goal.progress_percentage()}
