import numpy as np

seed = 42
frps_random_state = np.random.RandomState(seed=42)


def set_random_state(
        seed_value: int
        ):
    global seed, frps_random_state
    seed = seed_value
    frps_random_state.seed(seed_value)
