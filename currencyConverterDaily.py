"""
	This script is used to store the currency change rates into text and csv files on daily basis.
	This script should be executed once on each day and it used INR(indian rupees) as the base currency for BlueOptima.
	In this script a list of all the currencies is used to store their daily currency change on the basis of Indian rupees.
	text file on daily basis is saved as -> test_(DATE_OF_EXECUTION).txt
	CSV file on daily basis is saved as -> test_(DATE_OF_EXECUTION).csv
"""

import requests 
import json 
import csv 
import datetime 
now=datetime
def convert_and_print(FROM,TO):
	DAILY_CONVERSION_API="https://free.currencyconverterapi.com/api/v6/convert?q="+FROM+"_"+TO+"&compact=ultra"
	data=requests.get(url=DAILY_CONVERSION_API)
	jsonData=data.json()
	#print (FROM, " to ", TO)
	#print(jsonData[FROM+"_"+TO])
	value=jsonData[FROM+"_"+TO]
	print (value)
	return value

#list of the currency code for all the countries 
countryCodes={"ALL","XCD","EUR","BBD","BTN","BND","XAF","CUP","USD","FKP","GIP","HUF","IRR","JMD","AUD","LAK","LYD","MKD","XOF","NZD","OMR","PGK","RWF","WST","RSD","SEK","TZS","AMD","BSD","BAM","CVE","CNY","CRC","CZK","ERN","GEL","HTG","INR","JOD","KRW","LBP","MWK","MRO","MZN","ANG","PEN","QAR","STD","SLL","SOS","SDG","SYP","AOA","AWG","BHD","BZD","BWP","BIF","KYD","COP","DKK","GTQ","HNL","IDR","ILS","KZT","KWD","LSL","MYR","MUR","MNT","MMK","NGN","PAB","PHP","RON","SAR","SGD","ZAR","SRD","TWD","TOP","VEF","DZD","ARS","AZN","BYR","BOB","BGN","CAD","CLP","CDF","DOP","FJD","GMD","GYD","ISK","IQD","JPY","KPW","LVL","CHF","MGA","MDL","MAD","NPR","NIO","PKR","PYG","SHP","SCR","SBD","LKR","THB","TRY","AED","VUV","YER","AFN","BDT","BRL","KHR","KMF","HRK","DJF","EGP","ETB","XPF","GHS","GNF","HKD","XDR","KES","KGS","LRD","MOP","MVR","MXN","NAD","NOK","PLN","RUB","SZL","TJS","TTD","UGX","UYU","VND","TND","UAH","UZS","TMT","GBP","ZMW","BTC","BYN"}
length=len(countryCodes)
print ("total countires are ",length)
i=0
j=0
count1=0
count2=0
now = datetime.datetime.now()
todayDate=str(now.year)+"-"+str(now.month)+"-"+str(now.day) #today's date 
#base currency on which BlueOptima works is considered as INR 
#we can use two loops considering all the currencies as base currencies to get relative values to all other currencies 
baseCurrency="INR"
for code in countryCodes:
				try :
					value=convert_and_print(baseCurrency,code)	
					count1+=1;
					line=baseCurrency+","+code+","+str(value)+","+todayDate+"\n"
					print (line)
					f=open("test_"+todayDate+".txt","a+")
					f.write(line)
					f.close()
				except :
					print("Sorry! Something wrong with Internet? or So many requests will lead you to get you ip Blocked :P")
					count2+=1;
print ("Passed Api Calls",count1)
print ("Failed Api Calls",count2)

#now the content is stored in text file, let's store in csv with data 
list = []
 
#to use csv write 
writer = csv.writer

try: 
    #pasring the text into the array 
    with open("test_"+todayDate+".txt", "r") as input_file:
        for line in input_file:
            temp_arr = line.split(',')
            list.append(temp_arr)
 
    #reading the text and writing to the csv file 
    todayDate=str(now.year)+"-"+str(now.month)+"-"+str(now.day)
    with open("test_"+todayDate+".csv", "w") as out_file:
        for row in list:
            writer(out_file).writerow(row)
    print("Have written into the csv file for",todayDate)
 
    # Handle errors and write log_file
except Exception as e:
	print ("Some issue occured")
