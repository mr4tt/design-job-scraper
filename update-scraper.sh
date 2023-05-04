git pull --no-edit

now=$(TZ=America/Los_Angeles date +'%m/%d/%Y %H:%M %Z')

python3 scrape-esdj.py

git push 