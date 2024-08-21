# Setup I2C OLED 128x64px on Headless Pi5 Bookworm

Questa guida ti mostrerà come configurare un display OLED I2C 128x64px su un Raspberry Pi 5 che esegue Bookworm (64bit) senza interfaccia grafica (headless).

## Requisiti

- Raspberry Pi 5 con Bookworm 64bit installato
- Accesso SSH al Raspberry Pi
- Display OLED 128x64px con connessione I2C

## Collegamento del Display OLED al Raspberry Pi

Segui il diagramma sottostante per collegare correttamente il display OLED al Raspberry Pi 5:

![OLED Connection Diagram](https://github.com/user-attachments/assets/fd5db9fe-6da0-4e04-9189-fa6d7e5208a9)


Connessione PIN:

- VCC = Pin 1
- SDA = Pin 3
- SCL = Pin 5
- GND = Pin 9

## Passaggi

### 1. Installazione di Bookworm 64bit

Assicurati di avere Bookworm 64bit installato sul tuo Raspberry Pi 5.

### 2. Connessione SSH al Raspberry Pi

Utilizza il terminale per accedere al tuo Raspberry Pi tramite SSH. Se ricevi l'errore "WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!", esegui i seguenti comandi:

```bash
nano ~/.ssh/known_hosts
```
- Premi `Ctrl+K` per rimuovere tutte le voci relative al Raspberry Pi.
- Premi `Ctrl+X` per uscire, poi `Y` per salvare e `Enter` per confermare.

Ora puoi connetterti di nuovo tramite SSH.

### 3. Configurazione dell'I2C

Nel terminale, esegui:

```bash
sudo raspi-config
```
- Vai su "3. Interface Options" > `I4 I2C` > `Yes` > `Ok`
- Seleziona `Finish`

### 4. Aggiornamento del sistema e installazione di pacchetti necessari

Esegui i seguenti comandi per aggiornare il sistema e installare Python e pip:

```bash
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install python3-pip python3-venv git
sudo apt install --upgrade python3-setuptools
```

### 5. Configurazione dell'ambiente virtuale

Creazione di un ambiente virtuale chiamato `oled_env`:

```bash
python3 -m venv oled_env --system-site-packages
```

Attiva l'ambiente virtuale:

```bash
source oled_env/bin/activate
```

Dovresti vedere `(oled_env)` all'inizio della riga del terminale.

### 6. Installazione dei pacchetti per l'OLED

Mentre sei nell'ambiente virtuale, esegui i seguenti comandi:

```bash
cd ~
pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo -E env PATH=$PATH python3 raspi-blinka.py
```

Quando il processo è completato, premi `Y` per riavviare il Raspberry Pi.

### 7. Test del Display OLED

Dopo il riavvio, riconnettiti tramite SSH e verifica che l'OLED sia rilevato correttamente:

```bash
i2cdetect -y 1
```

Dovresti vedere una griglia con `3c` tra le righe, confermando che l'OLED è collegato correttamente.

### 8. Installazione di `OLED_Stats`

Esci dall'ambiente virtuale:

```bash
deactivate
```

Installa `git` e clona la repository necessaria:

```bash
cd ~
git clone https://github.com/RUDEWORLD/OLED_Stats.git
```

Rientra nell'ambiente virtuale, accedi alla directory del progetto e avvia lo script:

```bash
cd ~
source oled_env/bin/activate
cd OLED_Stats
python3 stats.py
```

A questo punto, il tuo OLED dovrebbe accendersi. Tuttavia, il display si spegnerà al riavvio poiché il programma viene eseguito in un ambiente virtuale. Per risolvere questo problema, procederemo a creare un file eseguibile.

### 9. Creazione di un file eseguibile per l'avvio automatico

Scarica il file di attivazione dalla repository e rendilo eseguibile:

```bash
cd ~
curl -OL https://raw.githubusercontent.com/minerale00/PI5OLED/main/OLED_ACTIVATE
sudo chmod +x /home/yourusername/OLED_ACTIVATE
```

Modifica il crontab per eseguire il file al riavvio:

```bash
crontab -e
```

Se è la prima volta che apri crontab, seleziona `1` e premi `Enter`. Aggiungi la seguente riga in fondo al file, sostituendo "pi" con il tuo nome utente se necessario:

```bash
@reboot /home/pi/OLED_ACTIVATE &
```

Salva e chiudi il crontab (Ctrl+X, Y, Enter).

### 10. Riavvia il Raspberry Pi

Riavvia il Raspberry Pi per vedere il display OLED accendersi automaticamente.

```bash
sudo reboot
```

## Repository Correlata

I file necessari per il setup, inclusi gli script, possono essere trovati nella repository [Pi5OLED](https://github.com/RUDEWORLD/Pi5OLED).
