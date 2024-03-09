import requests
import os
import json
from datetime import datetime


# Now you can access the variables using os.environ
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
TELEGRAM_CHATID=os.getenv("TELEGRAM_CHATID")
TELEGRAM_BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")

class PassLogement:
    
    def __init__(self):
        self.auth_cookie = "PHPSESSID=3dbpu25s7cl5djbk635sva1776"
        #pass
    
    def auth(self):
        login_url = 'https://offres.passlogement.com/account/auth/login'
        data = {
            "username": USERNAME,
            "password": PASSWORD
        }

        session = requests.Session()
        response = session.post(login_url, data=data)

        if response.ok:
            self.auth_cookie = response.headers["Set-Cookie"].split(";")[0]
        else:
            print("Échec de l'authentification. Vérifiez vos informations d'identification.")
    
    def fetch_offers(self):
        login_url = "https://offres.passlogement.com/account/offer/listing/json"
        custom_headers = {
            "Cookie": self.auth_cookie
        }

        session = requests.Session()
        response = session.get(login_url, headers=custom_headers)
        json_offers = json.loads(response.content)["offer"]
        self.offers = [Offer(o) for o in json_offers]
        self.great_offers = [offer for offer in self.offers if offer.is_great_offer()]

    
    def notify_great_offers(self):

        message = f"""
                ALERTE BONNES OFFRES !

        {"".join([offer.to_str() for offer in self.great_offers])}
        """

        # URL for the Telegram Bot API endpoint to send messages
        url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

        # Parameters for the message
        params = {
            'chat_id': TELEGRAM_CHATID,
            'text': message
        }

        # Send the message
        response = requests.get(url, params=params)

        # Check if the message was sent successfully
        if response.status_code == 200:
            print("Message sent successfully")
        else:
            print("Failed to send message:", response.text)


class Offer:

    def __init__(self,json: dict):
        self.id = int(json["id"])
        self.reference = json["specialId"]
        self.accommodationTypeLabel = json["accommodationTypeLabel"]
        self.surface = int(json["surface"])
        self.rentalPrice = float(json["rentalPrice"])
        self.roommate = int(json["roommate"])
        self.dalo = int(json["dalo"])
        self.city = json["city"]
        self._address = json["address"]
        self.zipcode = int(json["zipcode"])
        self.numberCandidatesOnOffer = int(json["numberCandidatesOnOffer"])
        self.partnerLabel = json["partnerLabel"] 
        self.dateCreated = datetime.strptime(json["dateCreated"], "%Y-%m-%d %H:%M:%S")
        self.dateUpdated = datetime.strptime(json["dateUpdated"], "%Y-%m-%d %H:%M:%S") 
        self.dateValidity = datetime.strptime(json["dateValidity"], "%Y-%m-%d").date()

    
    def is_great_offer(self):
        sine_qua_none = self.dalo==0 and self.roommate==0 and self.rentalPrice<=9010 and self.numberCandidatesOnOffer<5
        great_T1_2 = self.rentalPrice<=600 and int(self.accommodationTypeLabel[-1]) < 3
        great_T3 = self.rentalPrice<=1100 and int(self.accommodationTypeLabel[-1]) >= 3

        return sine_qua_none and (great_T1_2 or great_T3)


    def to_tuple(self):
        return (self.id,self.reference,self.accommodationTypeLabel,self.surface,self.rentalPrice,self.roommate,self.dalo,self.city,self._address,self.zipcode,self.numberCandidatesOnOffer,self.partnerLabel,self.dateCreated,self.dateUpdated,self.dateValidity)


    def to_str(self):
        return  f"""
        Adresse: {self._address.capitalize()}, {self.zipcode} {self.city.capitalize()}
        Loyer: {self.rentalPrice} €
        Surface: {self.surface} m² ({self.accommodationTypeLabel})
        nombre de candidats: {self.numberCandidatesOnOffer}

        """
