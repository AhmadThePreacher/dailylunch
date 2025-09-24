@echo off
cd C:\Users\ahmkad\Projects\dailylunch\app\site
python scrape.py

git add .
git commit -m "Automated commit message"
git push origin main