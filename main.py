import requests
import telebot
import ipaddress  
import validators
import translate

def emp(txt):
	if(txt==''):
		return True
	else:

		return False
def checkIp(ip): # check if it is ip address
    
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        return False


def valdURL(txt): # check if it is URL 
	if(validators.url(txt)):
		return True
	else:
		return False

trans = translate.Translator(from_lang="en", to_lang="ar")

bot = telebot.TeleBot("Token")
@bot.message_handler(commands=["start","Start","ابدأ","أبدأ","ابدا" ,"أبدا"])
def reply(message):
	bot.send_message(message.from_user.id,f"مرحبا {message.from_user.first_name} نورتنا 😊\nفي حال واجهتك مشكلة تواصل معي\n https://mobile.twitter.com/_ii404")
	bot.send_message(message.from_user.id,f"\n الرجاء ادخال عنوان IP")
	
@bot.message_handler(content_types="text")
def response(message):
	if(checkIp(message.text)):
			payload = {f"ip":{message.text},"apikey":"apikey"}

			urll = "API"
			head =  {
				"API key"
			}

			req = requests.get(urll,headers=head,params=payload).json()

			try:
				list = [
				req["flag"], 

				f"{req['country']}" , 

				f"{req['countryCapital']}",

				f"{req['timezone']}", 

				
				f"{req['phoneCode']} ",

				f"{req['gmt']} "
				] #Create list to store json values

				arbi = ['','',"العاصمة","المنطقة الزمنية ","رمز الهاتف ",""]
				ctr=0
			
				for i in range(len(list)):
					if(ctr==4 or ctr==5 ): # Values I don't want to translate it
						rep = list[i].replace("''",'')
						arab= arbi[i]
						
						bot.send_message(message.from_user.id,f"{arab}  {rep}")
					elif(not list[i].strip().isdigit() and not valdURL(list[i]) and not emp(arbi[i])): #Check if it is string and not URL 
						TranslateTxt = trans.translate(list[i].replace("''",'')) #Translate string and remove ""
						bot.send_message(message.from_user.id,f"{arbi[i]} : {TranslateTxt}    {list[i]}") 
					elif(emp(arbi[i]) and not valdURL(list[i])):
						translatee = trans.translate(list[i])
						
						bot.send_message(message.from_user.id, translatee)
					elif(valdURL(list[i])):
						bot.send_photo(message.from_user.id,list[i])
			
					else:
						bot.send_message(message.from_user.id,f"{str(list[i])}")
					ctr+=1
					
			except Exception :
				bot.send_message(message.from_user.id,"الرجاء التحقق من عنوان IP")
	else:
		bot.send_message(message.from_user.id,"الرجاء التحقق من عنوان IP")

bot.infinity_polling()

