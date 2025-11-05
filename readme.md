# MD-321

> Ein Raspberry Pi Projekt zur **Erfassung, Übertragung und Überwachung** von Sensordaten und Systemmetriken via REST API, Docker und Open-Source-Monitoring-Tools.

---

## Projektübersicht

Dieses Projekt wurde im Rahmen des Moduls **321 – IT-Kleinprojekt abwickeln** entwickelt. Der Fokus liegt auf:

- Erfassen von Sensorwerten
- Bereitstellen dieser Werte über eine REST API
- Monitoring der API und des Gesamtsystems mit Prometheus + Loki
- Dashboard zur Visualisierung der Sensordaten im Browser
- Deployment via Docker Compose

---

## Installation & Einrichtung

> Voraussetzung: Installiertes Docker & docker-compose auf Raspberry Pi

### 1. Sensor-API starten:

```bash
cd sensor-api
docker-compose up -d
```

### 2. Monitoring-Stack starten:

```bash
cd ../system-monitoring
docker-compose up -d
```

**Hinweis:** Passe ggf. die `.yaml`/`conf` Files an deine Netzwerkumgebung an.

---

## Sensor-API

Die Sensor-API bietet HTTP-Zugriff auf Echtzeit-Sensordaten eines Raspberry Pi.

Basis-URL: `http://<raspberry-ip>:8080`

### Sensoren

| Sensor       | Zweck                     | File              |
| ------------ | ------------------------- | ----------------- |
| DHT11/DHT22  | Temperatur & Feuchtigkeit | `main.py`         |
| Licht-Sensor | Helligkeit in %           | `light_sensor.py` |
| PIR Bewegung | Bewegungserkennung (Bool) | `pir_sensor.py`   |
| HC-SR04      | Distanzmessung in cm      | `main.py`         |
| Touch-Sensor | Berührbarer GPIO-Switch   | `main.py`         |

> Du kannst die API leicht erweitern, indem du weitere Module unter `/sensor-api` hinzufügst.

---

## System Monitoring Stack

Die Überwachung erfolgt über folgende Services:

| Service    | Port | Zweck                            |
| ---------- | ---- | -------------------------------- |
| Prometheus | 9090 | Metriken sammeln                 |
| Loki       | 3100 | Log-Daten speichern              |
| Promtail   | N/A  | Docker-Logs an Loki weiterleiten |

### Monitoring starten:

```bash
cd system-monitoring
docker-compose up -d
```

### Monitoring-Endpoints:

* **Prometheus UI** → `http://<host-ip>:9090`
* **Loki API** → `http://<host-ip>:3100/loki/api/v1/query`
* Optional: **Grafana** (kann einfach ergänzt werden)

---

## Web-Dashboard

Eine simple Visualisierung der API-Daten in HTML/JS:

```plaintext
sensor-api/dashboard/index.html
```

Öffne das File im Browser oder deploye es auf einem Webserver.

Du kannst das Dashboard jederzeit durch eigene UI oder Frameworks ersetzen (Vue/Tailwind/etc).

---

## Docker Services

| Container  | Beschreibung              | File                                |
| ---------- | ------------------------- | ----------------------------------- |
| sensor-api | Python API + GPIO Zugriff | `sensor-api/docker-compose.yaml`    |
| prometheus | Metrics Sampler           | `system-monitoring/prometheus.yaml` |
| loki       | Log Collection            | `system-monitoring/loki.yaml`       |
| promtail   | Log Forwarder             | `system-monitoring/promtail.yaml`   |
