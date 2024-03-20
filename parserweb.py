from bs4 import BeautifulSoup
import requests
import dearpygui.dearpygui as dpg

webprefix = "https://checko.ru"
regions = ("RU", "BY")
region_links = ("https://checko.ru/company/select?code=all", "https://checko.ru/by/company/select?code=all")
selected_region = 0
list_categories = []
list_categories_links = []

def getHolderPlaceholder(link):
    return {
        "link": link,
        "name": "-",
        "ogrn": "-",
        "inn": "-",
        "UNP": "-",
        "register_date": "-",
        "activity_type": "-",
        "address": "-",
        "org_type": "-",
        "capital": "-",
        "holder": "-",
        "avg_worker_count": "-",
        "phones": "-",
        "emails": "-",
        "current_gov": "-",
        "registrator": "-"
    }

def get_activity_categories(url):
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "lxml")
    atags = bs.find_all("a", {"class": "link"})
    list = []
    links = []
    for i in atags:
        if (i.get_text() == "каталогом"):
            continue
        links.append((i.get_text(), i.get('href')))
        list.append(i.get_text())

    return list, links


# parsing companies page
'''url = "https://checko.ru/company/select?code=469000"
response = requests.get(url)
bs = BeautifulSoup(response.text, "lxml")
atags = bs.find_all("td", {"class": ""})
lst = []
for i in atags:
    company = i.find("a", {"class": "link"})
    if (company != None):
        lst.append(company.get_text())
        
for i in lst:
    print(i)'''

# parsing ru company page
def getRuCompanyData(url):
    response = requests.get(url)
    holder = getHolderPlaceholder(url)
    bs = BeautifulSoup(response.text, "lxml")
    basicsec = bs.find_all("section", {"id": "basic"})
    name = basicsec[0].find("p", {"class": "mb-4"})
    holder["name"] = name.get_text()
    divs = basicsec[0].find_all("div", {"class": "uk-width-1-2@m"})
    lcol = divs[0]
    rcol = divs[1]

    lcol_datas = lcol.find_all("div", {"class": "basic-data"})
    holder["ogrn"] = lcol_datas[1].find("strong", {"id": "copy-ogrn"}).get_text()
    holder["inn"] = lcol_datas[1].find("strong", {"id": "copy-inn"}).get_text()
    for data in lcol_datas:
        innerdivs = data.find_all("div")
        if (len(innerdivs) >= 2):
            ttl = innerdivs[0].get_text()
            if (ttl == "Дата регистрации"):
                holder["register_date"] = innerdivs[1].get_text()
            elif (ttl == "Вид деятельности"):
                holder["activity_type"] = innerdivs[1].get_text()
            elif (ttl == "Юридический адрес"):
                holder["address"] = innerdivs[1].get_text()
            elif (ttl == "Организационно-правовая форма"):
                holder["org_type"] = innerdivs[1].get_text()
            elif (ttl == "Уставный капитал"):
                holder["capital"] = innerdivs[1].get_text()
            elif (ttl == "Специальный налоговый режим"):
                spntodelete = innerdivs[1].find_all("span")
                for i in spntodelete:
                    i.decompose()
                holder["special_tax_mode"] = innerdivs[1].get_text()


    rcol_datas = rcol.find_all("div", {"class": "basic-data"})
    for data in rcol_datas:
        innerdivs = data.find_all("div")
        if (len(innerdivs) >= 2):
            ttl = innerdivs[0].get_text()
            if (ttl == "Держатель реестра акционеров"):
                holder["holder"] = innerdivs[1].get_text()
            if (ttl == "Среднесписочная численность работников"):
                spntodelete = innerdivs[1].find_all("span")
                for i in spntodelete:
                    i.decompose()
                holder["avg_worker_count"] = innerdivs[1].get_text()

    contactssec = bs.find_all("section", {"id": "contacts"})
    if (len(contactssec) > 0):
        contactsdivs = contactssec[0].find_all("div", {"class": "uk-grid-divider"})[0].find_all("div", {"class": "uk-width-1"})
        phones = contactsdivs[0].find_all("a", {"class": "black-link"})
        phones_str = ""
        for i in phones:
            if (len(phones_str) > 0):
                phones_str += ", "
            phones_str += i.get_text()
        if (len(phones_str) > 0):
            holder["phones"] = phones_str
        else:
            holder["phones"] = "-"
        emails = contactsdivs[1].find_all("a", {"class": "link"})
        emails_str = ""
        for i in emails:
            email_s = i.get_text()
            if email_s.__contains__("@"):
                if (len(emails_str) > 0):
                    emails_str += ", "
                emails_str += email_s
        if (len(emails_str) > 0):
            holder["emails"] = emails_str
        else:
            holder["emails"] = "-"
    return holder

# parsing by company page
def getByCompanyData(url):
    response = requests.get(url)
    holder = getHolderPlaceholder(url)
    bs = BeautifulSoup(response.text, "lxml")
    basicsec = bs.find_all("section", {"id": "basic"})
    name = basicsec[0].find("p", {"class": "mb-4"})
    holder["name"] = name.get_text()

    col_datas = basicsec[0].find_all("div", {"class": "basic-data"})
    holder["UNP"] = col_datas[1].find("strong", {"id": "copy-id"}).get_text()
    for data in col_datas:
        innerdivs = data.find_all("div")
        if (len(innerdivs) >= 2):
            ttl = innerdivs[0].get_text()
            if (ttl == "Дата регистрации"):
                holder["register_date"] = innerdivs[1].get_text()
            if (ttl == "Основной вид деятельности"):
                holder["activity_type"] = innerdivs[1].get_text()
            if (ttl == "Юридический адрес"):
                holder["address"] = innerdivs[1].get_text()
            if (ttl == "Текущий орган учёта"):
                holder["current_gov"] = innerdivs[1].get_text()

    regsec = bs.find_all("section", {"id": "registration"})
    col1_content = regsec[0].find_all("div", {"class": "uk-width-1"})[0]
    col1_divs = col1_content.find_all("div")
    holder["registrator"] = col1_divs[3].get_text()

    consec = bs.find_all("section", {"id": "contacts"})
    if (len(consec) > 0):
        grid = consec[0].find_all("div", {"class": "uk-grid-divider"})[0].find_all("div", {"class": "uk-width-1"})
        emails = grid[1].find_all("a", {"class": "link"})
        emails_str = ""
        for i in emails:
            email_s = i.get_text()
            print(email_s)
            if email_s.__contains__("@"):
                if (len(emails_str) > 0):
                    emails_str += ", "
                emails_str += email_s
        if (len(emails_str) > 0):
            holder["emails"] = emails_str
        else:
            holder["emails"] = "-"

        phones = grid[0].find_all("a", {"class": "black-link"})
        phones_str = ""
        for i in phones:
            phone_s = i.get_text()
            if (len(phones_str) > 0):
                phones_str += ", "
            phones_str += phone_s
        if (len(phones_str) > 0):
            holder["phones"] = phones_str
        else:
            holder["phones"] = "-"

    return holder

# parsing single page
def parseSingleCompaniesPage(url, isRu):
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "lxml")
    atags = bs.find_all("td", {"class": ""})
    lst = []
    for i in atags:
        company = i.find("a", {"class": "link"})
        if (company != None):
            cmpurl = webprefix + company["href"]
            lst.append(getRuCompanyData(cmpurl) if isRu else getByCompanyData(cmpurl))
    
    return lst

# parsing all pages from baseurl
def parseCompaniesPages(baseurl, isRu):
    lst = []
    res = parseSingleCompaniesPage(baseurl, isRu)
    lst = lst + res
    i = 1
    while (len(res) > 0):
        i += 1
        print("Page " + str(i))
        url = baseurl + "&page=" + str(i)
        res = parseSingleCompaniesPage(url, isRu)
        lst = lst + res
    return lst

def select_region(regname):
    global selected_region, list_categories, list_categories_links
    selected_region = regions.index(regname)
    list_categories, list_categories_links = get_activity_categories(region_links[selected_region])
    print(list_categories)

def callback_select_country(sender, app_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    select_region(app_data)
    print(selected_region)

#lst = parseCompaniesPages("https://checko.ru/company/select?code=841000", True)
#print(lst)

dpg.create_context()

# Font from https://fonts-online.ru/fonts/noto-mono
with dpg.font_registry():
    with dpg.font("notomono-regular.ttf", 13, default_font=True, tag="Default font") as f:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font("Default font")

dpg.create_viewport(title='Custom Title', width=600, height=300)

with dpg.window(label="Checko parser", width=550, height=250):
    dpg.add_text("Hello, world")
    dpg.add_combo(("RU", "BY"), label="Страна", callback=callback_select_country)
    dpg.add_combo((), label="Категории", id=999)
    dpg.add_button(label="Save")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()