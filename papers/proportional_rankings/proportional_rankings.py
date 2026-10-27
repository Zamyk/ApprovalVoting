import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
import os
import logging
from pathlib import Path

from votekit.pref_profile.approval_profile import ApprovalProfile
from votekit.elections.election_types.approval.hamming import OrderedWeightedHamming
from votekit.ballot_generator.std_generator.approval_impartial_culture import approval_ic_profile_generator, approval_biased_profile_generator
from votekit.comsoc.approval_manipulations import for_all_manipulations




def save_data(path, data):
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)


def experiment_1(path, n_voters, n_iterations, candidates, gen, *, n_jobs=1, verbose=True):
    log_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=log_level, format='%(message)s')

    results = []
    for i, m in enumerate(candidates):
        inner_candidates = [str(k) for k in range(m)]
        for j, fi in enumerate(range(n_voters)):
            manipulability_ratio = get_manipulability_ratio(inner_candidates, n_voters, gen, ("f", fi), n_iterations, n_jobs=n_jobs)
            results.append({
                'm': m,
                'orness': orness(n_voters, fi),
                'manipulability': manipulability_ratio
            })
            logging.info(f"Calculations completion [{(i*n_voters+j+1)/(len(candidates)*n_voters):.2%}]")
        logging.info(f"Completed calculations for {m} candidates")
    save_data(path.with_suffix(".csv"), results)
