import pandas as pd
import numpy as np
import os

os.makedirs("data", exist_ok=True)

# Generate 5000 rows to perfectly match your blueprint dataset person_ids
num_rows = 5000
np.random.seed(42)

# 🏃‍♂️ 1. Create Garmin Mock Data (Focus: Exertion, Stress, Steps)
garmin_data = {
    "person_id": np.arange(1, num_rows + 1),
    "date": ["2026-05-27"] * num_rows,
    "highest_energy_level": np.random.randint(65, 98, size=num_rows),
    "lowest_energy_level": np.random.randint(5, 25, size=num_rows),
    "total_recharge": np.random.randint(50, 85, size=num_rows),
    "average_stress_level": np.random.randint(15, 65, size=num_rows),
    "resting_heart_rate": np.random.randint(52, 74, size=num_rows)
}
# Induce a crash state for person_id 1 for your demo presentation
garmin_data["highest_energy_level"][0] = 18
garmin_data["average_stress_level"][0] = 78

df_garmin = pd.DataFrame(garmin_data)
df_garmin.to_csv("data/garmin_mock.csv", index=False)

# ⚫ 2. Create Whoop Mock Data (Focus: HRV, Recovery, Strain)
whoop_data = {
    "person_id": np.arange(1, num_rows + 1),
    "cycle_id": np.arange(1001, 1001 + num_rows),
    "recovery_score": np.random.randint(35, 95, size=num_rows),
    "hrv_rmssd_ms": np.random.randint(40, 110, size=num_rows),
    "skin_temp_delta_c": np.round(np.random.uniform(-0.5, 0.6, size=num_rows), 2),
    "day_strain": np.round(np.random.uniform(8.0, 18.5, size=num_rows), 1),
    "max_heart_rate": np.random.randint(155, 192, size=num_rows)
}
# Induce a critical recovery failure state for person_id 1
whoop_data["recovery_score"][0] = 41
whoop_data["hrv_rmssd_ms"][0] = 42

df_whoop = pd.DataFrame(whoop_data)
df_whoop.to_csv("data/whoop_mock.csv", index=False)

print("Generated data/garmin_mock.csv and data/whoop_mock.csv successfully.")