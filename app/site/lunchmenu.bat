@echo off
cd c:\dailylunch\app\site
python scrape.py

git add .
git commit -m "Automated commit message"
git push origin main

