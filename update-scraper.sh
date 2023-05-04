git pull --no-edit

now=$(TZ=America/Los_Angeles date +'%m/%d/%Y %H:%M %Z')

python3 scrape-esdj.py

git config --local user.email ${{ secrets.EMAIL }}
git config --local user.name ${{ secrets.NAME }}

git commit -m "adding new jobs on $now"