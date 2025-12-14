# Flask CI/CD Project

## Software Process Management Course - Part A (DevOps & Infrastructure)

A simple Flask API demonstrating CI/CD pipeline practices with Docker containerization and GitHub Actions workflows.

---

## 📋 Project Overview

This project demonstrates:

- Flask REST API with health checks
- Docker containerization
- Multi-environment deployment (Staging & Production)
- GitHub Actions CI/CD pipelines
- Automated testing with pytest

---

## 🏗️ Project Structure

```
Final Project Software Process - Group 10/
├── .github/
│   └── workflows/
│       ├── ci.yml              # CI pipeline (build & test)
│       ├── staging.yml         # Staging deployment
│       └── production.yml      # Production deployment
├── tests/
│   └── test_app.py            # Pytest unit tests
├── app.py                      # Flask application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Multi-environment orchestration
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Docker & Docker Compose
- Git

### Local Development

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**

   ```bash
   python app.py
   ```

3. **Test endpoints:**
   - Home: http://localhost:5000/
   - Health: http://localhost:5000/health

### Run Tests

```bash
pytest tests/ -v
```

---

## 🐳 Docker Usage

### Build and Run Single Container

```bash
# Build image
docker build -t flask-ci-app .

# Run container
docker run -p 5000:5000 -e APP_ENV=development flask-ci-app
```

### Using Docker Compose (Multi-Environment)

```bash
# Start staging environment (port 5000)
docker-compose up staging

# Start production environment (port 6000)
docker-compose up production

# Start both environments
docker-compose up

# Stop all containers
docker-compose down
```

**Access:**

- Staging: http://localhost:5000/health
- Production: http://localhost:6000/health

---

## 🔄 CI/CD Workflows

### 1. CI Pipeline (`ci.yml`)

**Triggers:** Push or PR to `main` branch

**Steps:**

- ✅ Checkout code
- ✅ Setup Python 3.8
- ✅ Install dependencies
- ✅ Run pytest tests
- ✅ Build Docker image
- ✅ Verify Docker build
- ✅ Test container runs

### 2. Staging Deployment (`staging.yml`)

**Triggers:** Push to `staging` branch

**Steps:**

- ✅ Build Docker image with staging tag
- ✅ Run staging container
- ✅ Execute smoke tests
- ✅ Verify environment configuration
- ✅ Cleanup

### 3. Production Deployment (`production.yml`)

**Triggers:** Push to `main` branch OR manual trigger

**Steps:**

- ✅ Build Docker image with production tag
- ✅ Tag with commit SHA for versioning
- ✅ Run production smoke tests
- ✅ Security checks
- ✅ Deployment summary

---

## 🌿 Branching Strategy

```
main            → Production deployments
  ↑
staging         → Staging environment testing
  ↑
feature/*       → Feature development branches
```

### Workflow:

1. Create feature branch: `git checkout -b feature/my-feature`
2. Develop and test locally
3. Push to staging: `git checkout staging && git merge feature/my-feature`
4. Test in staging environment
5. Merge to main: `git checkout main && git merge staging`
6. Production deployment triggered automatically

---

## 📡 API Endpoints

### `GET /`

Returns welcome message.

**Response:**

```
Hello from CI/CD Project
```

### `GET /health`

Health check endpoint with environment info.

**Response:**

```json
{
  "status": "healthy",
  "env": "development|staging|production"
}
```

---

## 🧪 Testing

### Local Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Test Coverage

- Home endpoint (`/`)
- Health endpoint (`/health`)
- JSON response validation
- Invalid routes (404)
- Method validation (405)

---

## 🔧 Environment Variables

| Variable  | Description             | Values                                 |
| --------- | ----------------------- | -------------------------------------- |
| `APP_ENV` | Application environment | `development`, `staging`, `production` |

---

## 📊 Port Configuration

| Environment | Host Port | Container Port |
| ----------- | --------- | -------------- |
| Staging     | 5000      | 5000           |
| Production  | 6000      | 5000           |

---

## 🛠️ Troubleshooting

### Docker Issues

**Port already in use:**

```bash
# Find and kill process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Stop all containers
docker-compose down
```

**Image build fails:**

```bash
# Clean Docker cache
docker system prune -a
docker-compose build --no-cache
```

### Test Failures

**Import errors:**

```bash
# Ensure you're in project root
cd "Final Project Software Process - Group 10"

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📚 Best Practices Demonstrated

✅ **Separation of Environments:** Staging and production isolated  
✅ **Health Checks:** Docker healthcheck + /health endpoint  
✅ **Automated Testing:** Pytest integration in CI pipeline  
✅ **Version Control:** Git-based workflow with proper branching  
✅ **Container Optimization:** Layer caching, slim base image  
✅ **Documentation:** Comprehensive README with examples  
✅ **Security:** No hardcoded secrets, environment variables

---

## 🎓 Learning Outcomes

This project demonstrates understanding of:

1. **Continuous Integration:** Automated build and test
2. **Continuous Deployment:** Automated staging and production pipelines
3. **Containerization:** Docker and Docker Compose
4. **Testing:** Unit tests with pytest
5. **Infrastructure as Code:** Declarative configuration
6. **DevOps Practices:** Multi-environment strategy

---

## 📝 Course Requirements Checklist

- [x] Flask API with multiple endpoints
- [x] Docker containerization
- [x] Docker Compose for multi-environment
- [x] GitHub Actions CI workflow
- [x] GitHub Actions staging workflow
- [x] GitHub Actions production workflow
- [x] Automated testing with pytest
- [x] Health check endpoint
- [x] Environment variable configuration
- [x] Proper port mapping (5000 staging, 6000 production)
- [x] Documentation (README)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📄 License

This project is created for educational purposes as part of the Software Process Management course.

---

## 👤 Author

**Group 10** - Software Process Management Course

---

## 🙏 Acknowledgments

- Course: Software Process Management
- Assignment: Part A - DevOps & Infrastructure
- Framework: Flask
- CI/CD: GitHub Actions
- Containerization: Docker

---

**⭐ Star this repo if you found it helpful!**
