import requests
from bs4 import BeautifulSoup
from app import db, TreasuryYieldTable
import datetime

def scrape():
    url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield'
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    table = soup.find("table", attrs={"class": "t-chart"})

    #printing the entire table
    #print(table.prettify())
    
    #getting every row of table
    trs = table.findAll("tr")
    
    #getting the column names
    col_names = table.findAll("th")
    column_name = [names.text for names in col_names]
    
    #getting the data on the table, excluding column names
    data = []
    for item in trs:
        td_tag = item.findAll('td')
        for tag in td_tag:
            data.append(tag.text)
    
    #converting data to list of lists and saving final list as data_lst
    length = len(column_name)
    dates = len(data) //length
    data_lst = []
    j = 0
    for i in range(dates):
        row = data[j: j+ length]
        data_lst.append(row)
        j +=13
    return data_lst

def setup_db():
    data = scrape()

    for lst in data:
        row = TreasuryYieldTable(date = lst[0], one_mo = lst[1], two_mo = lst[2], three_mo = lst[3], six_month = lst[4], 
                        one_year = lst[5], two_year = lst[6], three_year = lst[7], five_year = lst[8], seven_year =lst[9], ten_year = lst[10],
                        twenty_year = lst[11], thirty_year = lst[12], data_fetched = datetime.now)
        db.session.add(row)
        db.session.commit()
        
if __name__ == '__main__':
    scrape()
    setup_db()