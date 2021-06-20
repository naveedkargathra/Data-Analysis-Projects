import pandas as pd
import numpy as np
import datetime as dt
import smtplib
import openpyxl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# Reading RAW Data Set using Pandas and Extracting Month from 'created_on' Column.
data = pd.read_csv('C:\\Users\\navee\\Desktop\\Xeno\\Xeno_Assignment\\Raw Data\\Data_Set_2.csv')
data['created_on'] = pd.to_datetime(data['created_on'], format= "%d-%m-%Y %H:%M").dt.strftime('%y-%m')


## Overall MIS Report

# Generating Empty Dataframe as per required Report Sample for Overall Sheet.
df = pd.DataFrame(columns = ["Revenue", "Orders", "Customers", "New Customers", "Repeated Customers", "Frequency(Orders/Customers)"])

df["Revenue"]= data.groupby("created_on").sum()["amount"].astype(int) #Calculating Revenue by Month

df["Orders"] = data.groupby("created_on").size() #Total Orders per Month

df["Customers"] = data.groupby("created_on").agg(n_customers = ("customer_id", "nunique")) #Total Unique customers each Month

# Total New Customers each Month
df['New Customers'].iloc[0] = df['Customers'].iloc[0] 
for i in range(1,len(df)): 
    new_customers = df['Customers'].iloc[i] - df['Customers'].iloc[i-1]
    if new_customers >0:
        df['New Customers'].iloc[i] = new_customers
    else:
        df['New Customers'].iloc[i] = 0

# Total customers repeating orders in subsequent month
df['Repeated Customers'].iloc[0] = 0
df['Repeated Customers'] = df['Customers'] - df['New Customers']

# Frequency of Orders each Month
df['Frequency(Orders/Customers)'] = round(df['Orders'] / df['Customers'], 2)
print(df.head())
# Renaming column names as per Report Sample
index = { "18-01":"Month1","18-02":"Month2","18-03":"Month3","18-04":"Month4","18-05":"Month5","18-06":"Month6","18-07":"Month7","18-08":"Month8","18-09":"Month9","18-10":"Month10","18-11":"Month11","18-12":"Month12","19-01":"Month13","19-02":"Month14","19-03":"Month15", "19-04":"Month16", "19-05":"Month17", "19-06":"Month18", "19-07":"Month19", "19-08":"Month20", "19-09":"Month21", "19-10":"Month22", "19-11":"Month23", "19-12":"Month24" }
df= df.rename(index = index)
df_Transposed = df.T
print(df_Transposed.head())


# Appending 'Overall' Sheet to Final MIS Report
df_Transposed.to_excel("C:\\Users\\navee\\Desktop\\Xeno\\Xeno_Assignment\\Result\\MIS_Report.xlsx",sheet_name='Overall')


## LOCATION WISE MIS Report##

#Generating empty Dataframe for location wise data
df1 = pd.DataFrame(columns = ["Revenue", "Orders", "Customers", "New Customers", "Repeated Customers", "Frequency(Orders/Customers)"])

df1["Revenue"]= data.groupby(["location_id", "created_on"]).sum()["amount"].astype(int)  # Total Revenue each Month each Location

df1["Orders"] = data.groupby(["location_id", "created_on"]).size() # Total Orders each Month each Location
df1["Customers"] = data.groupby(["location_id", "created_on"]).agg(n_customers = ("customer_id", "nunique")) # Total Unique Customers for each month and each location


# Total New Customers each month each location
df1['New Customers'].iloc[0] = df1['Customers'].iloc[0]
for i in range(1,len(df1)): 
    new_customers = df1['Customers'].iloc[i] - df1['Customers'].iloc[i-1]
    if new_customers >0:
        df1['New Customers'].iloc[i] = new_customers
    else:
        df1['New Customers'].iloc[i] = 0

# Total Customers repeating orders in subsequent months for each location
df1['Repeated Customers'].iloc[0] = 0
df1['Repeated Customers'] = df1['Customers'] - df1['New Customers']

df1['Frequency(Orders/Customers)'] = round(df1['Orders'] / df1['Customers'], 2) # Frequency of Orders each Month for each Location

# Populating MIS Report for each location and appending sheets location wise
i = 1
for location_id, loc in df1.groupby(level=0):
    loc = loc.reset_index(level=0, drop = True)
    print(loc.head())
    index = { "18-01":"Month1","18-02":"Month2","18-03":"Month3","18-04":"Month4","18-05":"Month5","18-06":"Month6","18-07":"Month7","18-08":"Month8","18-09":"Month9","18-10":"Month10","18-11":"Month11","18-12":"Month12","19-01":"Month13","19-02":"Month14","19-03":"Month15", "19-04":"Month16", "19-05":"Month17", "19-06":"Month18", "19-07":"Month19", "19-08":"Month20", "19-09":"Month21", "19-10":"Month22", "19-11":"Month23", "19-12":"Month24" }
    loc= loc.rename(columns ={'created_on': ''},index = index)
    loc_Transposed = loc.T
    print(loc_Transposed.head())
    with pd.ExcelWriter('C:\\Users\\navee\\Desktop\\Xeno\\Xeno_Assignment\\Result\\MIS_Report.xlsx', mode='a') as writer:   # pylint: disable=abstract-class-instantiated
        loc_Transposed.to_excel(writer, sheet_name='Location ' + str(i))
    i +=1

#Script to send MIS report as an Email Attachmment

# Sender and Recipent Email Address
fromaddr = "Enter Your Own Email ID"
toaddr = "Enter the Recipent EMail ID"

# instance of MIMEMultipart
msg = MIMEMultipart()

# storing the senders email address
msg['From'] = fromaddr

# storing the receivers email address
msg['To'] = toaddr

# storing the subject
msg['Subject'] = "MIS Report of the Test for Data Analytics Postion"

# string to store the body of the mail
body = "I have attached the MIS Report as required by you for the second task in the Test For Data Analytics Position"

# attach the body with the msg instance
msg.attach(MIMEText(body, 'plain'))

# open the file to be sent
filename = "MIS_Report.xlsx"
attachment = open("C:\\Users\\navee\\Desktop\\Xeno\\Xeno_Assignment\\Result\\MIS_Report.xlsx", "rb")

# instance of MIMEBase and named as p
p = MIMEBase('application', 'octet-stream')

# To change the payload into encoded form
p.set_payload((attachment).read())

# encode into base64
encoders.encode_base64(p)

p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# attach the instance 'p' to instance 'msg'
msg.attach(p)

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login(fromaddr, "Enter your password for authentication")

# Converts the Multipart msg into a string
text = msg.as_string()

# sending the mails
s.sendmail(fromaddr, toaddr, text)

# terminating the session
s.quit()
