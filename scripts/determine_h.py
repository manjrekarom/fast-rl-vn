import os
import argparse

import habitat
from habitat_baselines.agents.ppo_agents import PPOAgent, get_default_config


def main():
    habitat_base_path = os.environ['HABITAT']  #or '/home/omanjrekar/MBRL-VLN/habitat-lab'
    os.chdir(habitat_base_path)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-type",
        default="rgb",
        choices=["blind", "rgb", "depth", "rgbd"],
    )
    parser.add_argument("checkpoint", type=str, help='Absolute path to the checkpoint')
    parser.add_argument(
        "--task-config", type=str, default="/home/omanjrekar/MBRL-VLN/configs/ppo_pointnav_rgb_hm3d_eval.yaml"
    )
    parser.add_argument(
        "--num-episodes", type=int, default=None
    )
    args = parser.parse_args()

    agent_config = get_default_config()
    agent_config.INPUT_TYPE = args.input_type
    if args.checkpoint is not None:
        agent_config.MODEL_PATH = args.checkpoint

    agent = PPOAgent(agent_config)
    benchmark = habitat.Benchmark(config_paths=args.task_config)
    metrics = benchmark.evaluate(agent, args.num_episodes)

    for k, v in metrics.items():
        habitat.logger.info("{}: {:.3f}".format(k, v))


if __name__ == "__main__":
    main()
