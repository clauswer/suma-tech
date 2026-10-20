import requests
from bs4 import BeautifulSoup
import re

def fetch_birth_year_by_author_id(author_id) -> int:
    """
    Gibt das Geburtsjahr des Autors mit der angegebenen ID zurück.

    Parameter:
    - author_id (int): Die ID des Autors, für den das Geburtsjahr abgerufen werden soll.
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
    
    # Alle a-Tags innerhalb des h2-Elements finden
    a_tags = author_section.find_all("a")
    
    if a_tags:
        # der 2. a-Tag enthält den Autorennamen und das Geburtsjahr
        try:
            a_tag = a_tags[1]
            # Den Text des a-Tags extrahieren
            author_text = a_tag.get_text(strip=True)
            
            # Mit regulärem Ausdruck nach dem Geburtsjahr suchen (4 aufeinanderfolgende Ziffern)
            match = re.search(r'\b(\d{4})\b', author_text)
            if match:
                return int(match.group(1))
            else:
                return None

        except IndexError:
            return None 
        
    return None


if __name__ == "__main__":
    authors = [
        {"id": 586, "name": "Goethe"},
        {"id": 289, "name": "Schiller"},
        {"id": 1049, "name": "Heine"},
        {"id": 35073, "name": "Mann"},
        {"id": 1735, "name": "Kafka"},
        {"id": 941, "name": "Hesse"},
        {"id": 1426, "name": "Kant"},
        {"id": 1995, "name": "Humboldt"},
        {"id": 1765, "name": "Fontane"},
        {"id": 846, "name": "Rilke"},
    ]

    for author in authors:
        birth_year = fetch_birth_year_by_author_id(author["id"])
        if birth_year:
            print(f"{author['name']}: {birth_year}")
        else:
            print(f"Geburtsjahr für {author['name']} nicht gefunden.")