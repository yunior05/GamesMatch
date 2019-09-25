from bs4 import BeautifulSoup as bs
import urllib.request as uReq
import requests


def get_data(subject_id):
    url_cookies = 'http://www.utesa.edu/webutesa/recintos/Santiago/HomeSG.asp?reci=UTSAN'
    r = requests.get(url_cookies,timeout=5)
    for cookie in r.cookies:
        cook = str(cookie)[8:-20]

    url = "http://www.utesa.edu/webutesa/recintos/InfGen/Horarios2.asp?FDesde=%s&Fhasta=%s&x=65&y=5&SelCiclo=32019"
    opener = uReq.build_opener()  
    opener.addheaders.append(('Cookie', cook))
    url_e = (url % (subject_id, subject_id + "999"))
    page = opener.open(url_e)
    page_html = page.read()
    page.close()

    page_soup = bs(page_html, "html.parser")
    table = page_soup.find("td", {"height": "238"})
    rows = table.findAll("tr")
    subject = {'groups': []}

    for row in rows:
        data = row.findAll("td", {"valign": "middle"})
        count = 0
        group = {}
        for info in data:
            if count == 3:
                subject['name'] = info.text.strip()
            if count == 1:
                group['id'] = info.text.strip()
            if count == 5:
                group['time'] = info.text.strip()
            if count == 6:
                group['classroom'] = info.text.strip()
            count +=1
        if group:
            subject['groups'].append(group)

    class materia:
        def __init__(self, name, groups):
            self.name = name
            self.groups = groups

    class grupo:
        def __init__(self, id_g, time, classroom):
            self.id = id_g
            self.time = time
            self.classroom = classroom

    subject_ob = materia(subject['name'], [])

    for g in subject['groups']:
        gup = grupo(g['id'], g['time'], g['classroom'])
        subject_ob.groups.append(gup)
    return subject_ob


def printData(value):
    data = get_data(value);
    print(data.name)
    for group in data.groups:
        print(group.id)
        print(group.time)
        print(group.classroom)
if __name__ == "__main__":
    ##example with id of ALGORITMOS COMPUTACIONALES INF117
    print(printData('INF117'))