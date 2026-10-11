source venv/bin/activate 2>/dev/null || source .venv/bin/activate 2>/dev/null || true

PYTHON_CMD="python3.11"
if ! command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3"
fi

if [ -f "papers/manipulation_of_hamming/experiments/results/experiment_1_uniform.csv" ]; then
    $PYTHON_CMD -m papers.manipulation_of_hamming.experiments.plot_experiment_1
fi

if [ -f "papers/manipulation_of_hamming/experiments_enhanced/plot_experiment_1_interval.py" ]; then
    $PYTHON_CMD -m papers.manipulation_of_hamming.experiments_enhanced.plot_experiment_1_interval "$@"
fi

deactivate 2>/dev/null || true
