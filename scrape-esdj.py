import requests
from bs4 import BeautifulSoup

readme = open("README.md", "w+")

readme.write("# Scraping Early Stage Design Jobs for internships\n\n")

readme.write("Link: https://www.earlystagedesignjobs.com/\n\n")

readme.write("| Title | Company | Location | Date Added | Country | Link |\n")
readme.write("| --- | --- | --- | --- | --- | --- |\n")

page_num = 1

while page_num in range(10):
    url = "https://www.earlystagedesignjobs.com/" if page_num == 1 else "https://www.earlystagedesignjobs.com/?d844da9d_page=" + str(page_num)

    # gets each page
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("div", class_="w-dyn-items")
    
    # if page_num > 1:
    #     empty = soup.find("div", class_="w-dyn-empty")
    #     print(empty.getText())
    #     if empty.getText() == "No items found.":
    #         break
    
    empty = soup.find("div", class_="w-dyn-empty")
    if empty != None:
        break

    # gets each job
    jobs = results.find_all("div", role="listitem")

    # filters for intern positions only 
    intern_jobs = results.find_all(
        "div", 
        class_="caption1-3 captiongrey", 
        string=lambda text: "intern" in text.lower()
        )

    # grabs the grandparents of caption1-3 so we can loop thru properly
    intern_job_elements = [x.parent.parent.parent.parent for x in intern_jobs]

    # removes duplicates 
    def remove_duplicates(iterable):
        seen = set()
        result = []
        for x in iterable:
            if x in seen: continue
            result.append(x)
            seen.add(x)
        return result
    
    # removes duplicates from intern job elements (using set unorders stuff)
    unique_intern_job_elements = remove_duplicates(intern_job_elements)

    for v in unique_intern_job_elements:
        title = v.find("h4", class_="h4-666")
        company = v.find("h3", class_="h3-white")
        location = v.find("div", class_="solojobimpdetails").findChildren()[0]
        date_added = v.find("div", class_="solojobdetailswrap").findChildren("div", class_="hordivjob")[3]
        country = v.find("div", class_="solojobimpdetails").findChildren()[6]
        link = v.find("a")["href"]

        print(date_added.text)


        readme.write(("| " + title.text + " ").replace("–","-"))

        readme.write("| " + company.text + " ")

        readme.write(("| " + location.text + " ").replace("é","e"))

        readme.write("| " + date_added.text + " ")

        readme.write("| " + country.text + " ")
        readme.write("| [Link](https://www.earlystagedesignjobs.com" + link + ") |\n")
        #readme.write("\n")

    print("Page: " + str(page_num))

    page_num+=1
    
readme.close()