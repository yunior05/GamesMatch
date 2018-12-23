from bs4 import BeautifulSoup as bs
import urllib.request as uReq
import requests

url_c = 'http://www.utesa.edu/webutesa/recintos/Santiago/HomeSG.asp?reci=UTSAN'
r = requests.get(url_c,timeout=5)
for cookie in r.cookies:
    cook = str(cookie)[8:-20]

url = "http://www.utesa.edu/webutesa/recintos/InfGen/Horarios2.asp?FDesde=CON115&Fhasta=CON115999&x=65&y=5&SelCiclo=12019"
opener = uReq.build_opener()  
opener.addheaders.append(('Cookie', cook))
f = opener.open(url)
page_html = f.read()
f.close()


page_soup = bs(page_html, "html.parser")
finish_data = []
table = page_soup.find("td", {"height": "238"})
rows = table.findAll("tr")
estructur = {'name': 'Algoritmo',
    'group': [
        {
        'clave': '123',
        'curso': 'b3',
        'horario': '56',
        },  {
        'clave': '321',
        'curso': 'b3',
        'horario': '56',
        }
    ]
}
for row in rows:
    data = row.findAll("td", {"valign": "middle"})
    count = 0
    gr = []
    for info in data:
        if count == 1:
            gr.append("Clave : %s" % info.text.strip())
        if count == 5:
            gr.append("Horario: %s " % info.text.strip())
        if count == 6:
            gr.append("Curso: %s" % info.text.strip())
        count +=1
    if gr:
        finish_data.append(gr)
        gr = []
print(finish_data)
print(estructur)
