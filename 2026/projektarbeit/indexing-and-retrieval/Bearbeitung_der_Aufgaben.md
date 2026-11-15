**Aufgabe 3: eBooks ohne gültige Start- und End-Marker**

Die eBooks mit den IDs
43932
43987
36779
31660
43931
enthalten keine Start- und End-Marker, da statt der Texte eine XML-Datei mit Erläuterungen zur Lizenzlage des Werkes in Deutschland heruntergeladen wurden.

**Bonusaufgabe: Welche Parameter haben den geringsten bzw. größten Einfluss auf die Qualität der zurückgelieferten E-Books?**

Die Parameter `minwl` und `boost` haben die größten Einflüsse auf die zurückgelieferten Ergebnisse: mit `boost=true` wird die relevance der interesting terms berücksichtigt. Durch einen höhren `minwl`-Wert werden interesting terms unter einer bestimmten Wortlänge ignoriert.  