# Deployment Guide

## Cloud Deployment Options

### Option 1: Render (Recommended)

Render is ideal for this Flask application with free tier availability and PostgreSQL support.

#### Step 1: Prepare Repository
```bash
# Initialize git repository if not already done
git init
git add .
git commit -m "Initial commit: Fitness Tracker WebApp"
```

#### Step 2: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub or Google
3. Connect your GitHub repository

#### Step 3: Create Web Service
1. Click "Create +" → "Web Service"
2. Select your Fitness Tracker repository
3. Configure:
   - **Name**: fitness-tracker
   - **Environment**: Docker
   - **Region**: Choose nearest to your location
   - **Plan**: Free tier (sufficient for development)

#### Step 4: Environment Variables
Set in Render Dashboard → Environment:
```
FLASK_ENV=production
SECRET_KEY=your-random-secret-key-here
SQLALCHEMY_DATABASE_URI=postgresql://user:password@host/fitness_tracker
```

#### Step 5: Database Setup
1. In Render Dashboard, create PostgreSQL database
2. Copy connection string to `SQLALCHEMY_DATABASE_URI`
3. Run migrations after deployment

#### Step 6: Deploy
```bash
git push origin main
# Render auto-deploys on push
```

---

### Option 2: Vercel (Serverless)

For serverless deployment using Vercel's Python runtime.

#### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

#### Step 2: Configure Application
Update `run.py` for serverless:
```python
# Export app for serverless
from backend.app import create_app
app = create_app('production')

if __name__ == '__main__':
    app.run()
```

#### Step 3: Create Vercel Project
```bash
vercel --prod
```

#### Step 4: Set Environment Variables
```bash
vercel env add FLASK_ENV production
vercel env add SECRET_KEY your-secret-key
vercel env add SQLALCHEMY_DATABASE_URI postgresql://...
```

#### Step 5: Deploy
```bash
vercel --prod
```

---

### Option 3: AWS (Elastic Beanstalk)

For more control and scaling capabilities.

#### Prerequisites
- AWS Account
- AWS CLI installed and configured

#### Step 1: Install EB CLI
```bash
pip install awsebcli
```

#### Step 2: Initialize Elastic Beanstalk
```bash
eb init -p python-3.11 fitness-tracker --region us-east-1
```

#### Step 3: Create Environment
```bash
eb create fitness-tracker-env
```

#### Step 4: Set Environment Variables
```bash
eb setenv FLASK_ENV=production SECRET_KEY=your-key SQLALCHEMY_DATABASE_URI=postgresql://...
```

#### Step 5: Deploy
```bash
eb deploy
```

---

### Option 4: Heroku (Legacy - Free Tier Discontinued)

If using paid Heroku tier:

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create fitness-tracker-app

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment
heroku config:set FLASK_ENV=production SECRET_KEY=your-key

# Deploy
git push heroku main

# Run migrations
heroku run python init_db.py
```

---

## Production Setup Checklist

### Before Deployment

- [ ] Update `SECRET_KEY` to a random, secure value (use `secrets` module)
- [ ] Set `FLASK_ENV=production`
- [ ] Configure PostgreSQL database URL
- [ ] Set `SESSION_COOKIE_SECURE=True` for HTTPS
- [ ] Enable CSRF protection in Flask-WTF
- [ ] Review and update `.env` variables
- [ ] Test locally with `FLASK_ENV=production`

### Database Migrations

```bash
# Run initialization script
python init_db.py

# This creates tables and seeds badge/food data
```

### SSL/HTTPS Certificate

Most cloud providers (Render, Vercel, AWS) provide free SSL certificates automatically.

### Domain Configuration

1. Get custom domain from registrar (Namecheap, GoDaddy, etc.)
2. Update DNS records to point to your cloud provider
3. Enable SSL certificate

### Monitoring

Set up monitoring for:
- Application health (uptime checks)
- Error logs (Sentry integration)
- Performance metrics (APM)
- Database performance

---

## Post-Deployment

### 1. Create Initial Admin/Test User
```bash
# SSH into server or use web terminal
python -c "
from backend.app import create_app, db
from backend.app.models.user import User
from backend.app.models.gamification import GamificationState

app = create_app('production')
with app.app_context():
    user = User(username='testuser', email='test@example.com')
    user.set_password('securepassword')
    db.session.add(user)
    db.session.commit()
    
    gamification = GamificationState(user_id=user.id)
    db.session.add(gamification)
    db.session.commit()
    print('Test user created!')
"
```

### 2. Set Up Backup

```bash
# Render PostgreSQL auto-backs up
# For AWS RDS, enable automated backups in console

# Schedule database dumps (weekly)
pg_dump DATABASE_URL > backups/fitness_db_$(date +%Y%m%d).sql
```

### 3. Enable Logging

Add to `run.py`:
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    handler = RotatingFileHandler('fitness_tracker.log', maxBytes=10240, backupCount=10)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
```

---

## Troubleshooting Deployment

### Application Won't Start
- Check logs: `render logs` or cloud provider console
- Verify `SQLALCHEMY_DATABASE_URI` is correct
- Ensure `SECRET_KEY` is set

### Database Connection Error
```
psycopg2.OperationalError: could not connect to server
```
- Verify database URL format: `postgresql://user:pass@host:5432/dbname`
- Check database is running and accessible
- Verify firewall/security group allows connection

### Static Files Not Loading
- Ensure `frontend/static/` directory exists
- Configure Flask to serve static files correctly
- Consider using CDN for production (CloudFlare, AWS CloudFront)

### High Memory Usage
- Reduce worker processes in Gunicorn
- Enable connection pooling for database
- Review slow queries in logs

---

## Performance Optimization

### 1. Database Indexing
```python
# Already included in models, but ensure indexing:
user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
```

### 2. Caching
Add Redis caching (optional):
```bash
pip install redis
```

### 3. CDN Configuration
Upload static assets to CloudFlare or AWS CloudFront for faster delivery.

### 4. Database Connection Pooling
Already configured via SQLAlchemy. Tune if needed:
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 3600,
}
```

---

## Rollback Procedure

### Render
```bash
# View deployment history in dashboard
# Click on previous version and "Redeploy"
```

### AWS Elastic Beanstalk
```bash
eb abort  # Cancel current deployment
eb swap --destination-name production-env  # Swap to previous version
```

---

## Security Considerations

- [ ] Use HTTPS only
- [ ] Set secure session cookies
- [ ] Enable CSRF protection
- [ ] Validate all user inputs
- [ ] Sanitize database queries (SQLAlchemy ORM handles this)
- [ ] Keep dependencies updated: `pip list --outdated`
- [ ] Implement rate limiting for login attempts
- [ ] Use environment variables for secrets
- [ ] Regular security audits: `pip install safety && safety check`

---

## Support & Resources

- Render Docs: https://render.com/docs
- Flask Deployment: https://flask.palletsprojects.com/deployment/
- PostgreSQL: https://www.postgresql.org/docs/
- Gunicorn: https://gunicorn.org/

For issues or questions, refer to the main README.md or create an issue in the repository.
