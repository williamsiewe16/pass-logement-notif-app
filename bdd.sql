#################################################################################################
#                                                                                               #
#                               PASS_LOGEMENT_NOTIF_APP_BDD                                     #
#                                                                                               #
#################################################################################################

DROP DATABASE IF EXISTS pass_logement_bd;
CREATE DATABASE pass_logement_bd;
USE pass_logement_bd;

CREATE TABLE offers(
    id INT PRIMARY KEY,
    reference VARCHAR(100),
    accommodationTypeLabel VARCHAR(100),
    surface INT,
    rentalPrice FLOAT,
    roommate INT,
    dalo INT,
    city VARCHAR(100),
    _address VARCHAR(100),
    zipcode INT,
    numberCandidatesOnOffer INT,
    partnerLabel VARCHAR(100),
    dateCreated DATETIME,
    dateUpdated DATETIME,
    dateValidity DATE
)

