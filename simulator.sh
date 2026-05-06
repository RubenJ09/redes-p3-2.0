#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"
HOST="${MQTT_HOST:-localhost}"
PORT="${MQTT_PORT:-1883}"

echo "Iniciando sistema en $HOST:$PORT..."

"$PYTHON_BIN" manage.py run_controller --host "$HOST" --port "$PORT" &
CONTROLLER_PID=$!

cleanup() {
    echo "Cerrando procesos..."
    kill $(jobs -p) 2>/dev/null || true
    exit
}
trap cleanup SIGINT SIGTERM EXIT

sleep 2

"$PYTHON_BIN" tools/dummy_switch.py --host "$HOST" --port "$PORT" switch_caldera &
"$PYTHON_BIN" tools/dummy_sensor.py --host "$HOST" --port "$PORT" sensor_salon &
"$PYTHON_BIN" tools/dummy_clock.py --host "$HOST" --port "$PORT" clock_salon &

echo "Simulación en marcha. Pulsa Ctrl+C para detener."
wait