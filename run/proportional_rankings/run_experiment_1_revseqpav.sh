source venv/bin/activate 2>/dev/null || source .venv/bin/activate 2>/dev/null || true

PYTHON_CMD="python3.11"
if ! command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3"
fi

nohup nice -n 0 $PYTHON_CMD -m papers.proportional_rankings.experiments.experiment_1_revseqpav > output.proportional_rankings.experiment_1_revseqpav.log 2>&1 &

deactivate 2>/dev/null || true