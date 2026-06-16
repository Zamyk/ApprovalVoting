source venv/bin/activate

nohup nice -n 19 python3.11 -m papers.manipulation_of_hamming.experiments.experiment_1 > output_1.log 2>&1 &


deactivate