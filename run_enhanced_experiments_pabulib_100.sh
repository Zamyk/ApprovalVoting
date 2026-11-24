cd "$(dirname "$0")"
MODULE=papers.manipulation_of_hamming.experiments_enhanced.experiment_pabulib_100

if command -v uv &> /dev/null; then
    # uv creates/uses .venv from pyproject.toml + uv.lock
    RUN="uv run python"
else
    source venv/bin/activate 2>/dev/null || source .venv/bin/activate 2>/dev/null || true
    RUN="python3.11"
    command -v python3.11 &> /dev/null || RUN="python3"
fi

nohup nice -n 19 $RUN -m $MODULE > output_pabulib_100.log 2>&1 &
