source venv/bin/activate 2>/dev/null || source .venv/bin/activate 2>/dev/null || true

PYTHON_CMD="python3.11"
if ! command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3"
fi

nohup nice -n 19 $PYTHON_CMD -m papers.manipulation_of_hamming.experiments_enhanced.experiment_1_euclidean_integers > output_1_euclidean_integers.log 2>&1 &

deactivate 2>/dev/null || true