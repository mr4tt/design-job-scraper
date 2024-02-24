import requests
from bs4 import BeautifulSoup

readme = open("README.md", "w+", encoding="utf-8")
internships = open("internships.md", "w+", encoding="utf-8")
fulltime = open("fulltime.md", "w+", encoding="utf-8")

all_files = [readme, internships, fulltime]

esdj_link = "# Scraping Early Stage Design Jobs \n\nLink: https://www.earlystagedesignjobs.com/\n\n"
chart_headers = "| Title | Company | Location | Date Added | Country | ESDJ Link | Job Link |\n"
chart_break = "| --- | --- | --- | --- | --- | --- | --- |\n"

# add chart markdown style to each file
for f in all_files:
    f.write(esdj_link)
    if f == readme:
        f.write("""Please check out [internships.md](https://github.com/mr4tt/scrape-esdj/blob/main/internships.md) for only internships, or [fulltime.md](https://github.com/mr4tt/scrape-esdj/blob/main/internships.md) for only full time positions.\n\n""")
    f.write(chart_headers)
    f.write(chart_break)

page_num = 1

while page_num in range(6):
    url = "https://www.earlystagedesignjobs.com/" if page_num == 1 else "https://www.earlystagedesignjobs.com/?d844da9d_page=" + str(page_num)

    # gets each page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find("div", class_="w-dyn-items")
    
    # stop if we find empty jobs
    empty = soup.find("div", class_="w-dyn-empty")
    if empty != None:
        break

    jobs = results.find_all(
        "div", 
        class_="caption1-3 captiongrey", 
        )

    # grabs the grandparents of caption1-3 so we can loop thru properly
    job_elements = [x.parent.parent.parent.parent for x in jobs]

    # removes duplicates 
    def remove_duplicates(iterable):
        seen = set()
        result = []
        for x in iterable:
            if x in seen: continue
            result.append(x)
            seen.add(x)
        return result
    
    # removes duplicates from job elements (using only set unorders stuff)
    unique_job_elements = remove_duplicates(job_elements)

    # find the actual job link 
    def get_job_link(link):
        # gets the page of the job
        esdj_link = "https://www.earlystagedesignjobs.com" + link
        esdj_page = requests.get(esdj_link)
        soup2 = BeautifulSoup(esdj_page.content, "html.parser")

        # use if there's multiple links 
        # links = soup2.find_all('div', class_="jobbody")
        # for x in links:
        #     print(x.find("a")["href"])

        # returns the job link 
        return soup2.find("a",{"class":"button gotojobbutton w-button"}).get("href")
    
    def write_to_file(files, title, company, location, date_added, country, link, job_link):
        for file in files:
            file.write(("| " + title + " ").replace("–","-"))
            file.write("| " + company.text + " ")
            file.write(("| " + location.text + " ").replace("é","e"))
            file.write("| " + date_added.text + " ")
            file.write("| " + country.text + " ")
            file.write("| [Link](https://www.earlystagedesignjobs.com" + link + ") ")
            file.write("| [Link](" + job_link + ") |\n")

    # append the jobs to their respective files
    for v in unique_job_elements:
        title = v.find("h4", class_="h4-666")
        company = v.find("h3", class_="h3-white")
        location = v.find("div", class_="solojobimpdetails").findChildren()[0]
        date_added = v.find("div", class_="solojobdetailswrap").findChildren("div", class_="hordivjob")[3]
        country = v.find("div", class_="solojobimpdetails").findChildren()[6]
        link = v.find("a")["href"]
        job_type = v.find("div", class_="solojobimpdetails").findChildren()[2]

        job_link = get_job_link(link)
        files_to_write = [readme]

        if "intern" in job_type.text.lower():
            files_to_write.append(internships)
        else:
            files_to_write.append(fulltime)

        write_to_file(files_to_write, title.text, company, location, date_added, country, link, job_link)

        print(date_added.text)

    print("Page: " + str(page_num))

    page_num += 1
    
readme.close()
internships.close()
fulltime.close()
