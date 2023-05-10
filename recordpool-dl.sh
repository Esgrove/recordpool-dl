#!/bin/bash
set -eo pipefail

USAGE="USAGE: $0"

# Get absolute path to repo root
REPO_ROOT=$(git rev-parse --show-toplevel || (cd "$(dirname "${BASH_SOURCE[0]}")" && pwd))

init_options() {
    while [ $# -gt 0 ]; do
        case "$1" in
            -h|--help)
                echo "$USAGE"
                exit 1
                ;;
            --verbose)
                # Print shell commands
                set -x
                ;;
        esac
        shift
    done
}

init_options "$@"

PYTHON_MAIN="$REPO_ROOT/src/RecordPoolDownloader.py"

# macOS uses 'python3' by default but Windows uses just 'python'
if [ -n "$(command -v python3)" ]; then
    python3 "$PYTHON_MAIN"
elif [ -n "$(command -v python)" ]; then
    python "$PYTHON_MAIN"
else
    echo "Python not found, install Python 3 and make sure it is found in PATH"
    exit 1
fi
