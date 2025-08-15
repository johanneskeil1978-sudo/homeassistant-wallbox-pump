# 📦 Changelog


## [0.1.5] - 2025-08-15
### 🔹 Neu
- **Polling konfigurierbar**: Neues Options-Menü in der Integration erlaubt die Einstellung des Abfrageintervalls (`scan_interval`) zwischen 15 s und 3600 s.
- **Live-Übernahme** des Intervalls ohne Neustart der Integration.
- **Standard**: 120 s.

### 🔹 Technisches
- Implementierung über `OptionsFlow`.
- Automatisches Limitieren von zu kleinen/großen Werten.

## [0.1.4] - 2025-08-14
### 🔹 Neu
- **Geräte-Zuordnung korrigiert**:  
  Alle Entitäten (Status, Leistung, Energie, Session-Dauer, Session-ID, Charging, Start, Stop) werden jetzt sauber unter **einem Gerät „Wallbox“** angezeigt.  
  → Umsetzung über `unique_id` und `DeviceInfo` mit identischen `identifiers`.  
- **Code-Cleanup**:  
  - Vereinheitlichte `device_info`-Funktion für Sensoren, Binary-Sensoren und Buttons.  
  - Konsistente `unique_id`-Namensgebung: `{domain}_{device_id}_{suffix}`.
- **Manifest** auf Version 0.1.4 aktualisiert.  
- **README** und `hacs.json` ergänzt, um HACS-Kompatibilität zu sichern.

### 🔹 Bugfixes
- Entitäten hingen zuvor lose unter der Integration und nicht am Gerät.  
- Keine funktionale Änderung an der API-Abfrage – Polling bleibt bei 120 Sekunden Standard.
