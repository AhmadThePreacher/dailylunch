@echo off
cd C:\Users\ahmkad\Repo\dailylunch\app\site
git fetch --all --prune
git pull

python scrape.py

git add .
git commit -m "Automated commit message"
git push origin main
