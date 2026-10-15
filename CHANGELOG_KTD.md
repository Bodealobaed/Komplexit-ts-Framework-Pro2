# Gezielte Korrekturen

- Ressourcen & Kosten: Eingabebereich von `st.form` auf reaktiven `st.container` umgestellt. Die Checkboxen aktivieren die abhängigen Zahlenfelder nun unmittelbar nach dem Klick.
- Die vorhandenen Validierungsregeln und Berechnungsfunktionen in `engine.py` wurden nicht verändert.
- KTD-Logo als Bild im Seitenbereich ergänzt.
- Unkommentiertes Sternchen im M1-Ergebnis `CI / QR*` entfernt (`CI / QR`). Die fachliche Interpretation der Kennzahl bleibt gesondert zu prüfen.
- Kostenanzeige behandelt `0.00` ausdrücklich als gültigen Wert, statt ihn als fehlenden Wert zu formatieren.
- Zwei zusätzliche Regressionstests ergänzt.

**Hinweis:** Die Profilnamen und Fachbegriffe wurden nicht pauschal großgeschrieben: Adjektive werden im Deutschen auch in wissenschaftlichen Tabellen normalerweise kleingeschrieben. Wissenschaftliche Originalformeln wurden nicht ergänzt oder verändert.
