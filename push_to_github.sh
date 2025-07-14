#!/bin/bash

# 🔧 Set these before running
GITHUB_USERNAME="AtomaHuro"
REPO_NAME="chatbrain-vtuber"

# 🗂️ Initialize repo
git init
git add .
git commit -m "Initial commit: AI VTuber brain core setup"

# 🌐 Create remote and push
git remote add origin https://github.com/AtomaHuro/AiVtuberProject.git
git branch -M main
git push -u origin main

echo "✅ Project pushed to https://github.com/AtomaHuro/AiVtuberProject.git"
