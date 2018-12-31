from bs4 import BeautifulSoup as bs
import urllib.request as uReq
import requests

# Constants
URL = "http://www.utesa.edu/webutesa/recintos/InfGen/Horarios2.asp?FDesde=%s&Fhasta=%s&x=65&y=5&SelCiclo=12019"
URL_COOKIES = 'http://www.utesa.edu/webutesa/recintos/Santiago/HomeSG.asp?reci=UTSAN'


class Subject:
    def __init__(self, name, groups):
        self.name = name
        self.groups = groups


class Group:
    def __init__(self, id_group='', time='', classroom='', is_virtual=False):
        self.id = id_group
        self.time = time
        self.classroom = classroom
        self.is_virtual = is_virtual


def get_cookies(url):
    r = requests.get(url, timeout=5)
    for cookie in r.cookies:
        return str(cookie)[8:-20]


def get_html(url, cookies):
    opener = uReq.build_opener()
    opener.addheaders.append(('Cookie', cookies))
    page = opener.open(url)
    page_html = page.read()
    page.close()
    return page_html


def get_data(subject_id):
    cookies = get_cookies(URL_COOKIES)
    url_e = (URL % (subject_id, subject_id + "999"))
    page_html = get_html(url_e, cookies)

    page_soup = bs(page_html, "html.parser")
    table = page_soup.find("td", {"height": "238"})
    rows = table.findAll("tr")
    subject_data = Subject('', [])

    for row in rows:
        data = row.findAll("td", {"valign": "middle"})
        count = 0
        group_data = Group()
        print(data)
        for info in data:
            if count == 3:
                subject_data.name = info.text.strip()
            if count == 1:
                group_data.id = info.text.strip()
            if count == 5:
                group_data.time = info.text.strip()
            if count == 6:
                group_data.classroom = info.text.strip()
            count += 1
        if group_data.id != '':
            if group_data.classroom == 'VIRTU-':
                group_data.is_virtual = True
            subject_data.groups.append(group_data)

    return subject_data


if __name__ == "__main__":
    # example to print data of ADM900
    data = get_data('ADM900')
    # print('Subject name: %s' % data.name)
    # print("=============================")
    # for group in data.groups:
    #     print(
    #         'Group id: %s | Group Date: %s | Group Classroom: %s | VIRTUAL: %s' %
    #         (group.id, group.time, group.classroom, group.is_virtual))
    #     print("====================================================================")
    print("FINISH")