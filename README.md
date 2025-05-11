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
