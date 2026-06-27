import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path

def fetch_books_by_author_id(author_id):
    """
    Gibt eine Liste von URLs für alle Werke eines Autors mit der angegebenen ID zurück.
    """

    # URL der HTML-Seite mit allen deutschsprachigen E-Books
    URL = "https://www.gutenberg.org/browse/languages/de"

    # HTML-Seite abrufen
    response = requests.get(URL)
    response.encoding = 'utf-8'
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Seite: {response.status_code}")
        return []

    # HTML-Seite parsen
    soup = BeautifulSoup(response.text, "html.parser")

    # Abschnitt mit h2-Überschrift des Autorennamens in der HTML-Seite finden
    author_section = None
    for h2 in soup.find_all("h2"):
        a_tag = h2.find("a", {"id": "a" + str(author_id)})
        if a_tag:
            author_section = h2
            break

    if not author_section:
        print("Autor-Abschnitt im HTML nicht gefunden.")
        return []

    # Die folgende <ul>-Liste durchsuchen
    book_list = author_section.find_next_sibling("ul")
    if not book_list:
        print("Keine Liste mit Werken des Autors gefunden.")
        return []

    # Alle <li>-Elemente extrahieren, die einen Link enthalten
    books = []
    for li in book_list.find_all("li", class_="pgdbetext"):
        link = li.find("a")
        if link:
            href = link["href"]
            if re.match(r"/ebooks/\d+", href) and li.text.endswith("(German) (as Author)"):
                books.append("https://www.gutenberg.org" + href)

    return books

if __name__ == "__main__":
    authors = [
        {"id": 586, "name": "Goethe"},
    ]
    # Verzeichnis german-work-urls erstellen, falls es nicht existiert
    dir_path = Path("german-work-urls")
    dir_path.mkdir(parents=True, exist_ok=True)

    for author in authors:
        books = fetch_books_by_author_id(author["id"])
        print(f"Es wurden {len(books)} Werke von {author['name']} gefunden.")

        if books and len(books) > 0:
            output_path = dir_path / f"{author['name']}-ebooks.txt"
            with output_path.open("w", encoding="utf-8") as file:
                for book in books:
                    file.write(book + "\n")
            print(f"Die URLs der Werke wurden in die Datei {author['name']}-ebooks.txt gespeichert.")