from bs4 import BeautifulSoup
from page import html_page
from string import digits
from replit import db

soup = BeautifulSoup(html_page, 'html.parser', multi_valued_attributes=None)

key = 0
for name in soup.find_all('p'):

  text = name.get_text()
  
  clean = text.translate({ord(k): None for k in digits})
  db[key] = clean
  key = key + 1
  print(clean)




