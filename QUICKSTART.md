# 🚀 Quick Start Guide - CI/CD Project

## Step-by-Step Setup Instructions

### 1️⃣ Verify Project Files

Make sure all these files exist:

```
✓ app.py
✓ requirements.txt
✓ Dockerfile
✓ docker-compose.yml
✓ .github/workflows/ci.yml
✓ .github/workflows/staging.yml
✓ .github/workflows/production.yml
✓ tests/test_app.py
✓ README.md
```

---

### 2️⃣ Test Locally (Without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# In another terminal, test it:
curl http://localhost:5000/
curl http://localhost:5000/health
```

Expected outputs:

- `/`: `Hello from CI/CD Project`
- `/health`: `{"env":"development","status":"healthy"}`

**Stop the app:** Press `Ctrl+C`

---

### 3️⃣ Run Tests

```bash
# Install pytest
pip install pytest requests

# Run tests
pytest tests/ -v
```

You should see all tests pass ✅

---

### 4️⃣ Test with Docker

```bash
# Build image
docker build -t flask-ci-app .

# Run container
docker run -p 5000:5000 -e APP_ENV=development flask-ci-app

# Test in browser or curl:
# http://localhost:5000/
# http://localhost:5000/health
```

**Stop container:** Press `Ctrl+C` then:

```bash
docker ps -a
docker rm <container_id>
```

---

### 5️⃣ Test Multi-Environment with Docker Compose

```bash
# Start staging (port 5000)
docker-compose up staging
# Test: http://localhost:5000/health (should show "env":"staging")

# In new terminal, start production (port 6000)
docker-compose up production
# Test: http://localhost:6000/health (should show "env":"production")

# Or start both at once:
docker-compose up

# Stop all:
docker-compose down
```

---

### 6️⃣ Set Up GitHub Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Flask CI/CD project"

# Create GitHub repo (do this on GitHub website)
# Then link and push:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

---

### 7️⃣ Create Branches for Workflows

```bash
# Create and push staging branch
git checkout -b staging
git push -u origin staging

# Go back to main
git checkout main
```

---

### 8️⃣ Trigger GitHub Actions

**CI Workflow (Automatic):**

- Push any code to `main` branch → CI runs automatically

**Staging Workflow:**

```bash
git checkout staging
# Make a small change to trigger workflow
echo "# Test" >> README.md
git add .
git commit -m "Test staging workflow"
git push
```

Check: GitHub → Actions tab → "Deploy to Staging"

**Production Workflow:**

```bash
git checkout main
git merge staging
git push
```

Check: GitHub → Actions tab → "Deploy to Production"

---

### 9️⃣ Monitor Workflows

1. Go to your GitHub repository
2. Click **Actions** tab
3. You'll see:
   - ✅ CI Pipeline (runs on every push to main)
   - ✅ Deploy to Staging (runs on push to staging)
   - ✅ Deploy to Production (runs on push to main)

---

## 🔍 Testing Checklist

- [ ] Flask app runs locally
- [ ] Home endpoint returns correct message
- [ ] Health endpoint returns JSON with environment
- [ ] All pytest tests pass
- [ ] Docker image builds successfully
- [ ] Docker container runs and responds
- [ ] Staging container runs on port 5000
- [ ] Production container runs on port 6000
- [ ] Docker Compose runs both environments
- [ ] Git repository initialized
- [ ] Code pushed to GitHub
- [ ] CI workflow runs successfully
- [ ] Staging workflow runs successfully
- [ ] Production workflow runs successfully

---

## 🐛 Common Issues & Solutions

### Issue: Port already in use

```bash
# Windows - Find process
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID> /F
```

### Issue: Docker image won't build

```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t flask-ci-app .
```

### Issue: Tests fail with import errors

```bash
# Make sure you're in the project root
cd "c:\Software Final Exam\Final Project Software Process - Group 10"

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: GitHub Actions workflow not triggering

- Make sure branch names match exactly (main, staging)
- Check the Actions tab is enabled in repo settings
- Verify .github/workflows/ directory structure

---

## 📊 Expected Results

### Local Test:

```
$ python app.py
 * Running on http://0.0.0.0:5000
```

### Pytest Output:

```
tests/test_app.py::test_home_endpoint PASSED
tests/test_app.py::test_health_endpoint PASSED
tests/test_app.py::test_health_endpoint_returns_json PASSED
tests/test_app.py::test_invalid_endpoint PASSED
tests/test_app.py::test_home_endpoint_method_not_allowed PASSED
===== 5 passed in 0.12s =====
```

### Docker Compose:

```
staging_1      | * Running on http://0.0.0.0:5000
production_1   | * Running on http://0.0.0.0:5000
```

---

## 🎯 Submission Checklist

For your Software Process Management course:

- [ ] All code files created and working
- [ ] Local testing completed successfully
- [ ] Docker containerization working
- [ ] Docker Compose multi-environment tested
- [ ] GitHub repository created
- [ ] All three workflows (CI, Staging, Production) tested
- [ ] Screenshots of successful workflow runs
- [ ] README.md documentation complete
- [ ] Code follows PEP 8 standards
- [ ] Comments explain key sections

---

## 📸 Screenshots to Include

1. Local app running (terminal + browser)
2. Pytest results (all tests passing)
3. Docker Compose with both environments
4. GitHub Actions - CI workflow success
5. GitHub Actions - Staging workflow success
6. GitHub Actions - Production workflow success
7. Health endpoint responses for both environments

---

## 💡 Pro Tips

1. **Test locally first** before pushing to GitHub
2. **Read error messages carefully** - they usually tell you what's wrong
3. **Use git commit often** with clear messages
4. **Check GitHub Actions logs** if workflows fail
5. **Keep terminal open** to see real-time logs

---

## ✅ You're Done!

Congratulations! You've successfully created a complete CI/CD pipeline with:

- ✅ Flask REST API
- ✅ Docker containerization
- ✅ Multi-environment deployment
- ✅ Automated testing
- ✅ GitHub Actions workflows

**Good luck with your submission! 🎉**

---

**Need Help?**

- Check the main README.md for detailed explanations
- Review error logs carefully
- Test each component individually
- Ask your instructor or TAs if stuck
