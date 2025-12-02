from selenium import webdriver
import bs4
import csv

driver = webdriver.Firefox()

curr_log = "https://www.fflogs.com/reports/kNn2rcQKLZCTgHdh?fight=46&type=damage-done&source=708"
driver.get(curr_log)
print(driver.title)

def get_soup(url):
    driver.get(url)
    html_content = driver.page_source
    page = bs4.BeautifulSoup(html_content, "lxml")
    return page


log_html = get_soup(curr_log)

for row in log_html.find_all('tr'):
    for cell in row.find_all('td'):
        print(cell)


driver.quit()
