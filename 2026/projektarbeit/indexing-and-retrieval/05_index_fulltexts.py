#!/bin/python

"""
Skript zum Einlesen von Volltexten aus dem Verzeichnis `fulltexts` und Indexierung der Volltexte zusammen mit den Metadaten in den Solr-Core `pg_fulltexts`.
Die Metadaten werden aus dem Solr-Core `my1stcore` abgefragt, basierend auf der E-Book-ID, die aus dem Dateinamen der Volltextdateien extrahiert wird.

authors: Anja Jungbluth, Sebastian Scherübl, Claus Werner
date: 2024-10-27
version: 1.0
"""

import pysolr
import os
import sys
import logging
import json 

from _01_get_ebook_ids import create_solr_instance

logging.basicConfig(format='%(levelname)s: %(message)s')


def query_ebook_id(solr_instanz:pysolr.Solr, ebook_id:str):
    """Solr-Query nach einer ebook_id.
    
    Parameter:
    - solr_instanz (pysolr.Solr): Objekt für die abzufragende Solr-Instanz
    - ebook_id (str): Die ID des E-Books, nach dem gesucht werden soll

    Returns:
    - doc (json): JSON-Objekt mit den Angaben zu Titel, Autoren, Sprachen, Subjects und Erstelldatum im Project Gutenberg
    """

    query = f"id:{ebook_id}"

    # TODO: Error-Handling: if response.docs -> denn wenn es keine treffer gibt, ist dies eine leere Liste, somit falsy

    return solr_instanz.search(q=query, fl='id,title,authors,language,subjects,issued', wt="json")


def read_fulltext_file(file_path: str) -> str:
    """Liest den Volltext aus einer Datei ein.

    Parameter:
    - file_path (str): Pfad zur Volltextdatei

    Returns:
    Inhalt der Volltextdatei als String
    """

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
        
    except FileNotFoundError:
        logging.error(f"Datei nicht gefunden: {file_path}")
        return ""
    
    except IOError as e:
        logging.error(f"Fehler beim Lesen der Datei {file_path}: {e}")
        return ""


if __name__ == "__main__":

    # Für Debugging kann ein E-Book-ID beim Skript-Aufruf als Argument übergeben werden, um die Solr-Query zu testen
    if len(sys.argv) == 2:
        try:
            ebook_id = int(sys.argv[1])
        except (ValueError, IndexError):
            logging.error("Bitte geben Sie eine gültige E-Book-ID als Argument an.")
            exit(1)

        solr_instance = create_solr_instance("http://localhost:8983/solr/my1stcore")
        response = query_ebook_id(solr_instance, ebook_id)
        
        if not response.docs:
            logging.error(f"Keine Treffer für E-Book-ID {ebook_id} gefunden.")
            exit(1)

        print(f"Response:\n{response.docs[0]}")


    # Normaler Programmablauf
    else:

        indexing_counter = 0
        error_counter = 0

        logging.info("Solr-Instanzen erstellen.")
        my1stcore_instance = create_solr_instance("http://localhost:8983/solr/my1stcore")
        pg_fulltexts_instance = create_solr_instance("http://localhost:8983/solr/pg_fulltexts")

        # flitered.txt-files aus fulltexts laden
        filelist = [file for file in os.listdir("fulltexts") if file.endswith("filtered.txt")]

        # Daten zu den Titeln aus my1stcore laden
        for file in filelist:
            id = file.split("_")[0]

            logging.info(f"Lade Daten aus my1stcore zu ID {id}.")
            response = query_ebook_id(solr_instanz=my1stcore_instance, ebook_id=id)

            if not response.docs:
                logging.warning(f"Keine Metadaten für E-Book-ID {id} gefunden. Überspringe Datei {file}.")
                error_counter += 1
                continue

            logging.info(f"Ergänze Text aus {file}.")
            response["fulltext"] = read_fulltext_file(file)

            logging.info(f"Lade Daten zu ID {id} in pg_fulltexts.")
            pg_fulltexts_instance.add([response])
            # TODO: muss das nicht bei respones.docs erägnzt werden???

            logging.info(f"Indexiere Daten zu ID {id} in pg_fulltexts.")
            pg_fulltexts_instance.commit()

            logging.info(f"Indexierung zu ID {id} abgeschlossen.")
            indexing_counter += 1

        logging.info(f"Indexierung abgeschlossen. Insgesamt {indexing_counter} Dokumente indexiert. Fehler bei {error_counter} Dokumenten.")