from flask import Flask
from dotenv import load_dotenv
from pass_logement import PassLogement
from bdd import BDD


# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)

@app.route('/test')
def test():
   return "ok"

@app.route('/fetch_offers')
def fetch_and_notify():

    # authentification
    print("I- authentification....")
    p = PassLogement()
    #p.auth()
    print(p.auth_cookie)
    print("OK","\n")

    # fetch all offers currently available on the website and select the great offers
    print("II- fetch all offers....")
    p.fetch_offers()
    offers = [offer.to_tuple() for offer in p.offers]
    print("OK","\n")
    
    # notify great offers via telegram
    print("IV- notification on great offers via telegram....")
    p.notify_great_offers()
    print("OK","\n")

    # update the database with the current offers
    print("III- update the database with the current offers....")
    bdd = BDD()
    bdd.upsert(offers)
    print(p.great_offers)
    print("OK")

    return "OK"


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080, debug=True)