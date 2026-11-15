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
import csv
import json

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



def parameter_test(document_id):

    mintf = 2
    mindf = 5
    minwl = 5
    maxdfpct = 25
    match_include = "false"
    boost = "true"

    # mintf verändern
    search_similar(document_id, 3, mindf, minwl, maxdfpct, match_include, boost)
    search_similar(document_id, 12, mindf, minwl, maxdfpct, match_include, boost)

    # mindf verändern
    search_similar(document_id, mintf, 6, minwl, maxdfpct, match_include, boost)
    search_similar(document_id, mintf, 15, minwl, maxdfpct, match_include, boost)

    # minwl verändern
    search_similar(document_id, mintf, mindf, 6, maxdfpct, match_include, boost)
    search_similar(document_id, mintf, mindf, 15, maxdfpct, match_include, boost)

    # maxdfpct verändern
    search_similar(document_id, mintf, mindf, minwl, 26, match_include, boost)
    search_similar(document_id, mintf, mindf, minwl, 35, match_include, boost)

    # match.include verändern
    search_similar(document_id, mintf, mindf, minwl, maxdfpct, "true", boost)

    # boost verändern
    search_similar(document_id, mintf, mindf, minwl, maxdfpct, match_include, "false")



def search_similar(document_id, mintf, mindf, minwl, maxdfpct, match_include, boost):

    params = {
        "q": f"id:{document_id}",
        "rows": 3,
        "fl": "id,title,authors,score",
        "wt": "json",
        "mlt.mintf": mintf,
        "mlt.mindf": mindf,
        "mlt.minwl": minwl,
        "mlt.maxdfpct": maxdfpct,
        "mlt.match.include": match_include,
        "mlt.boost": boost
    }

    response = requests.get(
        f"{SOLR_CORE_URL}/mlt",
        params=params,
        timeout=30
    )
    response.raise_for_status()
    data = response.json()

    similar_docs = data.get("response", {}).get("docs", [])
    interesting_terms = data.get("interestingTerms", [])

    print("\n Ähnliche E-Books \n")

    if not similar_docs:
        print("Keine ähnlichen E-Books gefunden.")
    else:
        for i, doc in enumerate(similar_docs, start=1):

            title = doc.get("title", "-")
            if isinstance(title, list):
                title = ", ".join(title)

            authors = doc.get("authors") or []

            print(
                f"Ähnlicher Treffer #{i} "
                f"(ID: {doc.get('id')}): {title} "
                f"Autor: {', '.join(authors)} "
                f"Score-Wert: {doc.get('score')}"
            )

    print("\n Interesting Terms \n")
    print(interesting_terms)

    with open("mlt_tests.csv", "a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        writer.writerow([
            f"mintf={mintf}, mindf={mindf}, minwl={minwl}, "
            f"maxdfpct={maxdfpct}, match.include={match_include}, boost={boost}"
        ])

        for doc in similar_docs:

            title = doc.get("title", "-")
            if isinstance(title, list):
                title = ", ".join(title)

            writer.writerow([
                title,
                doc.get("id"),
                doc.get("score")
            ])

        writer.writerow([
            "Interesting Terms",
            json.dumps(interesting_terms, ensure_ascii=False)
        ])

        writer.writerow([])




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
            """
        )
    # ID des besten Suchtreffers ermitteln
    document_id = result.get("id")

    # Ähnliche Dokumente suchen
    search_similar(document_id, 2, 5, 5, 25, "false", "true")
    #Parametertest
    parameter_test(document_id)


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
