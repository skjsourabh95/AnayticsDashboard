import numpy as np


def cusum(x, threshold_std=1):
    """
    CUSUM implementation. Reference https://en.wikipedia.org/wiki/CUSUM

    Args:
        x:  the observed values
        threshold_std: the number times of standard deviation for the threshold

    Returns:
        the list of cumulative sums
    """

    mean = np.mean(x)
    std = np.std(x)
    threshold = threshold_std * std

    # weights of the threshold values
    nu = abs(threshold - mean)

    # normalize values
    values = (x - mean - nu / 2) / std

    v_sum = 0
    cusum_values = []
    for v in values:
        v += v_sum
        v_sum = np.maximum(v, 0)
        cusum_values.append(v_sum)

    return np.array(cusum_values)


def hlm(x, past_years=3):
    """
    Historical Limits Method (HLM) implementation. Reference http://wwwnc.cdc.gov/EID/article/21/2/14-0098-Techapp1.pdf

    Args:
        x: the observed values
        past_years: the period

    Returns:
        0 - if current values less than historical limits
        ratio - if current values greater than historical limits
    """

    x_curr = x[-1]
    x_past = x[:-1][-past_years:]

    mean = x_past.mean()
    std = x_past.std()
    ratio = (x_curr - mean) / std

    return np.where((x_curr / mean) > (1 + 2 * (std / mean)), ratio, 0)
