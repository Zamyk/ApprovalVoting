from experiments.experiment_1 import run_experiment_1
from experiments.experiment_2 import run_experiment_2
from experiments.plot_experiment_1 import plot_experiment_1
from experiments.plot_experiment_2 import plot_experiment_2
from experiments_enhanced.experiment_1 import run_experiment_1 as run_experiment_1_enhanced
from experiments_enhanced.experiment_2 import run_experiment_2 as run_experiment_2_enhanced
from experiments_enhanced.plot_experiment_1 import plot_experiment_1 as plot_experiment_1_enhanced
from experiments_enhanced.plot_experiment_2 import plot_experiment_2 as plot_experiment_2_enhanced


if __name__ == "__main__":
    run_experiment_1()
    plot_experiment_1()
    run_experiment_2()
    plot_experiment_2()
    run_experiment_1_enhanced()
    plot_experiment_1_enhanced()
    run_experiment_2_enhanced()
    plot_experiment_2_enhanced()