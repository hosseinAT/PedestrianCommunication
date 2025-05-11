# Fußgängerkommunikation für autonome Fahrzeuge

Dieses Projekt zielt darauf ab, eine effektive Kommunikation zwischen autonomen Fahrzeugen und Fußgängern mithilfe visueller Signale, insbesondere animierter Augenanzeigen, zu ermöglichen. Durch die Erkennung von Fußgängern mit einer Intel RealSense D456C-Kamera und der Anzeige dynamischer Augenanimationen sorgt das System dafür, dass sich Fußgänger beim Überqueren der Straße in der Nähe autonomer Fahrzeuge sicher und wahrgenommen fühlen.

Das System erkennt bis zu vier Fußgänger, verfolgt deren Position mithilfe eines YOLOv8-Modells und eines Kalman-Filters und zeigt grüne oder rote Augensignale an, um anzuzeigen, ob das Überqueren sicher ist. Die animierten Augen bewegen sich dynamisch auf den nächsten Fußgänger zu und ahmen damit eine menschliche Interaktion nach.

---

## Inhaltsverzeichnis

* [Funktionen](#funktionen)
* [Projektstruktur](#projektstruktur)
* [Hardwareanforderungen](#hardwareanforderungen)
* [Softwareanforderungen](#softwareanforderungen)
* [Installation](#installation)
* [Verwendung](#verwendung)

---

## Funktionen

* **Fußgängererkennung**: Verwendet die Intel RealSense D456C-Kamera und YOLOv8 zur Erkennung und Verfolgung von bis zu vier Fußgängern.
* **Dynamische Augenanimation**: Zeigt animierte Augen, die sich dem nächsten Fußgänger zuwenden; mit grünem (sicher) oder rotem (nicht sicher) Signal.
* **Echtzeitverarbeitung**: Verarbeitet Farb- und Tiefenbilder in Echtzeit für präzises Tracking.
* **Kalman-Filter-Tracking**: Robuste Verfolgung der Fußgänger mithilfe eines Kalman-Filters.
* **Konfigurierbare Einstellungen**: Anpassung von Kameraauflösung, Erkennungsgenauigkeit und Anzeigeparametern über eine YAML-Konfigurationsdatei.

---

## Projektstruktur

```

PedestrianCommunication/
├── src/
│   ├── camera/
│   │   └── realsense\_camera.py       # Steuerung der Intel RealSense Kamera
│   ├── detection/
│   │   └── pedestrian\_detector.py    # Fußgängererkennung mit YOLOv8
│   ├── display/
│   │   └── eye\_animation.py          # Verwaltung der Augenanimation
│   ├── tracker/
│   │   ├── kalman\_filter.py          # Kalman-Filter zur Verfolgung
│   │   └── sort.py                   # SORT-Algorithmus zur Mehrfachverfolgung
│   ├── utils/
│   │   ├── coordinate\_utils.py       # Koordinatentransformation für Animation
│   │   └── logger.py                 # Protokollierungskonfiguration
│   ├── config/
│   │   └── settings.yaml             # Konfiguration für Kamera, Erkennung, Anzeige
│   ├── main.py                       # Hauptskript zum Starten des Systems
│   └── yolov8n.pt                    # Vorgefertigtes YOLOv8-Modell
├── output/                           # Ausgabeordner (z. B. Logs)
├── docs/                             # Dokumentation
├── test/                             # Testscripte (optional)
├── requirements.txt                  # Python-Abhängigkeiten
└── pedestrian\_communication.log      # Logdatei für Debugging

````

---

## Hardwareanforderungen

* **Intel RealSense D456C Kamera**: Zum Erfassen von Farb- und Tiefenbildern.
* **Computer**:

  * CPU: Intel Core i5/i7 oder besser
  * GPU: NVIDIA-GPU empfohlen für YOLOv8
  * USB 3.0-Anschluss für Kamera
  * RAM: mindestens 8 GB (16 GB empfohlen)
  * Betriebssystem: Ubuntu 20.04 (empfohlen) oder Windows 10/11

---

## Softwareanforderungen

* **Intel RealSense SDK 2.0**: Zur Kamerasteuerung und Tiefenbildverarbeitung
* **Python 3.8+**

### Benötigte Python-Bibliotheken

* `pyrealsense2`: Interaktion mit RealSense-Kamera
* `opencv-python`: Bildverarbeitung und Anzeige
* `numpy`: Numerische Berechnungen
* `ultralytics`: YOLOv8-Framework
* `pyyaml`: Einlesen von YAML-Dateien
* `loguru`: Logging

---

## Installation

### Repository klonen

```bash
git clone https://github.com/<your-username>/PedestrianCommunication.git
cd PedestrianCommunication
````

### Intel RealSense SDK 2.0 installieren

**Ubuntu:**

```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key F6E65AC044F831AC80A06380C8B06676A6A9B1D0
echo "deb https://librealsense.intel.com/Debian/apt focal main" | sudo tee /etc/apt/sources.list.d/librealsense.list
sudo apt-get update
sudo apt-get install librealsense2-dkms librealsense2-utils librealsense2-dev
```

**Windows**:
Von der [Intel RealSense SDK-Website](https://www.intelrealsense.com/sdk-2/) herunterladen und installieren.

### Python-Abhängigkeiten installieren

```bash
pip install -r requirements.txt
pip install loguru==0.7.0 opencv-python==4.8.0 pyyaml==6.0
pip install --force-reinstall numpy==1.24.3 ultralytics==8.0.196
pip install pyrealsense2
```

### YOLOv8-Modell herunterladen

Die Datei `yolov8n.pt` befindet sich bereits im Verzeichnis `src/`.
Falls nicht vorhanden, bitte von [Ultralytics](https://github.com/ultralytics/ultralytics) herunterladen und dort ablegen.

### Kameraanschluss prüfen

Intel RealSense D456C per USB 3.0 anschließen und im **RealSense Viewer** testen.

---

## Verwendung

### Projektverzeichnis öffnen

```bash
cd PedestrianCommunication
```

### Hauptskript ausführen

```bash
python src/main.py
```

### Erwartete Ausgabe

* **Kamerafenster**: Zeigt Live-Feed mit erkannten Fußgängern (Bounding Boxes)
* **Augenfenster**: Animierte Augen werden grün bei Fußgängererkennung und richten sich auf den nächsten
* Ohne Fußgänger: Augen leuchten rot
* Mit `q` kann das Programm beendet werden

### Logs

Protokolle werden in `pedestrian_communication.log` gespeichert

---

## Konfiguration

Bearbeite die Datei `src/config/settings.yaml`:

```yaml
camera:
  resolution: [1280, 720]
  fps: 30
  depth_threshold: 2.0
detection:
  model: "yolov8n.pt"
  confidence: 0.5
display:
  window_size: [800, 600]
  eye_radius: 60
  pupil_radius: 20
  eye_color: [255, 255, 255]
  signal_green: [0, 255, 0]
  signal_red: [255, 0, 0]
```

> ✅ Auflösung für Geschwindigkeit anpassen
> ✅ Erkennungssicherheit justieren
> ✅ Anzeige visuell anpassen

---

## Mitwirken

Beiträge sind willkommen!

1. Repository forken
2. Feature-Branch erstellen:

   ```bash
   git checkout -b feature/dein-feature
   ```
3. Änderungen committen:

   ```bash
   git commit -m "Feature hinzugefügt"
   ```
4. Branch pushen:

   ```bash
   git push origin feature/dein-feature
   ```
5. Pull Request erstellen

> Bitte den Code-Stil des Projekts beachten und wenn möglich Tests hinzufügen.

---








Im Folgenden finden Sie die **README.md**-Datei auf Deutsch im Markdown-Format für Ihr Projekt zur Kommunikation zwischen autonomen Fahrzeugen und Fußgängern. Die Datei ist klar, prägnant und professionell gestaltet, um das Projektziel, die Installation, die Nutzung und technische Details für die GitHub-Community zu erklären. Diese Version ist so formatiert, dass sie den Markdown-Standards entspricht und direkt in GitHub verwendet werden kann.

---

# README.md

# Kommunikation zwischen autonomen Fahrzeugen und Fußgängern

Dieses Projekt implementiert ein System, das autonomen Fahrzeugen ermöglicht, mit Fußgängern über visuelle Anzeigen (animierte Augen) zu kommunizieren. Ziel ist es, das Sicherheitsgefühl von Fußgängern beim Überqueren der Straße in der Nähe autonomer Fahrzeuge zu erhöhen, indem Fußgänger erkannt und visuelle Signale wie bewegliche Augen oder grüne/rote Signale angezeigt werden.

## Funktionen

- **Fußgängererkennung**: Einsatz der Intel RealSense D456C Kamera und des YOLOv8-Modells zur Erkennung von bis zu 4 Fußgängern sowie Berechnung ihrer Position und Entfernung.
- **Visuelle Anzeige**: Animation von beweglichen Augen, die sich zum nächstgelegenen Fußgänger bewegen und mit grün (sicher) oder rot (Warnung) den Status anzeigen.
- **Fußgänger-Tracking**: Verwendung von Kalman-Filtern und dem SORT-Algorithmus für stabiles Tracking von Fußgängern über mehrere Frames hinweg.
- **Einfache Konfiguration**: Einstellungen über die Datei `settings.yaml` für Kamera, Erkennung und Anzeige.

## Technologien

- **Hardware**:
  - Intel RealSense D456C Kamera
  - Computer mit USB 3.0 und leistungsstarker CPU/GPU
- **Software**:
  - Python 3.8+
  - Intel RealSense SDK 2.0
  - Bibliotheken: `pyrealsense2`, `opencv-python`, `ultralytics`, `pygame`, `numpy`, `pyyaml`, `loguru`
- **Modell**: YOLOv8n für die Fußgängererkennung

## Voraussetzungen

### Hardware

- Intel RealSense D456C Kamera
- Computer mit USB 3.0 Port und Intel Core i5/i7 oder besser (vorzugsweise mit NVIDIA GPU für YOLOv8)
- Betriebssystem: Windows 10/11 oder Ubuntu 20.04

### Software

- Python 3.8 oder höher
- Intel RealSense SDK 2.0
- Python-Bibliotheken (siehe `requirements.txt`)

## Installation

1. **Repository klonen**:

   ```bash
   git clone https://github.com/<your-username>/PedestrianCommunication.git
   cd PedestrianCommunication
   ```

2. **Intel RealSense SDK installieren**:

   - Für Ubuntu:

     ```bash
     sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key F6E65AC044F831AC80A06380C8B194FD192FC2A6
     sudo add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo bionic main" -u
     sudo apt-get install librealsense2-dkms librealsense2-utils librealsense2-dev
     ```

   - Für Windows: Laden Sie das Installationsprogramm von der [Intel RealSense Webseite](https://www.intelrealsense.com/developers/) herunter und installieren Sie es.

3. **Python-Bibliotheken installieren**:

   ```bash
   pip install -r requirements.txt
   pip install loguru==0.7.0 opencv-python==4.'intens0 pyyaml==6.0 numpy==1.24.3 ultralytics==8.0.196 pyrealsense2 pygame
   ```

4. **YOLOv8-Modell herunterladen**:

   ```bash
   wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt -O src/yolov8n.pt
   ```

5. **Kamera anschließen**:

   - Schließen Sie die Intel RealSense D456C Kamera an einen USB 3.0 Port an.
   - Überprüfen Sie die Verbindung:

     ```bash
     rs-enumerate-devices
     ```

## Projektstruktur

```plaintext
PedestrianCommunication/
├── src/
│   ├── camera/
│   │   └── realsense_camera.py
│   ├── detection/
│   │   └── pedestrian_detector.py
│   ├── display/
│   │   └── eye_animation.py
│   ├── tracker/
│   │   ├── kalman_filter.py
│   │   └── sort.py
│   ├── utils/
│   │   ├── coordinate_utils.py
│   │   └── logger.py
│   ├── config/
│   │   └── settings.yaml
│   ├── main.py
│   └── yolov8n.pt
├── output/
├── docs/
├── test/
├── requirements.txt
└── pedestrian_communication.log
```

## Ausführung

1. Wechseln Sie in das Projektverzeichnis:

   ```bash
   cd PedestrianCommunication
   ```

2. Führen Sie das Hauptprogramm aus:

   ```bash
   python src/main.py
   ```

3. **Ausgabe**:

   - **Camera-Fenster**: Zeigt Kameraaufnahmen mit grünen Rahmen um Fußgänger und deren Entfernung (z. B. "Distance: 1.5m").
   - **Eyes-Fenster**: Animation von Augen, die sich zum nächstgelegenen Fußgänger bewegen und grün (Erkennung) oder rot (keine Erkennung) anzeigen.
   - Drücken Sie die Taste `q`, um das Programm zu beenden.

## Konfiguration

Bearbeiten Sie die Datei `settings.yaml` in `src/config`, um folgende Parameter anzupassen:

- `camera.resolution`: Kameraauflösung (z. B. `[1280, 720]`)
- `camera.depth_threshold`: Maximale Erkennungsentfernung (z. B. `2.0` Meter)
- `detection.confidence`: Konfidenzschwelle für YOLO (z. B. `0.5`)
- `display.window_size`: Größe des Animationsfensters für die Augen (z. B. `[800, 600]`)

## Fehlerbehebung

- **Kamerafehler**: Bei der Meldung "No RealSense camera found" überprüfen Sie den USB 3.0 Anschluss und die SDK-Installation.
- **Bibliotheksfehler**: Installieren Sie fehlende Bibliotheken erneut:

  ```bash
  pip install -r requirements.txt
  ```

- **YOLO-Modellfehler**: Stellen Sie sicher, dass die Datei `yolov8n.pt` im `src`-Verzeichnis vorhanden ist.
- Überprüfen Sie die Log-Datei `pedestrian_communication.log` für Debugging-Informationen.

## Weiterentwicklung

- **Verbesserte Erkennung**: Trainieren Sie das YOLOv8-Modell mit spezifischen Daten für städtische Umgebungen.
- **Erweiterte Animation**: Fügen Sie komplexere Augenbewegungen (z. B. Blinzeln) in `eye_animation.py` hinzu.
- **Erkennung mehrerer Fußgänger**: Erhöhen Sie die Anzahl erkannter Fußgänger in `pedestrian_detector.py`.

## Mitwirken

Um zum Projekt beizutragen:

1. Forken Sie das Repository.
2. Erstellen Sie einen neuen Branch für Ihre Änderungen:

   ```bash
   git checkout -b feature/your-feature
   ```

3. Committen Sie Ihre Änderungen und erstellen Sie einen Pull Request.

## Lizenz

Dieses Projekt ist unter der [MIT-Lizenz] veröffentlicht. Details finden Sie in der Datei `LICENSE`.

## Kontakt

Für Fragen oder Vorschläge kontaktieren Sie [Ihre E-Mail-Adresse] oder erstellen Sie ein Issue auf GitHub.

---

### Zusätzliche Hinweise:

- **Markdown-Format**: Die Datei ist im standardisierten Markdown-Format geschrieben, das von GitHub korrekt gerendert wird. Sie enthält Überschriften, Listen, Codeblöcke und Links für eine klare Struktur.
- **Lizenz**: Falls Sie eine spezifische Lizenz (z. B. MIT) verwenden möchten, fügen Sie eine `LICENSE`-Datei zum Projekt hinzu.
- **Repository-Link**: Ersetzen Sie `<your-username>` durch Ihren GitHub-Benutzernamen.
- **Bilder oder GIFs**: Um die README visuell ansprechender zu gestalten, können Sie Screenshots oder GIFs der Programmausgabe hinzufügen. Laden Sie diese in den `docs`-Ordner hoch und referenzieren Sie sie:

  ```markdown
  ![Kameraausgabe](docs/camera_output.png)
  ![Augenanimation](docs/eyes_animation.gif)
  ```

### Nächste Schritte:

1. Speichern Sie die `README.md`-Datei im Hauptverzeichnis Ihres Projekts.
2. Laden Sie das Projekt auf GitHub hoch:

   ```bash
   git init
   git add .
   git commit -m "Initial commit mit README"
   git remote add origin https://github.com/<your-username>/PedestrianCommunication.git
   git push -u origin main
   ```

3. Überprüfen Sie das Repository auf GitHub, um sicherzustellen, dass die README korrekt angezeigt wird.

Falls Sie weitere Anpassungen (z. B. zusätzliche Abschnitte oder eine andere Sprache) wünschen, lassen Sie es mich wissen!
