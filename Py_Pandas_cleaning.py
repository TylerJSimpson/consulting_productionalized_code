#CLEAN DRAYAGE.COM WEBSCRAPE
#Python3, Pandas, Regular

#import packages
import pandas as pd
import re as re

#show more columns on .head()
pd.set_option('display.max_columns', 10)

#read csv file
data = pd.read_csv(r"C:\Users\simpsont\Downloads\output.csv", names=["Customer"], encoding="unicode_escape")

#drop null value columns to avoid errors
data.dropna(inplace = True)

#define base dataframe
df = pd.DataFrame(data, columns=["Customer"])

#define dataframe1 for email and phone extraction
df1 = pd.DataFrame(data, columns=["Customer"])

def find_email(text):
    #find emails and add to Email column
    email = re.findall(r"[\w\.-]+@[\w\.-]+",str(text))
    return ",".join(email)
df1["Email"]=df["Customer"].apply(lambda x: find_email(x))

def find_phone(text):
    #find phone numbers and add to Phone column
    phone = re.findall(r"[\d]{3}-[\d]{3}-[\d]{4}",str(text))
    return ",".join(phone)
df1["Phone"]=df["Customer"].apply(lambda x: find_phone(x))

def find_hazmat(text):
    #find hazmat status and simplify to yes or no in Hazmat column
    hazmat = re.findall("haz-mat=yes", str(text), re.IGNORECASE)
    return "Yes" if hazmat else "No"
df1["Hazmat"]=df["Customer"].apply(lambda x: find_hazmat(x))

#drop first column leaving only phone and email
df1 = df1.iloc[: ,1:]

#define dataframe 2 out of 2
#first remove unwanted text between new lines
df2 = df["Customer"].str.replace("Company: ", "")

#split based on new lines from extraction
df2 = df2.str.split("\n", n=70, expand=True)

#drop column 1 "COMPANY DETAIL" text
df2 = df2.iloc[: , 1:]

#rename column as "Company"
df2.rename(columns={df2.columns[0]: "Company"}, inplace=True)

#create a "Port Serviced" column -- each extraction will need to be renamed
df2.insert(0, "Port Serviced", "Savannah")

#extract only the needed columns
df2 = df2[["Port Serviced", "Company"]]

#determine frame order and concatenate them
frames = [df2, df1]
df3 = pd.concat(frames, axis=1)

#write to csv
df3.to_csv("sav_port_contacts.csv", index=False, header=True)

