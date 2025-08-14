# Wallbox (PUMP Connect) – Home Assistant Custom Integration

Zeigt deine Wallbox (über PUMP Connect) als **Gerät** in Home Assistant an – inklusive **Status**, **Leistung**, **Energie**, **Session-Dauer** sowie **Start/Stop**.

## Features
- Polling-only (kein Webhook/öffentlicher Zugriff nötig)
- Entities: Status, Power (W), Energy (kWh), Session Duration (s), Active Session ID, Charging (binary)
- Buttons: Start / Stop
- Konfiguration via UI (API-Key & Device-ID)
- HACS-kompatibel (als Custom Repository)

## Installation über HACS (Custom Repo)
1. Dieses Repository in HACS hinzufügen: **HACS → Integrations → Custom repositories → URL des Repos** (Kategorie: *Integration*).
2. Integration installieren und Home Assistant neu starten.
3. In HA: *Einstellungen → Geräte & Dienste → Integration hinzufügen* → **Wallbox (PUMP Connect)** wählen.
4. **API-Key** (x-api-key) und **Device-ID** aus dem PUMP-Portal eintragen.

## Hinweise
- Standard-Polling: 120 s (einstellbar im Code; OptionsFlow folgt).
- Energie/Session-Dauer werden aus der aktiven Session ermittelt (Feldnamen variieren je nach PUMP; Integration nutzt mehrere Fallbacks).
- Für sofortige Statuswechsel ggf. PUMP-App verwenden (Polling-Design).

## Debug-Logs
In `configuration.yaml`:
```yaml
logger:
  default: warning
  logs:
    custom_components.wallbox_pump: debug
```

## Lizenz
MIT