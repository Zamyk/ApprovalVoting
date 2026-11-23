source venv/bin/activate 2>/dev/null || source .venv/bin/activate 2>/dev/null || true

PYTHON_CMD="python3.11"
if ! command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3"
fi

$PYTHON_CMD -m papers.manipulation_of_hamming.experiments_enhanced.plot_experiment_1_euclidean "$@"
$PYTHON_CMD -m papers.manipulation_of_hamming.experiments_enhanced.plot_experiment_2_euclidean "$@"

deactivate 2>/dev/null || true
