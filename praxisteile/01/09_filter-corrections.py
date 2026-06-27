import re

def remove_corrections_from_tokens(input_file, output_file):
    """
    Entfernt Korrekturen (in eckigen Klammern) am Ende von Tokens, die zeilenweise aus der Eingabedatei
    eingelesen werden und speichert die bereinigten Tokens in der Ausgabedatei.

    Parameter:
    - input_file (str): Pfad zur Eingabedatei, die die Tokens enthält.
    - output_file (str): Pfad zur Ausgabedatei, in die die bereinigten Tokens geschrieben werden.
    """
    with open(input_file, "r", encoding="utf-8") as infile:
        tokens = infile.readlines() # Tokens aus der Datei lesen

    with open(output_file, "w", encoding="utf-8") as outfile:
        for token in tokens:
            token = token.strip() # führende und nachfolgende Whitespaces entfernen
            # mögliche Korrektur am Ende eines Tokens entfernen
            token_cleaned = re.sub(r"\[[^\[\]]+\]$", "", token)
            if token_cleaned != token:
                print(f"Korrektur am Tokenende entfernt: {token} -> {token_cleaned}")
                token = token_cleaned
            outfile.write(token + "\n")

    num_of_tokens = len(tokens)
    print(f"Es wurden {num_of_tokens} Tokens in der Datei {output_file} gespeichert.")

if __name__ == "__main__":
    input_file = "21000_tokens.txt"
    output_file = "21000_tokens-wo-corrections.txt"
    remove_corrections_from_tokens(input_file, output_file)