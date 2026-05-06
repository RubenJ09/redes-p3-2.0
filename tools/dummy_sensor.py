from __future__ import annotations

import argparse
import time
import paho.mqtt.client as mqtt

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulador de sensor IoT")
    parser.add_argument("id", help="Identificador del dispositivo")
    parser.add_argument("--host", default="redes2.ii.uam.es", help="Host del broker")
    parser.add_argument("-p", "--port", type=int, default=1883, help="Puerto del broker")
    # Argumentos exactos requeridos por el enunciado
    parser.add_argument("-i", "--interval", type=float, default=1, help="Segundos entre envíos")
    parser.add_argument("-m", "--min", dest="minimum", type=float, default=20, help="Valor mínimo")
    parser.add_argument("-M", "--max", dest="maximum", type=float, default=30, help="Valor máximo")
    parser.add_argument("--increment", type=float, default=1, help="Incremento del valor")
    parser.add_argument("--base-topic", default="redes2/2311/04", help="Prefijo del topic")
    return parser

def main() -> None:
    args = build_parser().parse_args()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(args.host, args.port, keepalive=60)
    client.loop_start()

    topic = f"{args.base_topic}/{args.id}"
    value = args.minimum
    increasing = True

    try:
        while True:
            client.publish(topic, str(value))
            time.sleep(args.interval)
            if increasing:
                value += args.increment
                if value >= args.maximum:
                    value = args.maximum
                    increasing = False
            else:
                value -= args.increment
                if value <= args.minimum:
                    value = args.minimum
                    increasing = True
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()