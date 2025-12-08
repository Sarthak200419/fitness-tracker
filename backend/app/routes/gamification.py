from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from backend.app.models.gamification import GamificationState, Badge, UserBadge
from backend.app import db

gamification_bp = Blueprint('gamification', __name__, url_prefix='/gamification')

@gamification_bp.route('/dashboard')
@login_required
def dashboard():
    """Gamification dashboard."""
    gamification = current_user.gamification_state or GamificationState(user_id=current_user.id)
    
    # Get user's badges
    user_badges = UserBadge.query.filter_by(user_id=current_user.id).all()
    
    # Get available badges
    all_badges = Badge.query.all()
    
    earned_badge_ids = {ub.badge_id for ub in user_badges}
    
    return render_template('gamification/dashboard.html',
                         gamification=gamification,
                         user_badges=user_badges,
                         all_badges=all_badges,
                         earned_badge_ids=earned_badge_ids)

@gamification_bp.route('/api/status')
@login_required
def get_status():
    """Get gamification status (API endpoint)."""
    gamification = current_user.gamification_state
    if not gamification:
        return jsonify({'error': 'Gamification state not found'}), 404
    
    return jsonify(gamification.to_dict())

def check_and_award_badges(user):
    """Check badge conditions and award badges to user."""
    gamification = user.gamification_state
    
    if not gamification:
        return []
    
    awarded = []
    all_badges = Badge.query.all()
    
    for badge in all_badges:
        # Skip if already earned
        if UserBadge.query.filter_by(user_id=user.id, badge_id=badge.id).first():
            continue
        
        # Check condition
        if badge.condition_type == 'streak' and gamification.current_streak >= badge.condition_value:
            user_badge = UserBadge(user_id=user.id, badge_id=badge.id)
            db.session.add(user_badge)
            awarded.append(badge)
        
        elif badge.condition_type == 'total_xp' and gamification.total_xp >= badge.condition_value:
            user_badge = UserBadge(user_id=user.id, badge_id=badge.id)
            db.session.add(user_badge)
            awarded.append(badge)
        
        elif badge.condition_type == 'level' and gamification.current_level >= badge.condition_value:
            user_badge = UserBadge(user_id=user.id, badge_id=badge.id)
            db.session.add(user_badge)
            awarded.append(badge)
    
    if awarded:
        db.session.commit()
    
    return awarded
