# 📦 Changelog

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