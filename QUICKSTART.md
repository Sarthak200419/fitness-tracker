# Quick Start Guide

Get your Fitness Tracker running in minutes!

## 1️⃣ Prerequisites

- Python 3.8+ (or use `python --version` to check)
- Git (optional, for version control)
- Modern web browser (Chrome, Edge, Firefox, Safari)

## 2️⃣ Installation (5 minutes)

### Windows

```bash
# Open PowerShell or Command Prompt
cd "C:\Users\YourUsername\OneDrive\Desktop\Fitness Tracker WebApp"

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database with seed data
python init_db.py

# Run the application
python run.py
```

### Mac/Linux

```bash
cd ~/Desktop/Fitness\ Tracker\ WebApp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run
python run.py
```

## 3️⃣ Access the App

Open your browser and go to:
```
http://localhost:5000
```

## 4️⃣ Create Your Account

1. Click **Register**
2. Enter:
   - Username (min 3 characters)
   - Email address
   - Password (min 6 characters)
3. Click **Register**
4. Go to **Login** and enter your credentials

## 5️⃣ Complete Your Profile

1. Click your username (top right) → **Profile**
2. Enter:
   - **Height** (cm)
   - **Weight** (kg)
   - **Age**
   - **Gender**
3. Click **Save Changes**
4. View your **Basal Metabolic Rate (BMR)** - your daily resting calorie burn

## 6️⃣ Log Your First Workout

1. Click **Activity** → **Log New Workout**
2. Select:
   - **Exercise Type**: Cardio, Strength, etc.
   - **Activity Name**: Running, weight lifting, etc.
   - **Duration**: How many minutes
   - **Intensity**: Light, Moderate, or Vigorous
3. Click **Log Workout**
4. **Congratulations!** 🎉 You earned your first XP!

## 7️⃣ Track Your Nutrition

1. Click **Nutrition** → **Log Meal**
2. Select a food (database includes 15 common foods)
3. Enter quantity in grams
4. Select meal type (breakfast, lunch, dinner, snack)
5. Click **Log Food**
6. View your daily totals against your calorie goal

## 8️⃣ Set a Goal

1. Click **Goals** → **Create New Goal**
2. Choose:
   - **Goal Type**: Weight loss, calorie intake, activity minutes, etc.
   - **Target Value**: Your target (e.g., 2000 cal/day)
   - **Period**: Daily, weekly, monthly, or overall
   - **Target Date**: Optional deadline
3. Click **Create Goal**
4. Track progress from the dashboard

## 9️⃣ View Your Gamification Stats

1. Click **Stats** in the top navigation
2. See your:
   - **Level** and **XP Progress**
   - **Day Streak** (consecutive activity days)
   - **Badges** earned
   - **Detailed Statistics** from the last 30 days

## 🔟 Keep Track of Your Progress

Each day:
- ✅ Log at least one workout → maintain your streak
- ✅ Track your meals
- ✅ Watch your XP grow
- ✅ Unlock new badges
- ✅ Level up!

---

## Common Tasks

### Add a New Food to Database

If the food you want isn't in the database:
1. Go to **Nutrition** → **Log Meal**
2. Scroll to **Add Custom Food**
3. Enter food name and calories per 100g
4. (Optional) Add protein, fat, carbs
5. Click **Add to Database**
6. Now you can log it in future meals!

### Edit or Delete a Workout

1. Go to **Activity**
2. Find the workout you want to modify
3. Click **Edit** to change details, or **Delete** to remove it

### View Weekly Statistics

1. Click **Stats** on top navigation
2. See your weekly workout summary
3. View charts and detailed breakdown

---

## Tips for Success

🎯 **Set Realistic Goals**
- Start with small, achievable goals
- Increase gradually as you progress

🔥 **Build Your Streak**
- Log at least one activity per day
- Streaks boost motivation!

⭐ **Unlock Badges**
- 7, 14, 30-day streaks
- 1000, 5000, 10000 XP milestones
- Reach levels 5, 10, etc.

📊 **Monitor Your Metrics**
- Check your dashboard daily
- Review weekly stats
- Track progress over time

🍎 **Balance Calories**
- Calculate: Calories Burned - Calories Eaten
- Aim for consistent daily pattern

---

## Troubleshooting

### "Port 5000 already in use"
```bash
# Change port in run.py or use:
python -m flask run --port 5001
```

### "Database locked" error
```bash
# Delete old database and reinitialize
rm fitness_tracker.db
python init_db.py
```

### Forgot password?
Currently, passwords can only be reset by creating a new account. Future versions will include password reset functionality.

### Browser won't connect to localhost
- Try: `http://127.0.0.1:5000`
- Check that Flask is still running
- Try a different browser

---

## Project Files Overview

| File/Folder | Purpose |
|---|---|
| `run.py` | Start the application |
| `init_db.py` | Initialize database with seed data |
| `requirements.txt` | Python package dependencies |
| `backend/` | Flask app, database models, routes |
| `frontend/` | HTML templates and CSS/JS |
| `README.md` | Full documentation |
| `DEPLOYMENT.md` | Cloud deployment guide |

---

## Next Steps

### For Development
- Add more foods to the database
- Customize badge conditions
- Add more workout types
- Integrate with Bluetooth devices (see `DEPLOYMENT.md`)

### For Deployment
- Follow `DEPLOYMENT.md` for cloud hosting (Render/Vercel)
- Set up PostgreSQL for production
- Configure environment variables
- Deploy to a live server

### For Features
- Add social sharing
- Export data to CSV
- Mobile app native version
- Integration with Apple Health/Google Fit

---

## Need Help?

- **README.md**: Comprehensive documentation
- **DEPLOYMENT.md**: Cloud hosting guide
- **Code Comments**: Check Python and JavaScript files for implementation details

---

**Happy tracking! 💪**

Start with one small habit today, and build from there. The best fitness tracker is the one you use consistently!
