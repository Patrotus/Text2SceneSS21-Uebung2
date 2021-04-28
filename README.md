Um die Anwendung auszuführen muss zunächst ein neues Conda-Enviroment angelegt werden mit `conda env create -name <name> -f t2s_uebung.yml`
Anschließend muss dieses mit `activate <name>` aktiviert werden.  
U.U. kann das Paket `en-core-web-sm` nicht gefunden werden, bzw. es fehlt. Dann muss dieses mit `python -m spacy download en_core_web_sm` manuell installiert werden.

Um das Programm laufen zu lassen, genügt es die `run.py`-Datei mit `python run.py` auszuführen.