import numpy as np
import pandas as pd

def generate_sin_cos_tan_with_drifts(n=600, noise_std=0.0, seed=42):
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    s1, s2 = n // 3, 2 * n // 3

    cfg = [
        dict(sin_amp=1.0, sin_freq=0.020, cos_amp=0.6, cos_freq=0.030, tan_amp=0.2, tan_freq=0.006),
        dict(sin_amp=1.8, sin_freq=0.045, cos_amp=0.3, cos_freq=0.015, tan_amp=0.35, tan_freq=0.012),
        dict(sin_amp=0.8, sin_freq=0.010, cos_amp=1.2, cos_freq=0.050, tan_amp=0.5, tan_freq=0.004),
    ]

    sin_vals, cos_vals, tan_vals = [], [], []

    def seg(i):
        return 0 if i < s1 else (1 if i < s2 else 2)

    for i in range(n):
        c = cfg[seg(i)]
        sin_vals.append(c["sin_amp"] * np.sin(2*np.pi*c["sin_freq"]*i))
        cos_vals.append(c["cos_amp"] * np.cos(2*np.pi*c["cos_freq"]*i))
        tan_arg = 2*np.pi*c["tan_freq"]*i
        tv = c["tan_amp"] * np.tan(tan_arg)
        tan_vals.append(np.clip(tv, -3.0, 3.0))

    df = pd.DataFrame({"Sequence": t, "Sin": sin_vals, "Cos": cos_vals, "Tan": tan_vals})
    return df

