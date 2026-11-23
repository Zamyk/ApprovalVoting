source venv/bin/activate 2>/dev/null || source .venv/bin/activate 2>/dev/null || true

PYTHON_CMD="python3.11"
if ! command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3"
fi

$PYTHON_CMD -m papers.proportional_rankings.experiments_enhanced.plot_experiment_2_datasets_2_all_by_candidates 2>&1
$PYTHON_CMD -m papers.proportional_rankings.experiments_enhanced.plot_experiment_2_datasets_2_all_by_voters 2>&1

deactivate 2>/dev/null || true
