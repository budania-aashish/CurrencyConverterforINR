#from datetime import timedelta, date
import datetime
import requests
import pickle
import pandas as pd
from lxml import html


#Collecting Historical Data
"""
Example:

payload={
	"INR":{
		"base" : "USD",
		"historicalData":{
		 	"2017-10-10" : "65.249001",
		} 
	},
	"AUD":{
		"base" : "USD",
		"historicalData":{
		 	"2017-10-10" : "3.672501",
		} 
	}
}
"""

def daterange(date1, date2):
	for n in range(int ((date2 - date1).days)+1):
		yield date1 + datetime.timedelta(n)


def getDate(startDate,endDate):
	df = pd.read_csv("codes-all.csv")  
	countryCodes=df['AlphabeticCode'] #this is the column having currency code 
	countryCodes=countryCodes.tolist() #to put them in a list 
	countryCodes = [x for x in countryCodes if str(x) != 'nan'] #removes all the names where country code is not existing 

	for countryCode in countryCodes:
		for date in daterange(startDate, endDate):
			collectHistoricalData(countryCode,date)



def collectHistoricalData(countryCode,date):
	date=date.strftime("%Y-%m-%d")
	year=date.split("-")[0]
	month=date.split("-")[1]
	day=date.split("-")[2]

	try:
		#resource to collect data is in the URL -> fxtop.com #
		URL="http://fxtop.com/en/currency-converter-past.php?A=1&C1="+countryCode+"&C2=USD&DD="+day+"&MM="+month+"&YYYY="+year+"&B=1&P=&I=1&btnOK=Go%21"
		page = requests.get(url=URL)
		tree = html.fromstring(page.content)
		#craping data from webpage #
		exchangeRate=tree.xpath('//td[@align="center"]/text()')
		exchangeRate=exchangeRate[22].split()[1].split("=")[1]
		if countryCode not in payload:
				#if country code is not added to payload earlier, then only add it # baisically to remove data redundancy 
				newEntry={}
				historicalData={}
				newEntry["base"]="USD"
				historicalData[date]=exchangeRate
				newEntry["historicalData"]=historicalData
				payload[countryCode]=newEntry
		else:
			payload[countryCode]["historicalData"][date] = exchangeRate

	except:
		print("Error in countryCode")

	print(payload)


def addToHistoricalData(sourceCurrency, destinationCurrency):
	if sourceCurrency != "USD":
		collectHistoricalData(sourceCurrency, datetime.datetime.today())
	if destinationCurrency != "USD":
		collectHistoricalData(destinationCurrency, datetime.datetime.today())

def currencyConverter(sourceCurrency, destinationCurrency, amount):
	todayDate=datetime.datetime.today().strftime('%Y-%m-%d')
	year=todayDate.split("-")[0]
	month=todayDate.split("-")[1]
	day=todayDate.split("-")[2]

	try:
		URL="http://fxtop.com/en/currency-converter-past.php?A=1&C1="+sourceCurrency+"&C2="+destinationCurrency+"&DD="+day+"&MM="+month+"&YYYY="+year+"&B=1&P=&I=1&btnOK=Go%21"
		page = requests.get(url=URL)
		tree = html.fromstring(page.content)
		response=tree.xpath('//td[@align="center"]/text()')
		response1=response[20].split()[1].split("=")
		countryCode=response1[0]
		exchangeRate=response1[1]
		amount=float(amount)*float(exchangeRate)
		print("Amount: ",amount)
		addToHistoricalData(sourceCurrency, destinationCurrency)
	except:
		print("FAILURE")



payload={} #global access 
startDate = datetime.date(2018, 9, 10)
endDate = datetime.date(2018, 9, 11)
getDate(startDate,endDate)
pickle.dump( payload, open( "historicalData.p", "wb" ) )

payload=pickle.load( open("historicalData.p", "rb" ) )
currencyConverter('AUD', 'INR', 2)
#print(payload)


print (payload['AUD']['historicalData']['2018-09-11']) #gives AUD in dollars from stored historicalData on 2018-09-11 