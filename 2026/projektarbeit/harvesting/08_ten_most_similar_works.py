import os
import requests
from bs4 import BeautifulSoup
from nltk.stem import SnowballStemmer

def compute_terms_per_work(input_dir, stemmer=None):
    """
    Berechnet die Menge der Terme in einem Werk, indem die Tokens aus der ".tokens"-Datei gelesen und optional gestemmt werden.
    Die berechneten Terme werden in einer neuen Datei "{workID}-terms.txt" im jeweiligen Autorenverzeichnis gespeichert. Hierbei erfolgt die Ausgabe der Terme in lexikographischer Reihenfolge. 

    Parameter:
    - input_dir (str): Der Pfad zum Hauptverzeichnis, das die Unterverzeichnisse der Werke enthält.
    - stemmer (SnowballStemmer): Der Stemmer, der verwendet werden soll (Standard: None, wenn kein Stemming gewünscht ist).
    """
    # Suche in Werkverzeichnissen nach Textdateien mit der Endung ".tokens"
    for author_dir in os.listdir(input_dir):
        author_path = os.path.join(input_dir, author_dir)
        if os.path.isdir(author_path):
            terms = set()
            # alle Tokens in einer Menge sammeln, so dass jedes Token nur einmal betrachtet wird
            for filename in os.listdir(author_path):
                if filename.endswith(".tokens"):
                    file_path = os.path.join(author_path, filename)
                    with open(file_path, "r", encoding="utf-8") as f:
                        for token in f:
                            if stemmer:
                                token = stemmer.stem(token.strip())
                            else:
                                token = token.strip()
                            if token:
                                terms.add(token)
                    workID = filename.replace(".tokens", "")
                    with open(os.path.join(author_path, f"{workID}-terms.txt"), "w", encoding="utf-8") as f:
                        for term in sorted(terms):
                            f.write(term + "\n")

def compute_similarity(terms_A, terms_B, mode="jaccard"):
    """
    Berechnet die Ähnlichkeit zwischen zwei Autoren basierend auf den zugehörigen Term-Mengen ihrer Werke.

    Parameter:
    - terms_A: Menge der Terme des ersten Autors
    - terms_B: Menge der Terme des zweiten Autors
    - mode: Modus der Ähnlichkeitsberechnung ("jaccard", "dice", "otsuka-ochiai")
    """
    intersection = terms_A & terms_B # Schnittmenge der Term-Mengen beider Autoren
    if mode == "jaccard":
        union = terms_A | terms_B # Vereinigungsmenge der Term-Mengen beider Autoren
        similarity = len(intersection) / len(union) if union else 0
    elif mode == "dice":
        # bietet sich an, wenn die beiden Term-Mengen sehr unterschiedlich groß sind (Normierung der Größe der
        # Schnittmenge durch das arithmetische Mittel der Größen der beiden Term-Mengen)
        len_arithmetic_mean = 0.5 * (len(terms_A) + len(terms_B))
        similarity = len(intersection) / len_arithmetic_mean if len_arithmetic_mean > 0 else 0
    elif mode == "otsuka-ochiai":
        # bietet sich an, wenn die beiden Term-Mengen sehr unterschiedlich groß sind (Normierung der Größe der
        # Schnittmenge durch das geometrische Mittel der Größen der beiden Term-Mengen)
        len_geom_mean = (len(terms_A) * len(terms_B)) ** 0.5
        similarity = len(intersection) / len_geom_mean if len_geom_mean > 0 else 0
    else:
        similarity = 0

    return similarity

def fetch_work_title_by_work_id(work_id) -> int:
    """
    Gibt den Titel eines Werkes mit der angegebenen ID zurück.

    Parameter:
    - work_id (int): Die ID des Werkes, für das der Titel abgerufen werden soll.
    """

    url = "https://www.gutenberg.org/ebooks/" + str(work_id)

    # HTML-Seite abrufen
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Seite: {response.status_code}")
        return []

    # HTML-Seite parsen
    soup = BeautifulSoup(response.text, "html.parser")

    # Abschnitt mit h2-Überschrift des Autorennamens in der HTML-Seite finden
    meta_title = soup.find("meta", {"name": "title"})
    if meta_title:
        title = meta_title.get("content") 
    else:
        title = "Titel nicht gefunden"
        
    return title

if __name__ == "__main__":
    
    input_dir = "german-works"
    compute_terms_per_work_switch = False

    if compute_terms_per_work_switch:
        stemmer = SnowballStemmer("german") 

        print("Berechne Terme pro Werk...")
        compute_terms_per_work(input_dir, stemmer)
        print("Berechnung der Terme pro Werk abgeschlossen.")


    mode = "jaccard"
    print(f"{mode}-Ähnlichkeitswerte zwischen den Werken berechnen...")

    if not os.path.exists(f"work-similarity_{mode}.csv"):
    
        print("Erstelle File-Liste der Terms-Dateien der Werke...")    
        # Zusammenstellen der file_list mit den terms-Dateien der Werke
        file_list = []
        for author_dir in os.listdir(input_dir):
            author_path = os.path.join(input_dir, author_dir)
            if os.path.isdir(author_path):
                for filename in os.listdir(author_path):
                        if filename.endswith("-terms.txt"):
                            file_list.append(os.path.join(author_path, filename))
        print("File-Liste der Terms-Dateien der Werke erstellt.")

        print("Berechne Ähnlichkeiten zwischen den Werken...")

        similarity_matrix = {}
        for i, work_A in enumerate(file_list):
            terms_A = set()
            with open(work_A, "r", encoding="utf-8") as f:
                for line in f:
                    terms_A.add(line.strip())
            for work_B in file_list[i + 1:]:
                terms_B = set()
                with open(work_B, "r", encoding="utf-8") as f:
                    for line in f:
                        terms_B.add(line.strip())
                similarity = compute_similarity(terms_A, terms_B, mode=mode)
                similarity_matrix[(work_A.split("-terms")[0], work_B.split("-terms")[0])] = similarity
        print("Berechnung der Ähnlichkeiten zwischen den Werken abgeschlossen.")

        # Sichern der Ähnlichkeitswerte zwischen den Werken als CSV-Datei
        print(f"Speichere die Ähnlichkeitswerte zwischen den Werken in work-similarity_{mode}.csv...")
        with open(f"work-similarity_{mode}.csv", "w", encoding="utf-8") as csv_file:
            for (work_A, work_B), similarity in similarity_matrix.items():

                label_work_A = "-".join(work_A.split(os.path.sep)[-2:]).split("-terms")[0]
                label_work_B = "-".join(work_B.split(os.path.sep)[-2:]).split("-terms")[0]

                csv_file.write(f"{label_work_A},{label_work_B},{similarity:.4f}\n")

        print(f"Ähnlichkeitswerte zwischen den Werken in work-similarity_{mode}.csv gesichert.")

    else:
        print(f"Die Datei work-similarity_{mode}.csv existiert bereits.")
        
    
    print("Top 10-Ähnlichkeitswerte ermitteln und sichern...")

    if not os.path.exists(f"top-10-work-similarity_{mode}.csv"):
        print(f"Erstelle die Datei top-10-work-similarity_{mode}.csv aus work-similarity_{mode}.csv...")

        similarity_matrix = {}
        with open(f"work-similarity_{mode}.csv", "r", encoding="utf-8") as csv_file:
            for line in csv_file:
                work_A, work_B, similarity = line.strip().split(",")
                similarity_matrix[(work_A, work_B)] = float(similarity)
        sorted_similarities = sorted(similarity_matrix.items(), key=lambda x: x[1], reverse=True)

        head_10_similarities = sorted_similarities[:10]
    
        with open(f"top-10-work-similarity_{mode}.csv", "w", encoding="utf-8") as csv_file:
            for (work_A, work_B), similarity in head_10_similarities:

                csv_file.write(f"{work_A},{work_B},{similarity:.4f}\n")
        print("Top-10-Ähnlichkeitswerte zwischen den Werken als csv-Datei gesichert.")

    else:
        print(f"Die Datei top-10-work-similarity_{mode}.csv existiert bereits.")

    
    print("Ausgabe der Top-10-Ähnlichkeitswerte (Titel, Autoren und Ähnlichkeitswert):\n")
    with open(f"top-10-work-similarity_{mode}.csv", "r", encoding="utf-8") as csv_file:
        for line in csv_file:
            work_A, work_B, similarity = line.strip().split(",")
            
            work_A_id = work_A.split("-")[-1]
            work_B_id = work_B.split("-")[-1]

            title_A = fetch_work_title_by_work_id(work_A_id)
            title_B = fetch_work_title_by_work_id(work_B_id)

            print(f"{title_A} (ID: {work_A_id}) - {title_B} (ID: {work_B_id}): Ähnlichkeit = {similarity}")