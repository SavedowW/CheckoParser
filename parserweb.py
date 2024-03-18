from bs4 import BeautifulSoup
import requests

# parsing main page
'''url = "https://checko.ru/company/select?code=all"
response = requests.get(url)
bs = BeautifulSoup(response.text, "lxml")
atags = bs.find_all("a", {"class": "link"})
res = []
k = 0
for i in atags:
    res.append((i.get_text(), i.get('href')))

for i in res:
    print(i)'''

# parsing companies page
url = "https://checko.ru/company/select?code=469000"
response = requests.get(url)
bs = BeautifulSoup(response.text, "lxml")
atags = bs.find_all("td", {"class": ""})
lst = []
for i in atags:
    company = i.find("a", {"class": "link"})
    if (company != None):
        lst.append(company.get_text())
        
for i in lst:
    print(i)