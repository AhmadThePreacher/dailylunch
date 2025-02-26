@echo
echo Starting Task >> C:\Projects\dailylunch\app\site\log.txt
cd C:\Projects\dailylunch\app\site
python scrape.py

git add .
git commit -m "Automated commit message"
git push origin main

echo Task Completed >> C:\Projects\dailylunch\app\site\log.txt
