
import warnings
import gymnasium as gym
import torch as t

from ppo.my_probe_envs import Probe1, Probe2, Probe3, Probe4, Probe5
from ppo.utils import PPOArgs, arg_help
from ppo.train import train_ppo
from .utils import TrajectoryWriter

warnings.filterwarnings("ignore", category= DeprecationWarning)
device = t.device("cuda" if t.cuda.is_available() else "cpu")

if __name__ == "__main__":
    args = PPOArgs()
    args.track = False

    for i in range(5):
        probes = [Probe1, Probe2, Probe3, Probe4, Probe5]
        gym.envs.registration.register(id=f"Probe{i+1}-v0", entry_point=probes[i])

    if args.trajectory_path:
        trajectory_writer = TrajectoryWriter(args.trajectory_path, args)
    else:
        trajectory_writer = None

    arg_help(args)
    train_ppo(args, trajectory_writer=trajectory_writer)

