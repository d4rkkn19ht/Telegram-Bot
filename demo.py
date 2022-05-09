import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime

page_url = "https://sjc.com.vn/giavang/textContent.php"
page = requests.get(page_url,verify=False)
soup = BeautifulSoup(page.content, 'html.parser')

# Lấy giá bán
raw_ask_price = soup.table.find_all("tr", limit = 2)[1].find_all("td")[2].text
ask_price = raw_ask_price.replace(',', '.') + ' VND'

# Lấy ngày giờ cập nhật
raw_date = soup.find_all(class_ = "w350 m5l float_left red_text bg_white")[0].text
date = datetime.strptime(raw_date, '%I:%M:%S %p %d/%m/%Y')
print_date = date.strftime('%d/%m/%Y %H:%M:%S')

print('%s %s %s' % (print_date, sys.argv[1], ask_price))