source venv/bin/activate

nohup nice -n 19 python3.11 -m papers.manipulation_of_hamming.experiments_enhanced.experiment_3 > output_3.log 2>&1 &
nohup nice -n 19 python3.11 -m papers.manipulation_of_hamming.experiments_enhanced.experiment_4 > output_4.log 2>&1 &
nohup nice -n 19 python3.11 -m papers.manipulation_of_hamming.experiments_enhanced.experiment_5 > output_5.log 2>&1 &


deactivate