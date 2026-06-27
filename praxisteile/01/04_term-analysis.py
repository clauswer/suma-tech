def count_term_frequencies(input_file):
    """
    Liest eine Datei mit einem Token pro Zeile und bestimmt daraus die Häufigkeit der einzelnen Terme.
    Auf Basis der Häufigkeitswerte werden schließlich die häufigsten und seltensten Terme im Text ausgegeben.

    Parameter:
    - input_file (str): Der Pfad zur Datei mit den Tokens.

    Rückgabe:
    - dict: Ein Dictionary mit den Termen und ihren zugehörigen Häufigkeitswerten.
    """
    # Dictionary zur Zählung der Termhäufigkeiten
    term_frequencies = {}

    with open(input_file, "r", encoding="utf-8") as infile:
        # Datei zeilenweise einlesen
        tokens = infile.read().splitlines()

    # Häufigkeiten bestimmen
    for token in tokens:
        if token in term_frequencies:
            # token erstmalig gefunden, daher Zähler auf 1 setzen
            term_frequencies[token] += 1
        else:
            # token erneut gefunden, daher vorhandenen Zähler um 1 erhöhen
            term_frequencies[token] = 1

    # Sortieren der Terme nach ihrer Häufigkeit
    sorted_terms = sorted(term_frequencies.items(), key=lambda item: item[1])

    # Ausgabe der 10 seltensten Terme
    print("\n10 seltenste Terme:")
    for term, count in sorted_terms[:10]: # Ausgabe der ersten 10 Elemente der sortierten Liste (seltenste Terme)
        print(f"{term} ({count})")

    # Ausgabe der 10 häufigsten Terme
    print("\n10 häufigste Terme:")
    for term, count in sorted_terms[-10:]: # Ausgabe der letzten 10 Elemente der sortierten Liste (häufigste Terme)
        print(f"{term} ({count})")

    return term_frequencies

if __name__ == "__main__":
    input_file = "21000_tokens.txt"
    term_frequencies = count_term_frequencies(input_file)
