import asyncio
import json
import paho.mqtt.client as mqtt
from APsystemsEZ1 import APsystemsEZ1M

# Ideas from https://github.com/SonnenladenGmbH/APsystems-EZ1-API/tree/main

# Konfiguration
INVERTER_IP = "192.168.1.100"
INVERTER_PORT = 8050
MQTT_BROKER = "localhost" 
MQTT_PORT = 1883
MQTT_TOPIC = "inverter/data"

# Initialisiere den Wechselrichter
inverter = APsystemsEZ1M(INVERTER_IP, INVERTER_PORT)

# MQTT-Client initialisieren
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

async def fetch_and_publish():
    try:
        data = {
            "device_info": await inverter.get_device_info(),
            "alarm_info": await inverter.get_alarm_info(),
            "output_data": await inverter.get_output_data(),
            "energy_today": await inverter.get_total_energy_today(),
            "energy_lifetime": await inverter.get_total_energy_lifetime(),
            "max_power": await inverter.get_max_power(),
            "power_status": await inverter.get_device_power_status()
        }
        
        # Konvertiere Daten in JSON
        payload = json.dumps(data)
        
        # Senden der Daten an den MQTT-Broker
        client.publish(MQTT_TOPIC, payload)
        print("Daten erfolgreich gesendet:", payload)
    except Exception as e:
        print(f"Fehler beim Abrufen der Daten: {e}")

# Hauptfunktion starten
async def main():
    while True:
        await fetch_and_publish()
        await asyncio.sleep(60)  # Alle 60 Sekunden Daten abrufen

asyncio.run(main())
