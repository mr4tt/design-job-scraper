git pull --no-edit

now=$(TZ=America/Los_Angeles date +'%m/%d/%Y %H:%M %Z')

cd /root/scrape-esdj

python3 scrape-esdj.py

git c "adding new jobs on $now"

git push
