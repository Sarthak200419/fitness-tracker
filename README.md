# Fitness Tracker WebApp

A gamified fitness and health tracker web application built with Flask and PostgreSQL. Track workouts, nutrition, and achieve fitness goals while earning XP and badges!

## Features

- 💪 **Activity Tracking**: Log workouts with MET-based calorie calculations
- 🍽️ **Nutrition Tracking**: Monitor daily calories and macronutrients
- 🎮 **Gamification**: Earn XP, level up, and unlock badges
- 🎯 **Goal Management**: Set and track personal fitness objectives
- ❤️ **Bluetooth Integration**: Connect smart devices for real-time heart rate monitoring
- 📊 **Analytics Dashboard**: Visualize progress with charts and statistics
- 🔐 **Secure Authentication**: User registration and login with password hashing

## Technology Stack

- **Backend**: Python 3.x, Flask 2.3
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Jinja2 templating
- **Authentication**: Flask-Login, Werkzeug
- **ORM**: SQLAlchemy
- **Deployment**: Render, Vercel-compatible

## Project Structure

```
Fitness Tracker WebApp/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models (User, Workout, Food, Goal, Badge)
│   │   ├── routes/          # API endpoints and views
│   │   ├── utils/           # Helper functions
│   │   └── __init__.py      # Flask app factory
│   ├── config.py            # Configuration management
│   └── __init__.py
├── frontend/
│   ├── templates/           # Jinja2 HTML templates
│   │   ├── auth/            # Login, register, profile
│   │   ├── dashboard/       # Main dashboard
│   │   ├── activity/        # Workout logging
│   │   ├── nutrition/       # Food tracking
│   │   ├── goals/           # Goal management
│   │   ├── gamification/    # Stats and badges
│   │   └── base.html        # Base template
│   └── static/
│       ├── css/             # Stylesheets
│       ├── js/              # JavaScript modules
│       └── img/             # Images and assets
├── run.py                   # Application entry point
├── init_db.py               # Database initialization
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md               # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip or conda package manager
- Modern web browser with JavaScript enabled

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd "Fitness Tracker WebApp"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   copy .env.example .env
   # Edit .env and set SECRET_KEY and other variables
   ```

5. **Initialize the database**
   ```bash
   python init_db.py
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

   The app will be available at `http://localhost:5000`

## Usage

### Creating an Account
1. Navigate to the registration page
2. Enter username, email, and password
3. Click "Register"
4. Log in with your credentials

### Logging a Workout
1. Go to **Activity** → **Log New Workout**
2. Select exercise type and activity
3. Enter duration and intensity
4. (Optional) Add heart rate or distance
5. Click "Log Workout"
6. You'll earn XP and update your streak!

### Tracking Nutrition
1. Go to **Nutrition** → **Log Meal**
2. Search for or add a food item
3. Enter quantity in grams
4. Select meal type (breakfast, lunch, dinner, snack)
5. Track your daily totals against your calorie goal

### Setting Goals
1. Go to **Goals** → **Create New Goal**
2. Choose goal type (weight loss, calorie intake, activity minutes, etc.)
3. Set target value and timeframe
4. Track progress from the dashboard

### Viewing Your Progress
- **Dashboard**: See today's summary, recent activity, and goal progress
- **Stats**: View detailed weekly and monthly statistics
- **Badges**: Unlock badges for streaks, XP milestones, and achievements

## Configuration

### Environment Variables
Edit `.env` to configure:
- `FLASK_ENV`: development or production
- `SECRET_KEY`: Random secret key for sessions
- `SQLALCHEMY_DATABASE_URI`: Database connection string

### Database
- **Development**: Uses SQLite (`fitness_tracker.db`)
- **Production**: Uses PostgreSQL (configure via `DATABASE_URL`)

## API Endpoints (Backend)

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout
- `GET/POST /auth/profile` - User profile management

### Activity
- `GET /activity/` - View all workouts
- `GET/POST /activity/log` - Log new workout
- `GET/POST /activity/<id>/edit` - Edit workout
- `POST /activity/<id>/delete` - Delete workout
- `GET /activity/api/mets` - Get MET values for activities

### Nutrition
- `GET /nutrition/` - View daily food log
- `GET/POST /nutrition/log` - Log food
- `GET /nutrition/food/search` - Search foods
- `POST /nutrition/food/add` - Add custom food
- `POST /nutrition/<id>/delete` - Delete food entry

### Goals
- `GET /goals/` - View all goals
- `GET/POST /goals/create` - Create goal
- `GET/POST /goals/<id>/edit` - Edit goal
- `POST /goals/<id>/delete` - Delete goal

### Gamification
- `GET /gamification/dashboard` - View stats and badges
- `GET /gamification/api/status` - Get current gamification state

## Gamification Mechanics

### XP Calculation
- **Activity**: 5 XP per minute of activity
- **Consistency**: Bonus XP for maintaining streaks

### Leveling System
- Level 1 requires 1,000 XP
- Each subsequent level: 1,000 × Level XP

### Streaks
- 1 activity per day maintains streak
- Streak broken if no activity for a day
- Track longest streak for motivation

### Badges
- **7/14/30-Day Streak**: Consecutive activity achievements
- **XP Milestones**: 1,000 / 5,000 / 10,000 XP badges
- **Level Achievements**: Reach level 5, 10, etc.

## Deployment

### Render (Recommended)
1. Push code to GitHub repository
2. Connect repository to Render
3. Set environment variables
4. Deploy!

### Vercel
1. Configure `vercel.json` (serverless functions)
2. Deploy Flask app using serverless adapter
3. Connect PostgreSQL database

## Features Coming Soon

- 🔗 Bluetooth connectivity for smartwatches
- 📱 Progressive Web App (PWA) support
- 📈 Advanced analytics and charts
- 🤝 Social features (friends, challenges)
- 🍽️ Meal planning and recipes
- 📲 Mobile app (React Native)

## Troubleshooting

### "Database locked" error
- Ensure only one instance of the app is running
- Delete `fitness_tracker.db` and reinitialize if corrupted

### Flash messages not showing
- Check Flask session configuration
- Ensure cookies are enabled in browser

### 404 errors on routes
- Verify all routes are registered in `app/__init__.py`
- Check template paths match folder structure

## Contributing

Feel free to fork this project and submit pull requests for improvements!

## License

This project is open source and available under the MIT License.

## Contact & Support

For issues, questions, or suggestions, please create an issue in the repository.

---

**Happy fitness tracking! 💪**
