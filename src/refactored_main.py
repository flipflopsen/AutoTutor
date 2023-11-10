import requests
import configparser
import os
import re

from requests.auth import HTTPBasicAuth
from tqdm import tqdm
from studi_abgabe import student_delivery as Delivery
from utils import student_delivery_ops as DeliveryUtil
from utils import tutor_evaluation as TutorConstants

# globals
global config, username, password, tutorChar, numberOfTutors

# constants (TODO: maybe move to config file for abstraction)
api_url = 'https://elearning.uni-oldenburg.de/api.php/'


def entry():
    print("Wilkommen beim AutoDownloader!")
    numberInputIncomplete = True
    tutorInputIncomplete = True
    genFalscheAbgabenIncomplete = True

    while numberInputIncomplete:
        try:
            number = int(input("Welches Übungsblatt? UE"))
            if(number <= 0 or number > 100):
                raise ValueError
            numberInputIncomplete = False
            if number < 10:
                blattnummer = "0"+str(number)
            else:
                blattnummer = str(number)    
        except ValueError:
            print("Ungültige Eingabe. Bitte geben eine Zahl zwichen 0 und 14 ein.")
    print(f"Übungsblatt UE{blattnummer} ausgewählt.")

    if(config['Tutoren']['UseTutoriumBuchstabe'] == True):
        tutorInputIncomplete = False

    valdidCofig = True
    while tutorInputIncomplete:
        tutorien = "ADFIBJGC"
        if(config['Tutoren']['UseTutoriumBuchstabe'] == 'Ja' and valdidCofig):
            tutorInputIncomplete = False
            print(f"Willkommen zurück Tutor {tutorBuchstabe}")
        else:
            try:
                tutorBuchstabe = input("Welcher Tutor bist du? ")
                tutorBuchstabe = tutorBuchstabe.upper()
                if(tutorBuchstabe not in tutorien):
                    raise ValueError
                tutorInputIncomplete = False
                print(f"Willkommen zurück Tutor {tutorBuchstabe}")
            except ValueError:
                print("Ungültige Eingabe. Bitte geben einen Buchstaben zwichen A und J ein.")
                continue
        try:
            number = tuturBuchstabeInNummer[tutorBuchstabe]
            tutorNumber = tutorNumberPicker[blattnummer][number]
        except Exception:
            tutorInputIncomplete = True
            valdidCofig = False
            print("Etwas ist schief gelaufen :/ Bitte versuche es manuell")


    while genFalscheAbgabenIncomplete:
        try:
            str = input("E-Mail-Liste mit den falschen Abgaben generieren (y/n)? ")
            if str == 'n':
                genFalscheAbgaben = False
            elif str == 'y':
                genFalscheAbgaben = True
            else:        
                raise ValueError
            genFalscheAbgabenIncomplete = False
        except ValueError:
            print("Ungültige Eingabe. Wähle y = ja oder n = nein.")

    # Restliche Config
    pattern = f"^UE{blattnummer}_\w+(\[\d+\])?\.zip$" #^UE\d{2}_\w+(\[\d+\])?\.zip$
    #patternTeam = f'UE{blattnummer}_(.*?)\.zip' 

    patternTeam = f'UE{blattnummer}_([\w\s]+)(?:\[.*\])?\.zip'
    targetDir = os.path.normpath(config['Dateien']['Speicherort']) 

    try:
        os.makedirs(targetDir)
        print(f'Downloadordner mit dem Pfad {targetDir} erstellt')
    except FileExistsError:
        # Ordner gibt es schon
        pass



def parse_config():
    global config, username, password, tutorChar, numberOfTutors

    config = configparser.ConfigParser()
    config.read('config.ini')
    username = config['API']['Username']
    password = config['API']['Passwort']
    tutorChar = config['Tutoren']['TutoriumBuchstabe']
    numberOfTutors = int(config['Tutoren']['AnzahlDerTutoren'])







def main():
    print("Hiu")

if __name__ == "__main__":
    main()