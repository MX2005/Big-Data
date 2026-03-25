#!/usr/bin/env bash

set -euo pipefail

CONTAINER_PATH="/app/pipeline"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="${HOST_RESULTS_DIR:-$SCRIPT_DIR/results}"

usage() {
  cat <<'EOF'
Usage: ./summary.sh [container_name_or_id]

Copies all generated .csv, .txt, and .png files from /app/pipeline inside the
container into the host results directory, then stops and removes that container.

If no container is provided, the script will use the only running container.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Error: docker is not installed or not available in PATH." >&2
  exit 1
fi

container="${1:-}"

if [[ -z "$container" ]]; then
  mapfile -t running_containers < <(docker ps --format '{{.Names}}')

  if [[ "${#running_containers[@]}" -eq 0 ]]; then
    echo "Error: no running containers found. Pass the container name or ID to summary.sh." >&2
    exit 1
  fi

  if [[ "${#running_containers[@]}" -gt 1 ]]; then
    echo "Error: multiple running containers found. Pass the container name or ID explicitly." >&2
    printf 'Running containers:\n' >&2
    printf '  %s\n' "${running_containers[@]}" >&2
    exit 1
  fi

  container="${running_containers[0]}"
fi

if ! docker inspect "$container" >/dev/null 2>&1; then
  echo "Error: container '$container' does not exist." >&2
  exit 1
fi

is_running="$(docker inspect -f '{{.State.Running}}' "$container")"

if [[ "$is_running" != "true" ]]; then
  echo "Error: container '$container' is not running." >&2
  exit 1
fi

mkdir -p "$RESULTS_DIR"

mapfile -t output_files < <(
  docker exec "$container" sh -c \
    "find '$CONTAINER_PATH' -maxdepth 1 -type f \\( -name '*.csv' -o -name '*.txt' -o -name '*.png' \\) | sort"
)

if [[ "${#output_files[@]}" -eq 0 ]]; then
  echo "Error: no .csv, .txt, or .png files were found in $CONTAINER_PATH inside '$container'." >&2
  exit 1
fi

for file_path in "${output_files[@]}"; do
  docker cp "$container:$file_path" "$RESULTS_DIR/"
done

docker stop "$container" >/dev/null
docker rm "$container" >/dev/null

echo "Copied ${#output_files[@]} file(s) to '$RESULTS_DIR'."
echo "Stopped and removed container '$container'."
