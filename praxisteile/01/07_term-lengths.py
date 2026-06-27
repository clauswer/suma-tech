def compute_term_lengths(input_file):
    """
    Berechnet die minimale, maximale und durchschnittliche Länge der Terme in der übergebenen Datei.
    """
    with open(input_file, "r", encoding="utf-8") as infile:
        # Datei zeilenweise einlesen
        tokens = infile.read().splitlines()

    # Termlängen bestimmen
    min_length = None
    min_length_tokens = []

    max_length = None
    max_length_tokens = []

    sum_of_lengths = 0

    # über alle Tokens iterieren, wobei jedes Token nur einmal betrachtet werden muss
    for token in set(tokens):
        length = len(token)
        sum_of_lengths += length
        if min_length is None or length < min_length:
            # neue minimale Termlänge gefunden
            min_length = length
            min_length_tokens = [token]
        elif length == min_length:
            # neues Token mit aktueller minimaler Länge gefunden
            min_length_tokens.append(token)
        if max_length is None or length > max_length:
            # neue maximale Termlänge gefunden
            max_length = length
            max_length_tokens = [token]
        elif length == max_length:
            # neues Token mit aktueller maximaler Länge gefunden
            max_length_tokens.append(token)

    print(f"Durchschnittliche Termlänge: {round(sum_of_lengths / len(set(tokens)), 1)}")

    print(f"\n{len(min_length_tokens)} Terme mit minimaler Länge {min_length}:")
    for token in min_length_tokens:
        print(token)

    print(f"\n{len(max_length_tokens)} Terme mit maximaler Länge {max_length}:")
    for token in max_length_tokens:
        print(token)

if __name__ == "__main__":
    input_file = "21000_tokens.txt"
    compute_term_lengths(input_file)
