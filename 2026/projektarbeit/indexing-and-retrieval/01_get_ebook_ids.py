#!/bin/python

"""
Skript zum Abfragen eines lokalen Solr-Servers und Ermitteln aller IDs von E-Books, die in deutscher Sprache vorliegen und den Dokumenttyp Text besitzen. Die IDs werden in der Textdatei ebook_ids.txt abgespeichert (eine ID pro Zeile). Die Anzahl der gespeicherten E-Book-IDs wird auf der Konsole ausgegeben.

authors: Anja Jungbluth, Sebastian Scherübl, Claus Werner
date: 2024-06-10
version: 1.0
"""

import pysolr
import json
import logging

logging.basicConfig(format='%(levelname)s: %(message)s')

# Solr-Host-URI zum Solr-Core
solr_host = "http://localhost:8983/solr/my1stcore"

# Solr-Instanz erstellen
solr = pysolr.Solr(solr_host, timeout=10)

# Error-Handling für die Verbindung zum Solr-Server
try:
    solr.ping()
except pysolr.SolrError as e:
    logging.error(f"Fehler beim Verbinden mit Solr: {e}")
    exit(1)

# Error-Handling für die Antwort vom Solr-Server
try:
    json.loads(solr.ping())
except json.JSONDecodeError:
    logging.error("Fehler: Die Antwort vom Solr-Server ist kein gültiges JSON.")
    exit(1)


# Liste zum Sammeln der IDs
ebook_ids = []


# Ergebnisse mittels Cursor abfragen:
for doc in solr.search(q='type:Text AND language:de', fl='id',sort='id ASC',cursorMark='*'):
    ebook_ids.append(doc['id'])

# IDs in Textdatei speichern
filename = "ebook_ids.txt" 
with open(filename, "w", encoding="utf-8") as f:
    for id in ebook_ids:
        f.writelines(id+"\n")

# Ausgabe der Anzahl
print(f"{len(ebook_ids)} IDs gefunden und in {filename} gespeichert.")