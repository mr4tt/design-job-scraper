import requests
from bs4 import BeautifulSoup

page_num = 1

while page_num in range(10):
    url = "https://www.earlystagedesignjobs.com/" if page_num == 1 else "https://www.earlystagedesignjobs.com/?d844da9d_page=" + str(page_num)
    
    # gets each page
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("div", class_="w-dyn-items")

    # gets each job
    jobs = results.find_all("div", role="listitem")

    # filters for intern positions only 
    intern_jobs = results.find_all(
        "div", 
        class_="caption1-3 captiongrey", 
        string=lambda text: "intern" in text.lower()
        )

    # grabs the grandparents of caption1-3 so we can loop thru properly
    intern_job_elements = set(
        x.parent.parent.parent.parent for x in intern_jobs
    )

    for c, v in enumerate(intern_job_elements):
        title = v.find("h4", class_="h4-666")
        company = v.find("h3", class_="h3-white")
        location = v.find("div", class_="solojobimpdetails").findChildren()[0]
        role = v.find("div", class_="solojobimpdetails").findChildren()[4]
        country = v.find("div", class_="solojobimpdetails").findChildren()[6]
        link = v.find("a")["href"]

        print(title.text, end="\n")
        print(company.text, end="\n")
        print(location.text, end="\n")
        print(role.text, end="\n")
        print(country.text, end="\n")
        print("https://www.earlystagedesignjobs.com" + link)
        print()

    print("Page: ", str(page_num))
    page_num+=1
    