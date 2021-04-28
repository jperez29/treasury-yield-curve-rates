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
    db.drop_all()
    db.create_all()

    #adding data to database
    for lst in data:
        row = TreasuryYieldTable(date = lst[0], one_mo = lst[1], two_mo = lst[2], three_mo = lst[3], six_month = lst[4], 
                    one_year = lst[5], two_year = lst[6], three_year = lst[7], five_year = lst[8], seven_year =lst[9], ten_year = lst[10],
                    twenty_year = lst[11], thirty_year = lst[12])
        db.session.add(row)
        db.session.commit()

def make_chart(data, filename):
    #I am doing this work in make_chart notebook for now
    #this code will be to create the chart
    print("generating matplotlib chart")
    plt.plot(data)

    #code to save chart in a file with the date when it was created
#     plt.savefig(f'charts/{filename}.png')
    print("completed")
    
def main():
    setup_db()
    #to get today's date
    dt_now = dt.datetime.now()
    dt_fmt = dt_now.strftime("%m-%d-%y-%H%M%S")
    #this is where I'll read the data in the sqlite3 as a df
    #will pass this data as the first argument in make_chart function  
    make_chart(np.arange(10), f'test-{dt_fmt}')
            
if __name__ == '__main__':
    # scrape()
    # setup_db()
    main()