import os
import random
import argparse
import shutil

import numpy as np

from habitat_baselines.common.baseline_registry import baseline_registry
from habitat_baselines.config.default import get_config as get_baselines_config

parser = argparse.ArgumentParser(description='Train (DD)PPO')

parser.add_argument('name', type=str, help='Experiment name (E.g.: ppo_rgb_hm3d_train_10')
parser.add_argument('path', type=str, help='Config Path')
parser.add_argument('--train', '--train-split', type=str, default='train_10_percent', \
    help='Train split to use for training')
parser.add_argument('--clean', action='store_true', default='Delete previous created folders with same exp name.')
args = parser.parse_args()
print('Args:', args)


if __name__ == "__main__":
    experiment_name = args.name
    habitat_base_path = os.environ['HABITAT']  #or '/home/omanjrekar/MBRL-VLN/habitat-lab'
    
    cwd = os.getcwd()
    os.chdir(habitat_base_path)

    # clean
    if args.clean:
        if os.path.exists(f'tb/{args.name}'):
            shutil.rmtree(f'tb/{args.name}')
        if os.path.exists(f'checkpoints/{experiment_name}'):
            shutil.rmtree(f'checkpoints/{args.name}')
        if os.path.exists(f'train_{experiment_name}.log'):
            os.remove(f'train_{experiment_name}.log')

    # seed = "42"  # @param {type:"string"}
    # steps_in_thousands = "10"  # @param {type:"string"}
    config = get_baselines_config(os.path.join(cwd, args.path))

    config.defrost()
    # training on val
    config.CHECKPOINT_FOLDER = f'checkpoints/{experiment_name}/'
    config.EVAL_CKPT_PATH_DIR = f'checkpoints/{experiment_name}/'
    config.LOG_FILE = f'train_{experiment_name}.log'
    config.NUM_UPDATES = -1
    config.EVAL.USE_CKPT_CONFIG = False
    # default is RGB_SENSOR
    config.SENSORS = ['RGB_SENSOR']
    # training on train_10
    config.TASK_CONFIG.DATASET.DATA_PATH = './data/datasets/pointnav/hm3d/v1/{split}/{split}.json.gz'
    config.TASK_CONFIG.DATASET.SPLIT = args.train
    config.TENSORBOARD_DIR = f'tb/{experiment_name}'
    config.VIDEO_OPTION = ["disk", "tensorboard"]
    config.freeze()
    print(config)

    random.seed(config.TASK_CONFIG.SEED)
    np.random.seed(config.TASK_CONFIG.SEED)

    trainer_init = baseline_registry.get_trainer(config.TRAINER_NAME)
    trainer = trainer_init(config)
    trainer.train()
