from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from backend.app import db
from backend.app.models.food import Food, FoodEntry
from datetime import datetime, timedelta

nutrition_bp = Blueprint('nutrition', __name__, url_prefix='/nutrition')

@nutrition_bp.route('/')
@login_required
def index():
    """View nutrition log."""
    # Get today's food entries
    today = datetime.utcnow().date()
    today_entries = FoodEntry.query.filter(
        FoodEntry.user_id == current_user.id,
        db.func.date(FoodEntry.logged_at) == today
    ).order_by(FoodEntry.logged_at.desc()).all()
    
    # Calculate daily totals
    total_calories = sum(e.calories for e in today_entries)
    total_protein = sum(e.protein_g or 0 for e in today_entries)
    total_fat = sum(e.fat_g or 0 for e in today_entries)
    total_carbs = sum(e.carbs_g or 0 for e in today_entries)
    
    # Get BMR for daily calorie recommendation (simplified: 1.5 * BMR)
    bmr = current_user.calculate_bmr()
    daily_target = int(bmr * 1.5) if bmr else 2000
    
    return render_template('nutrition/index.html',
                         today_entries=today_entries,
                         totals={
                             'calories': total_calories,
                             'protein': total_protein,
                             'fat': total_fat,
                             'carbs': total_carbs,
                         },
                         daily_target=daily_target)

@nutrition_bp.route('/log', methods=['GET', 'POST'])
@login_required
def log_food():
    """Log food intake."""
    if request.method == 'POST':
        food_id = request.form.get('food_id', type=int)
        quantity = request.form.get('quantity_grams', type=float)
        meal_type = request.form.get('meal_type', 'snack')
        
        # Validation
        if not food_id or not quantity or quantity <= 0:
            flash('Please select a food and enter a valid quantity.', 'danger')
            return redirect(url_for('nutrition.log_food'))
        
        food = Food.query.get(food_id)
        if not food:
            flash('Selected food not found.', 'danger')
            return redirect(url_for('nutrition.log_food'))
        
        # Create food entry
        entry = FoodEntry(
            user_id=current_user.id,
            food_id=food_id,
            quantity_grams=quantity,
            meal_type=meal_type
        )
        entry.calculate_macros()
        
        db.session.add(entry)
        db.session.commit()
        
        flash(f'Food logged: {food.name} ({quantity}g, {entry.calories} cal)', 'success')
        return redirect(url_for('nutrition.index'))
    
    # Get available foods (you can add more via admin or API)
    foods = Food.query.all()
    
    return render_template('nutrition/log.html', foods=foods)

@nutrition_bp.route('/food/search')
@login_required
def search_foods():
    """Search for foods (API endpoint)."""
    query = request.args.get('q', '').strip()
    
    if len(query) < 2:
        return jsonify([])
    
    foods = Food.query.filter(Food.name.ilike(f'%{query}%')).limit(10).all()
    return jsonify([f.to_dict() for f in foods])

@nutrition_bp.route('/food/add', methods=['POST'])
@login_required
def add_custom_food():
    """Add a custom food (admin or user-submitted)."""
    name = request.form.get('name', '').strip()
    calories_per_100g = request.form.get('calories_per_100g', type=float)
    protein = request.form.get('protein_g', type=float)
    fat = request.form.get('fat_g', type=float)
    carbs = request.form.get('carbs_g', type=float)
    
    if not name or not calories_per_100g:
        flash('Please fill in all required fields.', 'danger')
        return redirect(url_for('nutrition.log_food'))
    
    # Check if food already exists
    if Food.query.filter_by(name=name).first():
        flash('This food already exists in the database.', 'info')
        return redirect(url_for('nutrition.log_food'))
    
    food = Food(
        name=name,
        calories_per_100g=calories_per_100g,
        protein_g=protein,
        fat_g=fat,
        carbs_g=carbs
    )
    
    db.session.add(food)
    db.session.commit()
    
    flash(f'Food "{name}" added to database.', 'success')
    return redirect(url_for('nutrition.log_food'))

@nutrition_bp.route('/<int:entry_id>/delete', methods=['POST'])
@login_required
def delete_entry(entry_id):
    """Delete a food entry."""
    entry = FoodEntry.query.get_or_404(entry_id)
    
    if entry.user_id != current_user.id:
        flash('You do not have permission to delete this entry.', 'danger')
        return redirect(url_for('nutrition.index'))
    
    db.session.delete(entry)
    db.session.commit()
    flash('Food entry deleted.', 'success')
    return redirect(url_for('nutrition.index'))
