#!/usr/bin/env bash
set -e

ENV_FILE=""
DEMO=false
ACTION=""

while [ $# -gt 0 ]; do
  case "$1" in
    -f)
      ENV_FILE="$2"
      shift 2
      ;;
    --demo)
      DEMO=true
      shift 1
      ;;
    *)
      [ -z "$ACTION" ] && ACTION="$1"
      shift
      ;;
  esac
done

[ -z "$ENV_FILE" ] && { echo "Usage: $0 -f <file> [--demo] {build|up|stop|down}"; exit 1; }
[ -z "$ACTION" ] && ACTION="up"

COMPOSE="docker compose --env-file $ENV_FILE -f docker-compose.yml"

containers_exist() {
  [ -n "$($COMPOSE ps -aq 2>/dev/null | head -1)" ]
}

run_prestart_and_seed() {
  $COMPOSE exec backend bash scripts/prestart.sh
  if [ "$DEMO" = true ]; then
    $COMPOSE cp backend/seed_data.py backend:/employee_saas/backend/seed_data.py
    $COMPOSE exec backend python seed_data.py
  fi
}

stack_up() {
  $COMPOSE up -d --no-build db backend
}

stack_up_and_wait() {
  $COMPOSE up -d --no-build db backend --wait
}

full_setup() {
  echo "==> Building images..."
  $COMPOSE build
  stack_up_and_wait
  echo "==> Running migrations + init data..."
  run_prestart_and_seed
}

case "$ACTION" in
  build)
    if containers_exist; then
      echo "==> Already built. Starting stack..."
      stack_up_and_wait
    else
      full_setup
      echo "==> Build complete. Stack is running."
    fi
    ;;

  up)
    if containers_exist; then
      stack_up
    else
      echo "==> Not built. Running full setup..."
      full_setup
    fi
    ;;

  stop)
    $COMPOSE stop
    ;;

  down)
    $COMPOSE down -v
    ;;

  *)
    echo "Usage: $0 -f <file> [--demo] {build|up|stop|down}"
    exit 1
    ;;
esac
