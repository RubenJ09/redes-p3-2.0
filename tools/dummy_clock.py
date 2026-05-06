from __future__ import annotations

import argparse
from datetime import datetime, time as time_type, timedelta
import time
import paho.mqtt.client as mqtt

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulador de reloj IoT")
    parser.add_argument("id", help="Identificador del dispositivo")
    parser.add_argument("--host", default="redes2.ii.uam.es", help="Host del broker")
    parser.add_argument("-p", "--port", type=int, default=1883, help="Puerto del broker")
    parser.add_argument("--time", dest="start_time", default=None, help="Hora de inicio HH:MM:SS")
    parser.add_argument("--increment", type=float, default=1, help="Incremento en segundos")
    parser.add_argument("--rate", type=float, default=1, help="Frecuencia de envío en segundos")
    parser.add_argument("--base-topic", default="redes2/2311/04", help="Prefijo del topic")
    return parser

def parse_time(value: str | None) -> time_type:
    if value is None:
        return datetime.now().time().replace(microsecond=0)
    return datetime.strptime(value, "%H:%M:%S").time()

def main() -> None:
    args = build_parser().parse_args()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    
    client.connect(args.host, args.port, keepalive=60)
    client.loop_start()

    topic = f"{args.base_topic}/{args.id}"
    current_datetime = datetime.combine(datetime.today(), parse_time(args.start_time))

    try:
        while True:
            current_time_str = current_datetime.time().replace(microsecond=0).isoformat()
            client.publish(topic, current_time_str)
            time.sleep(args.rate)
            current_datetime += timedelta(seconds=args.increment)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()