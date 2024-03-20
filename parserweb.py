from bs4 import BeautifulSoup
import requests
import dearpygui.dearpygui as dpg
from openpyxl import Workbook

webprefix = "https://checko.ru"
regions = ("RU", "BY")
region_links = ("https://checko.ru/company/select?code=all", "https://checko.ru/by/company/select?code=all")
target_file = "data.xlsx"
selected_region = 0
selected_activity = -1
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
        "special_tax_mode": "-",
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

def save_ru_data(filename, companies):
    wb = Workbook()
    ws = wb.active
    ws["A1"] = "Ссылка"
    ws["B1"] = "Название"
    ws["C1"] = "ОГРН"
    ws["D1"] = "ИНН"
    ws["E1"] = "Дата регистрации"
    ws["F1"] = "Вид деятельности"
    ws["G1"] = "Юридический адрес"
    ws["H1"] = "Организационно-правовая форма"
    ws["I1"] = "Уставный капитал"
    ws["J1"] = "Специальный налоговый режим"
    ws["K1"] = "Держатель реестра акционеров"
    ws["L1"] = "Среднесписочная численность работников"
    ws["M1"] = "Почта"
    ws["N1"] = "Телефон"

    i = 2
    for comp in companies:
        itxt = str(i)
        ws["A"+itxt] = comp["link"]
        ws["B"+itxt] = comp["name"]
        ws["C"+itxt] = comp["ogrn"]
        ws["D"+itxt] = comp["inn"]
        ws["E"+itxt] = comp["register_date"]
        ws["F"+itxt] = comp["activity_type"]
        ws["G"+itxt] = comp["address"]
        ws["H"+itxt] = comp["org_type"]
        ws["I"+itxt] = comp["capital"]
        ws["J"+itxt] = comp["special_tax_mode"]
        ws["K"+itxt] = comp["holder"]
        ws["L"+itxt] = comp["avg_worker_count"]
        ws["M"+itxt] = comp["emails"]
        ws["N"+itxt] = comp["phones"]

        i += 1

    wb.save(target_file)

def save_by_data(filename, companies):
    wb = Workbook()
    ws = wb.active
    ws["A1"] = "Ссылка"
    ws["B1"] = "Название"
    ws["C1"] = "УНП"
    ws["D1"] = "Дата регистрации"
    ws["E1"] = "Основной вид деятельности"
    ws["F1"] = "Юридический адрес"
    ws["G1"] = "Текущий орган учета"
    ws["H1"] = "Орган, принявший решение о регистрации"
    ws["I1"] = "Почта"
    ws["J1"] = "Телефон"

    i = 2
    for comp in companies:
        itxt = str(i)
        ws["A"+itxt] = comp["link"]
        ws["B"+itxt] = comp["name"]
        ws["C"+itxt] = comp["UNP"]
        ws["D"+itxt] = comp["register_date"]
        ws["E"+itxt] = comp["activity_type"]
        ws["F"+itxt] = comp["address"]
        ws["G"+itxt] = comp["current_gov"]
        ws["H"+itxt] = comp["registrator"]
        ws["I"+itxt] = comp["emails"]
        ws["J"+itxt] = comp["phones"]

        i += 1

    wb.save(target_file)


def add_output_message(str):
    dpg.set_value("outputMessage", dpg.get_value("outputMessage") + "\n" + str)

# parsing ru company page
def get_ru_company_data(url):
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
def get_by_company_data(url):
    print("Called BY")
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
        if (len(innerdivs) >= 1):
            ttl = innerdivs[0].get_text()
            print(ttl)
            if (ttl == "Дата регистрации"):
                holder["register_date"] = innerdivs[1].get_text()
            if (ttl == "Основной вид деятельности"):
                holder["activity_type"] = innerdivs[1].get_text()
            if (ttl == "Юридический адрес"):
                holder["address"] = data.find_all("strong")[0].get_text()
                print("Found address: " + holder["address"])
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
def parse_single_companies_page(url, isRu):
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "lxml")
    atags = bs.find_all("td", {"class": ""})
    lst = []
    for i in atags:
        company = i.find("a", {"class": "link"})
        if (company != None):
            add_output_message("Обработка компании " + company.get_text())
            cmpurl = webprefix + company["href"]
            lst.append(get_ru_company_data(cmpurl) if isRu else get_by_company_data(cmpurl))
    
    return lst

# parsing all pages from baseurl
def parse_companies_pages(baseurl, isRu):
    lst = []
    res = parse_single_companies_page(baseurl, isRu)
    lst = lst + res
    i = 1
    while (len(res) > 0):
        i += 1
        add_output_message("Обработка страницы " + str(i))
        url = baseurl + "&page=" + str(i)
        res = parse_single_companies_page(url, isRu)
        lst = lst + res
    return lst

def select_region(regname):
    global selected_region, list_categories, list_categories_links
    selected_region = regions.index(regname)
    list_categories, list_categories_links = get_activity_categories(region_links[selected_region])

def select_category(catname):
    global selected_region, list_categories, list_categories_links, selected_activity
    idx = list_categories.index(catname)
    url = list_categories_links[idx][1]
    selected_activity = idx
    print(url)

def callback_select_country(sender, app_data):
    global list_categories_links, list_categories, selected_region
    select_region(app_data)
    #dpg.add_combo(items = ("test1", "test2"), label="Категории")
    dpg.configure_item("categoriescombo", items=list_categories, default_value=list_categories[0])
    select_category(list_categories[0])

def callback_select_activity(sender, app_data):
    global selected_activity
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    select_category(app_data)

def callback_select_file(sender, app_data):
    global target_file
    target_file = app_data["file_path_name"]
    dpg.set_value("selectedFile", "Текущий файл: " + target_file)

def callback_parse(sender, app_data):
    if (len(list_categories) == 0 or len(list_categories_links) == 0):
        return
    
    try:
        add_output_message("Начат парсинг со следующими настройками:")
        add_output_message("Регион: " + regions[selected_region])
        add_output_message("Вид деятельности: " + list_categories[selected_activity])
        lst = parse_companies_pages(webprefix + list_categories_links[selected_activity][1], selected_region == 0)
        print(lst)
        add_output_message("Парсинг окончен, сохраняем в файл")
        if (selected_region == 0):
            save_ru_data(target_file, lst)
        else:
            save_by_data(target_file, lst)
    except Exception:
        add_output_message("Возникла неопознанная ошибка")


dpg.create_context()

# Font from https://fonts-online.ru/fonts/noto-mono
with dpg.font_registry():
    with dpg.font("notomono-regular.ttf", 13, default_font=True, tag="Default font") as f:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font("Default font")

dpg.create_viewport(title='Custom Title', width=600, height=600)

with dpg.file_dialog(directory_selector=False, show=False, callback=callback_select_file, id="file_dialog_id", width=500 ,height=400,):
        dpg.add_file_extension("Source files (*.xlsx *.xls){.xlsx,.xls}", color=(0, 255, 255, 255))

with dpg.window(label="Checko parser", width=580, height=200, pos=(2, 2)):
    dpg.add_text("Выберите страну и вид деятельности")
    dpg.add_combo(("RU", "BY"), label="Страна", callback=callback_select_country)
    dpg.add_combo((), label="Категории", tag="categoriescombo", callback=callback_select_activity)
    dpg.add_button(label="Выберите файл", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_text(default_value="Текущий файл: " + target_file, tag="selectedFile")
    dpg.add_button(label="СТАРТ", callback=callback_parse)

with dpg.window(label="Log", width=580, height=355, pos=(2, 205)):
    dpg.add_text(default_value="",tag="outputMessage")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()