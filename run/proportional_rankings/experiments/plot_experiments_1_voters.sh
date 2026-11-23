source venv/bin/activate 2>/dev/null || source .venv/bin/activate 2>/dev/null || true

PYTHON_CMD="python3.11"
if ! command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3"
fi

$PYTHON_CMD -m papers.proportional_rankings.experiments.plot_experiment_1_all_voters

deactivate 2>/dev/null || true
