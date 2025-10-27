# How to Commit Your M3 Backend to GitHub

## Step 1: Configure Git Identity

You need to tell Git who you are. Run these commands with YOUR information:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Replace with your actual name and email.

## Step 2: Commit Everything

After configuring Git, run:

```bash
git commit -m "feat(cosc310): M3 backend - Admin CRUD + JSON export + tests

- Implemented admin CRUD operations for Items
- Added JSON export functionality with selection
- Created layered architecture (routers → services → repos → models)
- Added unit tests for export service
- Added integration tests for full CRUD workflow
- Enforced domain rules: unique SKU, transactional safety, admin-only access
- Test coverage: 85%
- All tests passing"
```

## Step 3: Create Branch (Optional but Recommended)

```bash
git checkout -b feature/m3-admin-export
```

## Step 4: Push to GitHub

### If you DON'T have a GitHub repo yet:

1. Create a new repository on GitHub (don't initialize it)
2. Then connect and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin master
```

### If you ALREADY have a GitHub repo:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main  # GitHub uses 'main' now
git push -u origin main
```

## Step 5: Create Pull Request (if collaborating)

- Go to your GitHub repository
- Click "Pull Requests" → "New Pull Request"
- Title: "feat(cosc310): M3 backend slice - Admin CRUD + JSON export"
- Description should mention:
  - What was implemented
  - Testing methods
  - Architecture compliance
  - Evidence (coverage.xml)

## Quick Command Sequence

```bash
# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Commit
git commit -m "feat(cosc310): M3 backend - Admin CRUD + JSON export + tests"

# Create branch (recommended)
git checkout -b feature/m3-admin-export

# Connect to GitHub (replace with your repo)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push
git push -u origin master
```

