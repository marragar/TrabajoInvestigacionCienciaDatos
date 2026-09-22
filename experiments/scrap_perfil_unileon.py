import requests
from bs4 import BeautifulSoup

url = "https://portalcientifico.unileon.es/investigadores/97244/detalle"
r = requests.get(url, timeout=10)
soup = BeautifulSoup(r.text, "html.parser")
print(soup.get_text(separator=" ", strip=True)[:2000])