import requests
from bs4 import BeautifulSoup


urls = ["https://www.earlystagedesignjobs.com/", 
        "https://www.earlystagedesignjobs.com/?d844da9d_page=2",
        "https://www.earlystagedesignjobs.com/?d844da9d_page=3"]

page_num = 1

for url in urls:

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("div", class_="w-dyn-items")
    jobs = results.find_all("div", role="listitem")

    intern_jobs = results.find_all(
        "div", 
        class_="caption1-3 captiongrey", 
        string=lambda text: "intern" in text.lower()
        )

    intern_job_elements = set(
        x.parent.parent.parent.parent for x in intern_jobs
    )

    #soup.select('div:has(> p.example:contains(TRUE))')
    #inner_jobs = results.find_all("div", class_="solojobimpdetails")
    #print(results.prettify())

    #for x in inner_jobs:
    #    print(x, end="\n")

    for c, v in enumerate(intern_job_elements):
        title = v.find("h4", class_="h4-666")
        company = v.find("h3", class_="h3-white")
        location = v.find("div", class_="solojobimpdetails").findChildren()[0]
        role = v.find("div", class_="solojobimpdetails").findChildren()[4]
        country = v.find("div", class_="solojobimpdetails").findChildren()[6]
        link = v.find("a")["href"]
        #location = v.select("div", class_="caption1-3 captiongrey:nth-child(1)")
        #test = v.select("div", class_="caption1-3 captiongrey:nth-child(2)")
        print(title.text, end="\n")
        print(company.text, end="\n")
        print(location.text, end="\n")
        print(role.text, end="\n")
        print(country.text, end="\n")
        print("https://www.earlystagedesignjobs.com" + link)
        print()
    print("Page: ", str(page_num))
    page_num+=1
    