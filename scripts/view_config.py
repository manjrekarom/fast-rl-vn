import os
import random
import argparse

import numpy as np

from habitat_baselines.common.baseline_registry import baseline_registry
from habitat_baselines.config.default import get_config as get_baselines_config


parser = argparse.ArgumentParser(description='View Config')

parser.add_argument('path', type=str, help='Config Path')
args = parser.parse_args()
print('Args:', args)


if __name__ == "__main__":
    # TODO: CHANGE PATH
    habitat_base_path = os.environ['HABITAT']
    cwd = os.getcwd()
    os.chdir(habitat_base_path)
    # seed = "42"  # @param {type:"string"}
    # steps_in_thousands = "10"  # @param {type:"string"}
    config = get_baselines_config(os.path.join(cwd, args.path))
    print(config)
