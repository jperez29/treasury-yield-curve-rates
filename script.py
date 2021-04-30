import requests
from bs4 import BeautifulSoup
from app import db, TreasuryYieldTable
import datetime as dt
import pandas as pd
import sqlite3 as sql
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

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
    #this code creates the chart
    df = data
    print("generating matplotlib chart")
    plt.style.use('bmh')
    plt.figure(figsize=(15,7))
    x = ['1 month', '2 month', '3 month', '6 month', '1 year', '2 year', '3 year', '5 year', '7 year', '10 year', '20 year', '30 year']
    y1 = list(df.iloc[-1][2:])
    y2 = list(df.iloc[-2][2:])
    y3 = list(df.iloc[-3][2:])
    plt.plot(x, y1, 'gs-', label = df.iloc[-1][1],markersize=8, linewidth=3.0, path_effects=[path_effects.SimpleLineShadow(shadow_color="green", linewidth=5),path_effects.Normal()])
    plt.plot(x, y2, '^-' ,color='magenta', label = df.iloc[-2][1], markersize=6, path_effects=[path_effects.SimpleLineShadow(shadow_color="red", linewidth=5),path_effects.Normal()])
    plt.plot(x, y3, 'bo-' , label = df.iloc[-3][1], markersize=4, path_effects=[path_effects.SimpleLineShadow(shadow_color="blue", linewidth=5),path_effects.Normal()])
    plt.title('Treasury Yield Curve')
    plt.xlabel('Maturity')
    plt.ylabel('Interest Rates')
    plt.title('Daily US Treasury Yield Curve')
    plt.legend(loc='upper left')
    plt.grid(False)

    #code to save chart in a file with the date when it was created
    plt.savefig(f'charts/{filename}.png')
    print("completed")
    plt.show()
    
def main():
    setup_db()
    #to get today's date
    dt_now = dt.datetime.now()
    dt_fmt = dt_now.strftime("%m-%d-%y-%H%M%S")
    #this is where I'll read the data in the sqlite3 as a df
    #will pass this data as the first argument in make_chart function
    db = 'treasury_yield_curve_rates.db'
    conn = sql.connect(db) 
    df = pd.read_sql("SELECT * FROM treasury_yield_table;", conn) 
    make_chart(df, f'test-{dt_fmt}')

if __name__ == '__main__':
    main()