@echo off
cd C:\Projects\dailylunch\app\site
python scrape.py

git add .
git commit -m "Automated commit message"
git push origin main