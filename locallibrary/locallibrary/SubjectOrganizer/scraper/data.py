from bs4 import BeautifulSoup as bs
import urllib.request as uReq
import requests
import objects

# Constants
URL = "http://www.utesa.edu/webutesa/recintos/InfGen/Horarios2.asp?FDesde=%s&Fhasta=%s&x=65&y=5&SelCiclo=12019"
URL_COOKIES = 'http://www.utesa.edu/webutesa/recintos/Santiago/HomeSG.asp?reci=UTSAN'

# class Subject:
#     def __init__(self, name, groups):
#         self.name = name
#         self.groups = groups


# class Group:
#     def __init__(self, id_group='', time='', classroom='', is_virtual=False):
#         self.id = id_group
#         self.time = time
#         self.classroom = classroom
#         self.is_virtual = is_virtual

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


def get_data(subject_id, url, subject_data = None):
    cookies = get_cookies(URL_COOKIES)

    if subject_data == None:
        url = (url % (subject_id, subject_id + "999"))
        subject_data = objects.Subject('', [])

    page_html = get_html(url, cookies)

    page_soup = bs(page_html, "html.parser")
    table = page_soup.find("td", {"height": "238"})
    rows = table.findAll("tr")

    for row in rows:
        data = row.findAll("td", {"valign": "middle"})
        group_data = objects.Group()
        
        if data:
            print('ID: %s and Status: %s' % (data[1].text.strip(), data[0].text.strip()))
            status = data[0].text.strip()
            subject_data.name = data[3].text.strip()
            group_data.id = data[1].text.strip()
            group_data.time = data[5].text.strip()
            group_data.classroom = data[6].text.strip()
            if 'Asig. Virtual' in group_data.time:
                group_data.is_virtual = True
            
            subject_data.groups.append(group_data)
    
    next_page = table.select_one('img[src*="../../images/PagSig.gif"]')
    if next_page:
        new_url = 'http://www.utesa.edu' + next_page.parent.get('href')
        return get_data(subject_id, new_url, subject_data)
    else:
        return subject_data


if __name__ == "__main__":
    # example to print data of ESP301  
    data = get_data('ESP301', URL)
    print('Subject name: %s' % data.name)
    print("=============================")
    for group in data.groups:
        print(
            'Group id: %s | Group Date: %s | Group Classroom: %s | VIRTUAL: %s' %
            (group.id, group.time, group.classroom, group.is_virtual))
        print("====================================================================")
    print("FINISH")