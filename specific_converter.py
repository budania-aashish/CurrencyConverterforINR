"""
	this script takes the currency codes of two coutries and amount to change to target currency from base currency 
""" 

import requests 
import datetime 

def findValue(FROM,TO):
	try :
		DAILY_CONVERTER_API = "https://free.currencyconverterapi.com/api/v6/convert?q="+FROM+"_"+TO+"&compact=ultra"
		data=requests.get(url=DAILY_CONVERTER_API)
		jsonData=data.json()
		value=float(jsonData[FROM+"_"+TO])
		#print ("1 "+ FROM+ " to "+ T +"equals "+value)
		return value;
	except :
		print ("Some error occured :(")

FROM=input("Enter your base currency code , for example Enter INR for Indian Rupees\n")
TO=input("Enter your target currency code, for example Enter USD for US Dollars\n")
AMOUNT=float(input("Enter amount to get value in target currency\n"))

print ("The total amount in "+TO+ " is \n")
print (str(AMOUNT*findValue(FROM,TO)).format('{0:.6f}', 2))
print ("\n")
