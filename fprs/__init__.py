import numpy as np

seed = 42
fprs_random_state = np.random.RandomState(seed=42)


def set_random_state(
        seed_value: int
        ):
    global seed, fprs_random_state
    seed = seed_value
    fprs_random_state.seed(seed_value)
