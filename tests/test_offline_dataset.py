import pytest

from src.decision_transformer.offline_dataset import TrajectoryLoader, TrajectoryReader

PATH = "tests/fixtures/test_trajectories.pkl"
PATH_COMPRESSED = "tests/fixtures/test_trajectories.xz"


def get_len_i_for_i_in_list(l):
    return [len(i) for i in l]


def test_trajectory_reader():

    trajectory_reader = TrajectoryReader(PATH)
    data = trajectory_reader.read()
    assert data is not None


def test_trajectory_reader_xz():

    trajectory_reader = TrajectoryReader(PATH_COMPRESSED)
    data = trajectory_reader.read()
    assert data is not None


def test_init_trajectory_loader():

    trajectory_data_set = TrajectoryLoader(PATH, pct_traj=1.0, device="cpu")

    assert trajectory_data_set.num_trajectories == 55
    assert trajectory_data_set.num_timesteps == 49920
    assert trajectory_data_set.actions is not None
    assert trajectory_data_set.rewards is not None
    assert trajectory_data_set.dones is not None
    assert trajectory_data_set.returns is not None
    assert trajectory_data_set.states is not None
    assert trajectory_data_set.timesteps is not None

    assert len(trajectory_data_set.actions) == len(trajectory_data_set.rewards)
    assert len(trajectory_data_set.actions) == len(trajectory_data_set.dones)
    assert len(trajectory_data_set.actions) == len(trajectory_data_set.returns)
    assert len(trajectory_data_set.actions) == len(trajectory_data_set.states)

    # lengths match
    assert get_len_i_for_i_in_list(
        trajectory_data_set.actions) == get_len_i_for_i_in_list(trajectory_data_set.states)

    # max traj length is 1000
    assert max(get_len_i_for_i_in_list(trajectory_data_set.actions)
               ) == trajectory_data_set.max_ep_len
    assert trajectory_data_set.max_ep_len == trajectory_data_set.metadata["args"]["max_steps"]


def test_init_trajectory_loader_xz():

    trajectory_data_set = TrajectoryLoader(
        PATH_COMPRESSED, pct_traj=1.0, device="cpu")

    assert trajectory_data_set.num_trajectories == 239
    assert trajectory_data_set.num_timesteps == 1920
    assert trajectory_data_set.actions is not None
    assert trajectory_data_set.rewards is not None
    assert trajectory_data_set.dones is not None
    assert trajectory_data_set.returns is not None
    assert trajectory_data_set.states is not None
    assert trajectory_data_set.timesteps is not None

    assert len(trajectory_data_set.actions) == len(trajectory_data_set.rewards)
    assert len(trajectory_data_set.actions) == len(trajectory_data_set.dones)
    assert len(trajectory_data_set.actions) == len(trajectory_data_set.returns)
    assert len(trajectory_data_set.actions) == len(trajectory_data_set.states)

    # lengths match
    assert get_len_i_for_i_in_list(
        trajectory_data_set.actions) == get_len_i_for_i_in_list(trajectory_data_set.states)


def test_trajectory_loader_get_batch():

    trajectory_data_set = TrajectoryLoader(PATH, pct_traj=1.0, device="cpu")
    s, a, r, d, rtg, timesteps, mask = trajectory_data_set.get_batch(
        batch_size=16, max_len=100)

    assert s.shape == (16, 100, 7, 7, 3)
    assert a.shape == (16, 100)
    assert r.shape == (16, 100, 1)  # flatten this later?
    assert d.shape == (16, 100)
    assert rtg.shape == (16, 101, 1)  # how did we get the extra timestep?
    assert timesteps.shape == (16, 100)
    assert mask.shape == (16, 100)


def test_trajectory_loader_get_indices_of_top_p():

    trajectory_data_set = TrajectoryLoader(PATH, pct_traj=1.0, device="cpu")
    indices = trajectory_data_set.get_indices_of_top_p_trajectories(
        pct_traj=0.1)

    assert len(indices) == 7
    assert indices[0] == 23
    assert indices[-1] == 33


# def test_init_trajectory_loader_pct_traj_001():

#     trajectory_data_set = TrajectoryLoader(PATH, pct_traj=.01, device="cpu")

#     assert trajectory_data_set.num_trajectories == 43319
#     assert trajectory_data_set.num_timesteps == 799744
#     assert trajectory_data_set.actions is not None
#     assert trajectory_data_set.rewards is not None
#     assert trajectory_data_set.dones is not None
#     assert trajectory_data_set.returns is not None
#     assert trajectory_data_set.states is not None
#     assert trajectory_data_set.timesteps is not None

#     assert len(trajectory_data_set.actions) == len(trajectory_data_set.rewards)
#     assert len(trajectory_data_set.actions) == len(trajectory_data_set.dones)
#     assert len(trajectory_data_set.actions) == len(trajectory_data_set.returns)
#     assert len(trajectory_data_set.actions) == len(trajectory_data_set.states)
