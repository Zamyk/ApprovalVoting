source venv/bin/activate 2>/dev/null || source .venv/bin/activate 2>/dev/null || true

PYTHON_CMD="python3.11"
if ! command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3"
fi

nohup nice -n 19 $PYTHON_CMD -m papers.proportional_rankings.experiments_enhanced.experiment_1_datasets_2_2_geometric > output.proportional_rankings.experiment_1_datasets_2_2_geometric.log 2>&1 &
nohup nice -n 19 $PYTHON_CMD -m papers.proportional_rankings.experiments_enhanced.experiment_1_datasets_2_5_4_geometric > output.proportional_rankings.experiment_1_datasets_2_5_4_geometric.log 2>&1 &
nohup nice -n 19 $PYTHON_CMD -m papers.proportional_rankings.experiments_enhanced.experiment_1_datasets_2_10_geometric > output.proportional_rankings.experiment_1_datasets_2_10_geometric.log 2>&1 &
nohup nice -n 19 $PYTHON_CMD -m papers.proportional_rankings.experiments_enhanced.experiment_1_datasets_2_av > output.proportional_rankings.experiment_1_datasets_2_av.log 2>&1 &
nohup nice -n 19 $PYTHON_CMD -m papers.proportional_rankings.experiments_enhanced.experiment_1_datasets_2_best_of > output.proportional_rankings.experiment_1_datasets_2_best_of.log 2>&1 &
nohup nice -n 19 $PYTHON_CMD -m papers.proportional_rankings.experiments_enhanced.experiment_1_datasets_2_greedycc > output.proportional_rankings.experiment_1_datasets_2_greedycc.log 2>&1 &
nohup nice -n 19 $PYTHON_CMD -m papers.proportional_rankings.experiments_enhanced.experiment_1_datasets_2_phragmen > output.proportional_rankings.experiment_1_datasets_2_phragmen.log 2>&1 &
nohup nice -n 19 $PYTHON_CMD -m papers.proportional_rankings.experiments_enhanced.experiment_1_datasets_2_revseqpav > output.proportional_rankings.experiment_1_datasets_2_revseqpav.log 2>&1 &
nohup nice -n 19 $PYTHON_CMD -m papers.proportional_rankings.experiments_enhanced.experiment_1_datasets_2_seqpav > output.proportional_rankings.experiment_1_datasets_2_seqpav.log 2>&1 &

deactivate 2>/dev/null || true