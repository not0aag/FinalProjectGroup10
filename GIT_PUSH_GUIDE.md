# Git Push Setup Guide - Person A

## 🎯 Your GitHub Repository
**URL:** https://github.com/not0aag/FinalProjectGroup10

---

## 📋 Step-by-Step Git Commands

### **Step 1: Initialize Git Repository**

```bash
cd "c:\Software Final Exam\Final Project Software Process - Group 10"
git init
```

**Expected Output:**
```
Initialized empty Git repository in c:/Software Final Exam/Final Project Software Process - Group 10/.git/
```

---

### **Step 2: Add All Files**

```bash
git add .
```

**This adds:**
- app.py
- requirements.txt
- Dockerfile
- docker-compose.yml
- .github/workflows/ (all 3 workflows)
- tests/
- All other files

---

### **Step 3: Create Initial Commit**

```bash
git commit -m "Initial commit: Flask app, Docker config, and CI/CD workflows"
```

**Expected Output:**
```
[main (root-commit) abc1234] Initial commit: Flask app, Docker config, and CI/CD workflows
 13 files changed, 700+ insertions(+)
 create mode 100644 app.py
 create mode 100644 Dockerfile
 ...
```

---

### **Step 4: Link to Your GitHub Repository**

```bash
git remote add origin https://github.com/not0aag/FinalProjectGroup10.git
```

**Verify it worked:**
```bash
git remote -v
```

**Expected Output:**
```
origin  https://github.com/not0aag/FinalProjectGroup10.git (fetch)
origin  https://github.com/not0aag/FinalProjectGroup10.git (push)
```

---

### **Step 5: Rename Branch to 'main'**

```bash
git branch -M main
```

---

### **Step 6: Push to GitHub**

```bash
git push -u origin main
```

**You may be prompted to authenticate:**
- Use GitHub Personal Access Token (PAT) if required
- Or GitHub CLI authentication

**Expected Output:**
```
Enumerating objects: 20, done.
Counting objects: 100% (20/20), done.
Delta compression using up to 8 threads
Compressing objects: 100% (18/18), done.
Writing objects: 100% (20/20), 15.50 KiB | 2.21 MiB/s, done.
Total 20 (delta 2), reused 0 (delta 0)
To https://github.com/not0aag/FinalProjectGroup10.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

### **Step 7: Create Staging Branch**

```bash
git checkout -b staging
```

**Expected Output:**
```
Switched to a new branch 'staging'
```

---

### **Step 8: Push Staging Branch**

```bash
git push -u origin staging
```

**Expected Output:**
```
Total 0 (delta 0), reused 0 (delta 0)
To https://github.com/not0aag/FinalProjectGroup10.git
 * [new branch]      staging -> staging
Branch 'staging' set up to track remote branch 'staging' from 'origin'.
```

---

### **Step 9: Return to Main Branch**

```bash
git checkout main
```

---

### **Step 10: Verify Branch Setup**

```bash
git branch -a
```

**Expected Output:**
```
* main
  staging
  remotes/origin/main
  remotes/origin/staging
```

📸 **TAKE SCREENSHOT OF THIS OUTPUT** (Required for A5)

---

## ✅ Verification Checklist

After completing the above steps:

### **Check GitHub Repository:**
1. Go to: https://github.com/not0aag/FinalProjectGroup10
2. Verify you see all files in the main branch
3. Click "Actions" tab - you should see workflows running

### **Check Branches:**
1. Click on branch dropdown (shows "main")
2. You should see both "main" and "staging" branches

### **Check GitHub Actions:**
1. Go to: https://github.com/not0aag/FinalProjectGroup10/actions
2. You should see "CI Pipeline" workflow running or completed
3. 📸 **TAKE SCREENSHOT when it shows green checkmark** (Required for A6)

---

## 🔐 GitHub Authentication

If you need to authenticate, you have two options:

### **Option 1: Personal Access Token (Recommended)**

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: "FinalProject"
4. Expiration: 30 days
5. Select scopes:
   - ✅ `repo` (all)
   - ✅ `workflow`
6. Click "Generate token"
7. **Copy the token** (you won't see it again!)
8. Use this token as password when git asks

### **Option 2: GitHub CLI**

```bash
# Install GitHub CLI first
# Then authenticate:
gh auth login
```

---

## 📸 Required Screenshots for A5 & A6

### **Screenshot 1: Branch List**
```bash
git branch -a
```
📸 Capture the terminal output showing main and staging branches

### **Screenshot 2: GitHub Actions - CI Pipeline**
Go to: https://github.com/not0aag/FinalProjectGroup10/actions
📸 Capture the Actions tab showing CI workflow with green ✓

### **Screenshot 3: GitHub Actions - Staging Workflow**
Push to staging branch first:
```bash
git checkout staging
echo "# Test staging" >> README.md
git add .
git commit -m "Test staging workflow"
git push
```
📸 Capture staging workflow with green ✓

### **Screenshot 4: GitHub Actions - Production Workflow**
```bash
git checkout main
git merge staging --no-ff -m "Merge staging to main"
git push
```
📸 Capture production workflow with green ✓

---

## 🚀 Complete Git Command Sequence

**Copy-paste this entire block** (after editing your name/email):

```bash
# Navigate to project
cd "c:\Software Final Exam\Final Project Software Process - Group 10"

# Configure Git (replace with your info)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Initialize and commit
git init
git add .
git commit -m "Initial commit: Flask app, Docker config, and CI/CD workflows"

# Link to GitHub
git remote add origin https://github.com/not0aag/FinalProjectGroup10.git
git branch -M main
git push -u origin main

# Create and push staging branch
git checkout -b staging
git push -u origin staging

# Return to main
git checkout main

# Verify branches
git branch -a
```

---

## ⚠️ Troubleshooting

### **Problem: Authentication Failed**
**Solution:** Use Personal Access Token as password, not your GitHub password

### **Problem: Remote Already Exists**
```bash
git remote remove origin
git remote add origin https://github.com/not0aag/FinalProjectGroup10.git
```

### **Problem: Branch Already Exists**
```bash
git branch -D staging
git checkout -b staging
```

### **Problem: Permission Denied**
**Solution:** Make sure you're logged into the correct GitHub account (not0aag)

---

## 🎯 Next Steps After Push

1. **Verify on GitHub** - Check all files are visible
2. **Check Actions Tab** - Wait for workflows to complete
3. **Take Screenshots** - Capture successful workflow runs
4. **Add Person B as Collaborator**:
   - Go to: https://github.com/not0aag/FinalProjectGroup10/settings/access
   - Click "Add people"
   - Enter Person B's GitHub username
   - Select "Write" or "Admin" permission

---

## ✅ Success Criteria

You're done when:
- ✅ All files visible on GitHub
- ✅ Both branches (main & staging) exist
- ✅ CI workflow runs and passes (green ✓)
- ✅ Screenshots captured
- ✅ Person B added as collaborator

---

**Ready to push? Run the commands above!** 🚀

**Repository:** https://github.com/not0aag/FinalProjectGroup10
