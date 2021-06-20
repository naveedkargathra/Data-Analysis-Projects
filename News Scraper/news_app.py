import sys,time
from bs4 import BeautifulSoup 
import requests 
import pandas as pd
from pymongo import MongoClient


url = 'https://www.scoopwhoop.com/category/news/'                                #URL of Scoopwhoop.com's Latest Headlines

try:
    page=requests.get(url)                                                       # Get HTML content from URL
    print(page.status_code)                                                      # HTTP Status Response
    
except Exception as e:    
    
    error_type, error_obj, error_info = sys.exc_info()      
    
    print ('ERROR FOR LINK:',url)
    
    print (error_type, 'Line:', error_info.tb_lineno)

frame =[]                                                                         #Initializing empty frame for dataframe
soup = BeautifulSoup(page.text, "html.parser")                                    #Using Beautifulsoup to parse HTML code
links=soup.find_all('div',attrs={'class':'article-list'})                         #Looks for tags <div> containing article-list
print(len(links))                                                                 # Number of news articles on a given page


for j in links:
    Statement = j.find("a",attrs={'class':'article-title'}).find('h4').text.strip()                    # Statment of News article
    Link="www.scoopwhoop.com" + j.find("div",attrs={'class':'article-body'}).find('a')['href'].strip() # Web Link for the news article      
    Author= j.find("a", attrs={'class':'article-author'}).text.strip()                                 # Name of the Author
    Date = j.find("span",attrs={'class':'timeago'}).get('data-date').strip()                           # Date and Time of Publication

    frame.append([Statement,Link,Author,Date])                                                         # Populating array over each iteration of loop


data=pd.DataFrame(frame, columns=['Statement','Link','Author','Date and Time'])    # Converting array into pandas dataframe

filename="NEWS.csv"
path = 'C:\\Users\\navee\\Downloads\\Python\\Dev\\'
data.to_csv(path+'NEWS.csv', sep=',')                                              # Dataframe to CSV

data_csv = pd.read_csv("NEWS.csv") 

# Connect to MongoDB Database
client = MongoClient("mongodb+srv://naveed_kargathra:ali2042015@cluster0.5mxjp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority") 

db = client['Naveed_Python']                                                       # Link to a pre-existing Database on MongoDB Cluster

collection = db['Web_Scraping']

data_csv.reset_index(inplace=True)

data_dict = data_csv.to_dict("records")                                            #CSV to JSON Dictionary


collection.insert_many(data_dict)                                                  #Upload JSON Dict to MongoDB

