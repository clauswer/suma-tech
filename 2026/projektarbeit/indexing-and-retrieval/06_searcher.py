"""
Skript das eine integrierte Metadaten- und Volltextsuche auf dem Solr-Core pg_fulltexts realisiert. 

authors: Anja Jungbluth, Sebastian Scherübl, Claus Werner
date: 2026-11-06
version: 1.0
"""

import pysolr
import locale
from datetime import datetime

# True: Metadatensuche in my1stcore
# False: Vollständige Suche in pg_fulltexts
TEST_MODE = False

if TEST_MODE:
    SOLR_CORE_URL = "http://localhost:8983/solr/my1stcore"
else:
    SOLR_CORE_URL = "http://localhost:8983/solr/pg_fulltexts"

locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")


def search(solr, query):

    if TEST_MODE:
        query_fields = "title^5 authors^2 subjects^1"
    else:
        query_fields = (
            "title^5 "
            "authors^2 "
            "subjects^1 "
            "fulltext^2 "
            "fulltext_alternative^3"
        )

    params = {
        "qf": query_fields,
        "defType": "edismax",
        "q.op": "OR",
        "mm": "10%",
        "bf": "recip(ms(NOW,issued),3.16e-11,1,1)",
        "rows": 10,
        "fl": "id,title,issued,authors,language,subjects,score",
        "debugQuery": "true",
    }

    try:
        results = solr.search(query, **params)
    except Exception as error:
        print(f"Fehler bei der Solr-Abfrage: {error}")
        return

    if not results or len(results) == 0:
        print("Ihre Suchanfrage liefert keine Treffer!")
        return

    print(
        f"\n* * * Insgesamt {results.hits} Suchergebnisse "
        f"gefunden - {len(results)} Treffer werden angezeigt. "
        f"* * *\n"
    )

    for i, result in enumerate(results, start=1):

        issued_value = result.get("issued")

        if issued_value:
            issued = datetime.fromisoformat(
                issued_value.replace("Z", "+00:00")
            )
            issued_text = issued.strftime("%d. %B %Y")
        else:
            issued_text = "-"

        # Auch mehrwertige Titelfelder berücksichtigen
        title = result.get("title", "-")
        if isinstance(title, list):
            title = ", ".join(title)

        authors = result.get("authors") or []
        language = result.get("language") or []
        subjects = result.get("subjects") or []

        print(
            f"""Suchtreffer # {i} (ID: {result.get('id')}): {title}
          Autor: {", ".join(authors)}
          Aufnahmedatum: {issued_text}
          Sprache: {", ".join(language)}
          Themengebiete: {", ".join(subjects)}
          Score-Wert: {result.get("score")}
"""
        )


if __name__ == "__main__":

    print("Project Gutenberg - Metadaten- und Volltextsuche")
    print(f"Solr-Core: {SOLR_CORE_URL}")
    print("Gib eine Suchanfrage ein oder 'quit!' zum Verlassen.")

    solr = pysolr.Solr(SOLR_CORE_URL, timeout=30)

    while True:
        user_query = input("Suchanfrage: ").strip()

        if user_query.lower() == "quit!":
            break
        elif user_query:
            search(solr, user_query)
