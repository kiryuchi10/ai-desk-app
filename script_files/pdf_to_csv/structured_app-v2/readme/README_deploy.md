# Deployment Instructions

## Frontend (Netlify)
```bash
# Build React app
npm run build

# Deploy folder on Netlify
# Connect repo or drag `build/` folder into Netlify site dashboard
```

## Backend (GitHub + CI/CD with Render/Heroku)
```bash
# Create requirements.txt
pip freeze > requirements.txt

# Create Procfile for deployment
echo "web: python app.py" > Procfile

# Push to GitHub and connect to Render
```

## CI/CD Example (GitHub Actions)
```yaml
# .github/workflows/deploy.yml
name: Deploy App

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Deploy to Heroku or Render
      run: echo "Deploy step..."
```