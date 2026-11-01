#!/bin/sh
# The AWTRIX NG TC002 simulator for NimbusPL, from the firmware's own Linux build:
#   tc002  52x16  http://localhost:8081
# Usage: sim/sim.sh build
#        sim/sim.sh start|stop|deploy|logs|mqtt
#        sim/sim.sh pub <topic> <payload> [-r]                   (publish on the test broker)
set -e
cd "$(dirname "$0")/.."

REF="${AWTRIX_REF:-v1.2.2}"
IMAGE="awtrix-ng-sim:$REF"
NET=awtrix-sim
BROKER=awtrix-mqtt

if [ "$1" = pub ]; then
  docker exec "$BROKER" mosquitto_pub -t "$2" -m "$3" $4
  exit 0
fi

# AWTRIX_SIM_TC002: run the TC002's own clock app (see sim/Dockerfile)
CLOCK=tc002; NAME=awtrix-sim-tc002; PORT=8081; SIZE="--width 52 --height 16"; DATA=awtrix-sim-tc002-data; ENV="-e AWTRIX_SIM_TC002=1"
URL="http://localhost:$PORT"

case "$1" in
  build)
    # --load: a buildx builder otherwise keeps the image in its cache only
    docker build --load -t "$IMAGE" --build-arg AWTRIX_REF="$REF" sim
    ;;
  start)
    docker network create "$NET" >/dev/null 2>&1 || true
    docker rm -f "$NAME" >/dev/null 2>&1 || true
    docker run -d --name "$NAME" --network "$NET" -p "$PORT:8080" -v "$DATA:/data" $ENV "$IMAGE" $SIZE >/dev/null
    echo "AWTRIX NG $REF TC002 simulator on $URL"
    ;;
  stop)
    docker stop "$NAME" >/dev/null && echo "stopped"
    ;;
  deploy)
    curl -sS -H "Content-Type: text/plain" -X PUT --data-binary "@dist/nimbus-$CLOCK.ax" "$URL/api/v1/apps/script/Nimbus"
    echo
    ;;
  logs)
    docker logs -f "$NAME"
    ;;
  mqtt)
    # a local Mosquitto for the tests; the simulator reads its broker settings at start
    docker network create "$NET" >/dev/null 2>&1 || true
    if ! docker ps --format '{{.Names}}' | grep -qx "$BROKER"; then
      docker rm -f "$BROKER" >/dev/null 2>&1 || true
      docker run -d --name "$BROKER" --network "$NET" eclipse-mosquitto:2 mosquitto -c /mosquitto-no-auth.conf >/dev/null
    fi
    curl -sS -X PUT -H "Content-Type: application/json" \
      -d "{\"mqttEnabled\":true,\"mqttHost\":\"$BROKER\",\"mqttPort\":1883}" "$URL/api/v1/system" >/dev/null
    docker restart "$NAME" >/dev/null
    echo "TC002 simulator connected to $BROKER"
    ;;
  *)
    echo "Usage: $0 build | start|stop|deploy|logs|mqtt | pub <topic> <payload> [-r]" >&2
    exit 1
    ;;
esac
