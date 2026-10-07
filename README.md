````markdown
# DEVI STUDIARE

Screensaver fullscreen in Python/Pygame ispirato all'estetica dello spazio cinematografico e all'atmosfera di **2001: Odissea nello spazio**.

Il programma mostra un campo stellare animato in prospettiva, accelera progressivamente in un effetto **warp**, quindi rallenta e fa comparire al centro la scritta:

> DEVI STUDIARE

La scritta è volutamente **nitida**, senza il forte effetto glow delle versioni precedenti.

## Caratteristiche

- Fullscreen automatico
- Campo stellare 3D simulato con prospettiva
- Accelerazione e decelerazione delle stelle
- Scie delle stelle durante il warp
- Leggera illuminazione centrale
- Scritta centrale nitida e leggibile
- Fade-in iniziale
- Audio in loop
- Supporto per:
  - `soundtrack.ogg`
  - `soundtrack.wav`
  - `soundtrack.mp3`
  - `soundtrack.mid`
  - `soundtrack.midi`
- Uscita con:
  - `ESC`
  - qualsiasi tasto
  - click del mouse
  - movimento significativo del mouse

## Requisiti

- Windows
- Python 3.x
- Pygame
- PyInstaller per creare l'EXE

Installazione di Pygame:

```bash
pip install pygame
````

Installazione di PyInstaller:

```bash
pip install pyinstaller
```

## Struttura del progetto

Una struttura consigliata è:

```text
DeviStudiare/
├── devi_studiare.py
├── soundtrack.ogg
├── README.md
└── requirements.txt
```

Per `requirements.txt`:

```text
pygame
pyinstaller
```

## Avvio da Python

Con `soundtrack.ogg` nella stessa cartella:

```bash
python devi_studiare.py
```

## Creazione dell'EXE

Per creare un singolo eseguibile Windows con la musica incorporata:

```bash
python -m PyInstaller --clean --onefile --noconsole --name=DeviStudiare --add-data "soundtrack.ogg;." devi_studiare.py
```

L'eseguibile verrà creato in:

```text
dist/DeviStudiare.exe
```

La modalità `--onefile` crea un singolo EXE. La risorsa audio viene inclusa nel bundle tramite `--add-data`.

## Audio

### OGG consigliato

Il formato consigliato è:

```text
soundtrack.ogg
```

È il formato da preferire per questa applicazione.

Il programma cerca automaticamente la musica in questa priorità:

```text
soundtrack.ogg
soundtrack.wav
soundtrack.mp3
soundtrack.mid
soundtrack.midi
```

Quando viene creato l'EXE con PyInstaller, il programma cerca la risorsa sia nel bundle temporaneo sia nella directory dell'eseguibile.

### MIDI

I file MIDI vengono gestiti separatamente su Windows tramite il sistema MIDI di Windows.

Per la massima affidabilità, **OGG è comunque consigliato**.

## Personalizzazione

I principali parametri si trovano all'inizio di `devi_studiare.py`.

### Numero di stelle

```python
NUM_STARS = 900
```

Aumentando il valore:

* aumenta la densità delle stelle
* aumenta il carico grafico

### Velocità normale

```python
BASE_SPEED = 0.10
```

### Velocità massima del warp

```python
WARP_MAX = 5.8
```

### Comparsa della scritta

```python
T_TEXT = 16.0
```

La scritta inizia a comparire dopo 16 secondi.

### Durata del fade della scritta

```python
T_TEXT_FADE = 2.0
```

## Timeline

La sequenza predefinita è:

```text
0s    Fade-in
2s    Inizio accelerazione
10s   Velocità massima
16s   Inizio comparsa della scritta
18s   Inizio rallentamento
28s   Fine rallentamento
```

I valori possono essere modificati direttamente nel file Python.

## Prestazioni

Il programma usa Pygame e disegna tutte le stelle in tempo reale.

Se l'animazione è poco fluida, prova a ridurre:

```python
NUM_STARS = 700
```

oppure:

```python
NUM_STARS = 500
```

Se invece il PC gestisce bene l'effetto, puoi aumentare il numero di stelle.

## Controlli

Durante l'esecuzione:

```text
ESC                    -> esci
Qualsiasi tasto        -> esci
Click                  -> esci
Movimento del mouse    -> esci
```

Il movimento del mouse viene ignorato per il primo secondo, così lo screensaver non si chiude immediatamente all'avvio.

## Build pulita

Per ricreare l'EXE da zero:

```bat
rmdir /s /q build
rmdir /s /q dist
del DeviStudiare.spec
```

Poi:

```bash
python -m PyInstaller --clean --onefile --noconsole --name=DeviStudiare --add-data "soundtrack.ogg;." devi_studiare.py
```

## Licenza

Questo progetto può essere utilizzato e modificato liberamente, salvo eventuali diritti relativi ai file audio o ad altri asset aggiunti al progetto.

Il nome e i riferimenti a **2001: Odissea nello spazio** vengono utilizzati come riferimento estetico del progetto; il progetto non è affiliato con i titolari dei relativi diritti.

## Note

Il progetto è pensato principalmente come screensaver/visualizzatore fullscreen personale.

Per distribuire l'applicazione a terzi, assicurati di avere i diritti necessari sulla musica utilizzata in `soundtrack.ogg`, `soundtrack.wav`, `soundtrack.mp3` o nei file MIDI.

```

Non sono riuscito a generare il file `.md` scaricabile perché lo strumento per la creazione del file non è disponibile in questo momento.
```
