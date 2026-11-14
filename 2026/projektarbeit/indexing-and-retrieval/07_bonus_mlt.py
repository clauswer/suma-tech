"""
Skript das eine integrierte Metadaten- und Volltextsuche auf dem Solr-Core pg_fulltexts realisiert. 

authors: Anja Jungbluth, Sebastian Scherübl, Claus Werner
date: 2026-11-06
version: 1.0
"""

import pysolr
import locale
from datetime import datetime
import requests

# True: Metadatensuche in my1stcore
# False: Vollständige Suche in pg_fulltexts
TEST_MODE = False

if TEST_MODE:
    SOLR_CORE_URL = "http://localhost:8983/solr/my1stcore"
else:
    SOLR_CORE_URL = "http://localhost:8983/solr/pg_fulltexts"

locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")

MLT_HANDLER_DEFAULTS = {
    "mlt.fl": "fulltext",
    "mlt.mintf": 2,
    "mlt.mindf": 5,
    "mlt.minwl": 5,
    "mlt.maxdfpct": 25,
    "mlt.interestingTerms": "list",
    # das Ausgangsdokument selbst soll nicht in der Trefferliste erscheinen
    "mlt.match.include": "false",
    "mlt.boost": "true",
}


def create_mlt_handler():
    response = requests.get(
        f"{SOLR_CORE_URL}/config/requestHandler"
    )
    response.raise_for_status()

    handlers = response.json()["config"]["requestHandler"]

    if "/mlt" not in handlers:
        response = requests.post(
            f"{SOLR_CORE_URL}/config",
            json={
                "add-requesthandler": {
                    "name": "/mlt",
                    "class": "solr.MoreLikeThisHandler",
                    "defaults": MLT_HANDLER_DEFAULTS
                }
            }
        )
        response.raise_for_status()
        print("MLT-Handler erstellt")

    else:
        print("MLT-Handler bereits vorhanden")




def search_similar(document_id):
    params = {
        "q": f"id:{document_id}",
        "rows": 3,
        "fl": "id,title,authors,score",
        "wt": "json",
        "mlt.maxdfpct": 10,
    }
    response = requests.get(
            f"{SOLR_CORE_URL}/mlt",
            params=params,
            timeout=30
        )
    response.raise_for_status()
    data = response.json()


    similar_docs = data.get("response", {}).get("docs", [])

    print("\n Ähnliche E-Books\n")

    if not similar_docs:
        print("Keine ähnlichen E-Books gefunden.")
    else:
        for i, doc in enumerate(similar_docs, start=1):

            title = doc.get("title", "-")
            if isinstance(title, list):
                title = ", ".join(title)

            authors = doc.get("authors") or []

            print(
                f"""Ähnlicher Treffer #{i} (ID: {doc.get('id')}): {title}
                Autor: {", ".join(authors)}
                Score-Wert: {doc.get('score')}
                """
            )

    print("\n* * * Interesting Terms * * *\n")
    print(data.get("interestingTerms", []))



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
        "rows": 1,
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

#    print(
#        f"\n* * * Insgesamt {results.hits} Suchergebnisse "
#        f"gefunden - {len(results)} Treffer werden angezeigt. "
#        f"* * *\n"
#    )

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

        print(f"""Suchtreffer # {i} (ID: {result.get('id')}): {title} Autor: {", ".join(authors)} Aufnahmedatum: {issued_text} Sprache: {", ".join(language)} Themengebiete: {", ".join(subjects)} Score-Wert: {result.get("score")}""")
    # ID des besten Suchtreffers ermitteln
    document_id = result.get("id")

    # Ähnliche Dokumente suchen
    search_similar(document_id)


if __name__ == "__main__":

    print("Project Gutenberg - Metadaten- und Volltextsuche")
    print(f"Solr-Core: {SOLR_CORE_URL}")
    print("Gib eine Suchanfrage ein oder 'quit!' zum Verlassen.")

    solr = pysolr.Solr(SOLR_CORE_URL, timeout=30)

    create_mlt_handler()

    while True:
        user_query = input("Suchanfrage: ").strip()

        if user_query.lower() == "quit!":
            break
        elif user_query:
            search(solr, user_query)
