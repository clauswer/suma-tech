import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from ten_most_similar_works import fetch_work_title_by_work_id

def filter_work_csv(work_set:set, csv_file:str = "work-similarity_jaccard.csv") -> pd.DataFrame:
    """
    Filtert aus einer CSV-Datei mit Ähnlichkeiten zwischen Werken alle Ähnlichkeiten heraus, die ausschließlich die Werke aus der angegebenen Menge enthalten.

    Das Ergebnis wird als pandas DataFrame zurückgegeben.

    Args:
        work_set (set): Eine Menge von mind. 2 Werken, nach denen gefiltert werden sollen.
        csv_file (str): Der Pfad zur CSV-Datei, die die Ähnlichkeiten zwischen den Werken enthält.

    Returns:
        pd.DataFrame: Ein DataFrame mit den Ähnlichkeitswerten zwischen den Werken.
    """

    df = pd.read_csv(csv_file, names=["Work A", "Work B", "Similarity"])

    return df[df["Work A"].isin(work_set) & df["Work B"].isin(work_set)]


def get_works_from_similarity_csv(csv_file:str = "top-10-work-similarity_jaccard.csv") -> set:
    """
    Liest aus einer CSV-Datei mit Ähnlichkeiten zwischen Werken alle Werke heraus, die in der Datei vorkommen.

    Das Ergebnis wird als Menge zurückgegeben.

    Args:
        csv_file (str): Der Pfad zur CSV-Datei, die die Ähnlichkeiten zwischen den Werken enthält.

    Returns:
        set: Eine Menge von Werken, die in der CSV-Datei vorkommen.
    """

    df = pd.read_csv(csv_file, names=["Work A", "Work B", "Similarity"])

    return set(df["Work A"]).union(set(df["Work B"]))


def change_author_work_id_to_label(author_work:str) -> str:
    """
    Ändert die Angabe Autor-WorkID eines Werks in ein Label um, das aus dem Autorennamen und dem Werktitel besteht.

    Args:
        author_work (str): Die Angabe Autor-WorkID des Werks, die geändert werden soll (Bsp.: 1883-Kafka-16304).

    Returns:
        str: Das Label des Werks im Format "Autor - Titel".
    """

    workID = author_work.split("-")[-1]
    
    return fetch_work_title_by_work_id(workID)
    
def build_matrix(df: pd.DataFrame) -> pd.DataFrame:
    df = df[["Work A", "Work B", "Similarity"]].copy()

    matrix = df.pivot_table(
        index="Work A",
        columns="Work B",
        values="Similarity",
        aggfunc="mean",
    )

    matrix = matrix.combine_first(matrix.T)
    all_ids = sorted(set(matrix.index) | set(matrix.columns))
    matrix = matrix.reindex(index=all_ids, columns=all_ids)
    for i in range(len(matrix)):
        matrix.iat[i, i] = 1.0
    return matrix.fillna(0.0)

def draw_heatmap(matrix: pd.DataFrame, output: str) -> None:
    n = len(matrix)
    cell = max(0.55, min(1.1, 11 / max(1, n)))
    plt.figure(figsize=(n * cell + 2.5, n * cell + 1.8))

    sns.heatmap(
        matrix,
        cmap="OrRd",
        vmin=0.0,
        vmax=1.0,
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        linecolor="white",
        square=True,
        cbar_kws={"label": "Ähnlichkeit", "shrink": 0.8},
    )

    plt.title("Ähnlichkeitsmatrix der Werke", fontsize=12, pad=12)
    plt.xticks(rotation=60, ha="right")
    plt.yticks(rotation=0)
    plt.xlabel("")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    works_file = "top-10-work-similarity_jaccard.csv"
    works_set = get_works_from_similarity_csv(works_file)

    print(f"Die Datei {works_file} enthält {len(works_set)} Werke.")

    similarity_file = "work-similarity_jaccard.csv"
    df = filter_work_csv(works_set, similarity_file)
    print(f"In der Ähnlichkeits-Tabelle Die Datei {similarity_file} wurden {len(df)} Einträge zu den Ähnlichkeiten zwischen den Werken in {works_file} gefunden.")

    # Ändern der Spalten "Work A" und "Work B" in Labels
    df["Work A"] = df["Work A"].apply(change_author_work_id_to_label)
    df["Work B"] = df["Work B"].apply(change_author_work_id_to_label)

    matrix = build_matrix(df)
    heatmap_file = "top10-work-similarity_jaccard.png"
    draw_heatmap(matrix, heatmap_file)
    print(f"Heatmap erstellt: {heatmap_file}")

