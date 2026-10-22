#!/bin/python

"""
Skript zum Laden von E-Book-Volltexten aus dem Project Gutenberg. Die IDs der E-Books werden aus der Textdatei ebook_ids.txt gelesen. Für jede ID wird die entsprechende Volltextdatei heruntergeladen und im Ordner fulltexts gespeichert.

authors: Anja Jungbluth, Sebastian Scherübl, Claus Werner
date: 2024-10-06
version: 1.0
"""


import requests
import os
import time

def download_file(url, filename):
    """
    Lädt eine UTF-8-codierte Textdatei von der angegebenen URL herunter und speichert sie als UTF-8-codierte Textdatei
    unter dem angegebenen Namen im lokalen Dateisystem. Bei der Textdatei handelt es sich um den Volltext eines
    E-Books aus dem Project Gutenberg. Die Funktion wartet zufällig zwischen 0.5 und 2 Sekunden, bevor sie die Datei
    von der angegebenen URL herunterlädt, um den Webserver von Project Gutenberg nicht zu überlasten.

    Parameter:
    - url (str): URL der Textdatei, die vom Project Gutenberg heruntergeladen werden soll.
    - filename (str): Der Name der lokal abzuspeichernden Datei.
    """

    # zwischen 0.5 und 2 Sekunden zufällig warten
    time.sleep(0.5 + 1.5 * (os.urandom(1)[0] / 255))

    response = requests.get(url, timeout=60, stream=True)
    response.encoding = 'utf-8'
    if response.status_code == requests.codes.ok:
        with open(filename, "w", encoding="utf-8") as file: 
            file.write(response.text)
        print(f"Datei erfolgreich heruntergeladen und gespeichert unter {filename}")
        return True

    print(f"Fehler beim Herunterladen der Datei von URL {url}: {response.status_code}")
    return False


def check_empty_file(file_path):
    """
    Prüft, ob eine Datei leer ist. 

    Parameter:
    - path (os.path oder str): Speicherort der Datei

    returns:
    - true wenn Datei leer ist
    - false wenn Datei nicht leer ist
    """

    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)

        if file_size == 0:
            print(f"Datei ohne Inhalt: {file_path}")
            return True
        return False



if __name__ == "__main__":

    # Ordner fulltexts erstellen, falls er nicht existiert
    base_dir = "fulltexts"
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)

    # Counter
    num_of_downloads = 0
    num_of_errors = 0
    num_of_empty_files = 0

    # IDs aus der Textdatei einlesen und Volltextdateien herunterladen
    try:
        with open("ebook_ids.txt", "r", encoding="utf-8") as file:
            for ebook_id in file.readlines():
                ebook_id = ebook_id.strip()  # Entfernen ggf. vorandener führender und nachgestellter Leerzeichen und Zeilenumbrüche
                output_file = os.path.join(base_dir, f"{ebook_id}.txt")
                
                if not os.path.exists(output_file):
                    url = f"https://www.gutenberg.org/ebooks/{ebook_id}.txt.utf-8"
                    print(f"Herunterladen der Textdatei von {url}")       
                    
                    if download_file(url, output_file):
                        num_of_downloads += 1
                    else:
                        num_of_errors += 1
                    
                    if check_empty_file(output_file):
                        num_of_empty_files += 1
    except Exception as e:
        print(f"Es ist ein Fehler aufgetreten: {e}")
    finally:
        # Ausgaben
        print(f"{num_of_downloads} Textdateien heruntergeladen.")
        print(f"Anzahl der Fehler: {num_of_errors}")
        print(f"Anzahl der leeren Dateien: {num_of_empty_files}")