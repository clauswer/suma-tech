
#!/usr/bin/env python3

"""
Indexiert gefilterte Project-Gutenberg-Volltexte
zusammen mit ihren Metadaten im Solr-Core pg_fulltexts.

Metadatenquelle: my1stcore
Volltextdateien: fulltexts/<ebook_id>_filtered.txt

Aufruf:
    python 05_index_fulltexts.py
    python 05_index_fulltexts.py 19794
"""

import os
import sys
import logging
import pysolr

from pathlib import Path

from _01_get_ebook_ids import create_solr_instance

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    force=True
)

# Aktuelles Arbeitsverzeichnis (suma-tech)
SCRIPT_DIR = Path.cwd()

# Verzeichnis mit den Volltextdateien
FULLTEXT_DIR = SCRIPT_DIR / "fulltexts"

METADATA_CORE = "http://localhost:8983/solr/my1stcore"
FULLTEXT_CORE = "http://localhost:8983/solr/pg_fulltexts"


def query_ebook_id(solr_instance, ebook_id):
    """Lädt die Metadaten eines E-Books aus my1stcore."""

    return solr_instance.search(
        f"id:{ebook_id}",
        fl="id,title,authors,language,subjects,issued",
        rows=1
    )


def read_fulltext_file(file_path):
    """Liest einen gefilterten Volltext ein."""

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except (OSError, UnicodeError) as error:
        logging.error(
            f"Fehler beim Lesen von {file_path}: {error}"
        )
        return ""


def prepare_document(metadata, fulltext):
    """Bereitet Metadaten und Volltext für Solr vor."""

    document = dict(metadata)

    # Titelfeld im neuen Core ist nicht mehrwertig
    title = document.get("title")

    if isinstance(title, list):
        document["title"] = title[0] if title else ""

    # Mehrwertige Felder sicherstellen
    for field in ("authors", "language", "subjects"):
        value = document.get(field)

        if value is None:
            document[field] = []
        elif not isinstance(value, list):
            document[field] = [value]

    # Volltext ergänzen
    document["fulltext"] = fulltext

    return document


def index_ebook(metadata_solr, fulltext_solr, file_path):
    """Indexiert ein einzelnes E-Book."""

    filename = os.path.basename(file_path)
    ebook_id = filename.split("_")[0]

    logging.info(f"Verarbeite E-Book-ID {ebook_id}")

    try:
        response = query_ebook_id(
            metadata_solr,
            ebook_id
        )

        if not response.docs:
            logging.warning(
                f"Keine Metadaten für ID {ebook_id} gefunden."
            )
            return False

        metadata = response.docs[0]

        fulltext = read_fulltext_file(file_path)

        if not fulltext.strip():
            logging.warning(
                f"Leerer Volltext für ID {ebook_id}."
            )
            return False

        document = prepare_document(
            metadata,
            fulltext
        )

        fulltext_solr.add(
            [document],
            commit=False
        )

        logging.info(
            f"E-Book-ID {ebook_id} zur Indexierung übertragen."
        )

        return True

    except Exception as error:
        logging.error(
            f"Fehler bei E-Book-ID {ebook_id}: {error}"
        )
        return False

def main():

    print("Indexierung gestartet.")
    print(f"Arbeitsverzeichnis: {SCRIPT_DIR}")
    print(f"Volltextverzeichnis: {FULLTEXT_DIR}")
    print(f"Verzeichnis vorhanden: {FULLTEXT_DIR.is_dir()}")

    # Hier folgt der bisherige Code ...
    
    metadata_solr = create_solr_instance(METADATA_CORE)
    fulltext_solr = create_solr_instance(FULLTEXT_CORE)

    if len(sys.argv) > 2:
        logging.error(
            "Aufruf: python 05_index_fulltexts.py [ebook_id]"
        )
        return

    # Optional nur eine E-Book-ID indexieren
    if len(sys.argv) == 2:
        ebook_id = sys.argv[1]

        if not ebook_id.isdigit():
            logging.error("Ungültige E-Book-ID.")
            return

        filenames = [f"{ebook_id}_filtered.txt"]

    else:
        filenames = sorted(
            filename
            for filename in os.listdir(FULLTEXT_DIR)
            if filename.endswith("_filtered.txt")
        )

    success_counter = 0
    error_counter = 0

    for filename in filenames:

        file_path = os.path.join(
            FULLTEXT_DIR,
            filename
        )

        if index_ebook(
            metadata_solr,
            fulltext_solr,
            file_path
        ):
            success_counter += 1
        else:
            error_counter += 1

    if success_counter > 0:
        try:
            fulltext_solr.commit()
            logging.info("Solr-Commit erfolgreich.")
        except Exception as error:
            logging.error(f"Commit fehlgeschlagen: {error}")
            return

    logging.info(
        f"Indexierung abgeschlossen: "
        f"{success_counter} übertragen, "
        f"{error_counter} Fehler."
    )


if __name__ == "__main__":
    main()
