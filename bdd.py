import mysql.connector
import os

# Now you can access the variables using os.environ
BDD_HOST=os.getenv("BDD_HOST")
BDD_USERNAME=os.getenv("BDD_USERNAME")
BDD_PASSWORD=os.getenv("BDD_PASSWORD")
BDD_DATABASE=os.getenv("BDD_DATABASE")


class BDD():

    def __init__(self):
        # Créer une connexion à la base de données
        try:
            connection = mysql.connector.connect(
                host=BDD_HOST,  # Adresse de l'hôte
                user=BDD_USERNAME,  # Nom d'utilisateur
                password=BDD_PASSWORD,  # Mot de passe
                database=BDD_DATABASE  # Nom de la base de données à laquelle se connecter
            )

            if connection.is_connected():
                print("Connexion réussie à la base de données")
                self.connection = connection

        except mysql.connector.Error as err:
            print("Erreur lors de la connexion à la base de données:", err)

    
    def upsert(self, data):
        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()

        # Example of an INSERT operation
        sql_insert_query = """
            INSERT INTO offers (
                id, reference, accommodationTypeLabel, surface, rentalPrice, roommate, dalo, city, _address,
                zipcode, numberCandidatesOnOffer, partnerLabel, dateCreated, dateUpdated, dateValidity 
            ) 
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                reference = VALUES(reference),
                accommodationTypeLabel = VALUES(accommodationTypeLabel),
                surface = VALUES(surface),
                rentalPrice = VALUES(rentalPrice),
                roommate = VALUES(roommate),
                dalo = VALUES(dalo),
                city = VALUES(city),
                _address = VALUES(_address),
                zipcode = VALUES(zipcode),
                numberCandidatesOnOffer = VALUES(numberCandidatesOnOffer),
                partnerLabel = VALUES(partnerLabel),
                dateCreated = VALUES(dateCreated),
                dateUpdated = VALUES(dateUpdated),
                dateValidity = VALUES(dateValidity);                               
            """

        # Data to insert
        record_to_insert = [(1, 'John', 50000)]

        # Execute the INSERT query
        cursor.executemany(sql_insert_query, data)

        # Commit the transaction
        self.connection.commit()


    def query(self, req):
        # Create a cursor object to execute SQL queries
        cursor = self.connection.cursor()
        cursor.execute(req)

        # Récupérer les résultats
        rows = cursor.fetchall()

        for row in rows:
            print(row)

        # Fermer le curseur
        cursor.close()
        
        return rows



