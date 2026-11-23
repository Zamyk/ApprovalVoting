source venv/bin/activate 2>/dev/null || source .venv/bin/activate 2>/dev/null || true

PYTHON_CMD="python3.11"
if ! command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3"
fi

nohup nice -n 19 $PYTHON_CMD -m papers.proportional_rankings.experiments_enhanced.generate_data_models_from_paper_with_new_instances > output.proportional_rankings.generate_data_models_from_paper_with_new_instances.log 2>&1 &

deactivate 2>/dev/null || true