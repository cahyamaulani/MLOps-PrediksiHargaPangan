import numpy as np
import pandas as pd

def calculate_psi(expected, actual, buckets=10):

    expected_percents, bins = np.histogram(expected, bins=buckets)
    actual_percents, _ = np.histogram(actual, bins=bins)

    expected_percents = expected_percents / len(expected)
    actual_percents = actual_percents / len(actual)

    psi = np.sum(
        (actual_percents - expected_percents) *
        np.log((actual_percents + 1e-6) / (expected_percents + 1e-6))
    )

    return psi