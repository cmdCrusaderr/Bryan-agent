import os
import pandas as pd
import numpy as np

filepath = "/Users/nishanttekwani/blueprint-agent/expanded_sleep_data_with_bio.csv"

def load_data_verify(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError("File not found at the specified path.")
    return pd.read_csv(filepath)

def data_preprocessing(targetpath):
    df = load_data_verify(targetpath)
    
    # 1. Standardize column headers
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # 2. Impute missing values for categorical blocks
    if 'sleep_disorder' in df.columns:
        df['sleep_disorder'] = df['sleep_disorder'].fillna('None')
        
    # 3. Clean and map categorical BMI classifications
    if 'bmi_category' in df.columns:
        df['bmi_category'] = df['bmi_category'].str.strip().str.replace('Normal Weight', 'Normal')

    # 4. Parse composite blood pressure strings into numerical dimensions
    if 'blood_pressure' in df.columns:
        df[['systolic_bp', 'diastolic_bp']] = df['blood_pressure'].astype(str).str.split('/', expand=True).astype(int)

    # 5. Extract sample tracking metrics for engineering
    num_rows = len(df)
    np.random.seed(42)

    # --- TABLE 1: BLUEPRINT PROTOCOL CONTROLS ---
    # Calculates a behavioral protocol compliance framework scaled by background stress indices
    habits_data = []
    for idx, row in df.iterrows():
        p_id = int(row['person_id'])
        stress = int(row['stress_level']) if 'stress_level' in df.columns else 5
        
        # High stress degrades the likelihood of strict curfew optimization
        compliance_prob = max(0.2, 1.0 - (stress * 0.10))
        is_compliant = np.random.choice([1, 0], p=[compliance_prob, 1.0 - compliance_prob])
        
        habits_data.append({
            "person_id": p_id,
            "supper_curfew_hours": round(np.random.uniform(4.5, 7.0) if is_compliant else np.random.uniform(0.5, 3.0), 1),
            "no_caffeine_after_noon": is_compliant,
            "blue_light_block_mins": np.random.randint(60, 90) if is_compliant else np.random.randint(0, 30),
            "supplement_compliance_pct": np.random.randint(95, 100) if is_compliant else np.random.randint(40, 80)
        })
    df_habits = pd.DataFrame(habits_data)

    # --- TABLE 2: NEURO-SLEEP ARCHITECTURE ---
    # Isolate neural markers, sleep periods, and derive macro sleep stages
    sleep_fields = [
        'person_id', 'sleep_duration', 'quality_of_sleep', 'sleep_disorder',
        'eeg_alpha', 'eeg_beta', 'eeg_theta'
    ]
    s_valid = [c for c in sleep_fields if c in df.columns]
    df_sleep = df[s_valid].copy()
    
    # Calculate sleep stage minutes leveraging total duration and protocol curfews
    if 'sleep_duration' in df_sleep.columns:
        total_mins = df_sleep['sleep_duration'] * 60
        
        # Tie micro sleep structures directly to the computed protocol constraints
        deep_ratios = np.where(df_habits['supper_curfew_hours'] >= 4.5, np.random.uniform(0.24, 0.32, size=num_rows), np.random.uniform(0.08, 0.16, size=num_rows))
        rem_ratios = np.where(df_habits['no_caffeine_after_noon'] == 1, np.random.uniform(0.20, 0.26, size=num_rows), np.random.uniform(0.10, 0.18, size=num_rows))
        
        df_sleep['deep_sleep_minutes'] = (total_mins * deep_ratios).astype(int)
        df_sleep['rem_sleep_minutes'] = (total_mins * rem_ratios).astype(int)
        
        # Adjust onset delays matching sleep quality and background disorder footprints
        base_latency = np.where(df_sleep['sleep_disorder'] != 'None', 35, 15)
        df_sleep['sleep_latency_minutes'] = (base_latency + np.random.randint(0, 20, size=num_rows)).astype(int)

    # --- TABLE 3: ADVANCED BIOMETRICS & ELECTROLYTES ---
    # Map physical performance metadata, ECG waves, and blood telemetry parameters
    biometric_fields = [
        'person_id', 'heart_rate', 'daily_steps', 'bmi_category', 'systolic_bp', 'diastolic_bp',
        'ecg_heartrate', 'ecg_qrs_duration', 'ecf_na', 'ecf_k', 'emg_mean', 'emg_max'
    ]
    b_valid = [c for c in biometric_fields if c in df.columns]
    df_vitals = df[b_valid].copy()
    
    # Feature Engineer Heart Rate Variability (HRV) using physical activity and stress markers
    if 'person_id' in df_vitals.columns:
        activity = df['physical_activity_level'] if 'physical_activity_level' in df.columns else 30
        stress = df['stress_level'] if 'stress_level' in df.columns else 5
        
        base_hrv = 85 + (activity * 0.3) - (stress * 5.5)
        # Screen restriction adherence provides systemic nervous system buffer to HRV
        hrv_boost = np.where(df_habits['blue_light_block_mins'] >= 60, np.random.randint(20, 40, size=num_rows), np.random.randint(-15, 5, size=num_rows))
        
        df_vitals['hrv_resting_ms'] = np.clip(base_hrv + hrv_boost, 35, 160).astype(int)
        df_vitals['skin_temp_delta_c'] = np.where(df_habits['blue_light_block_mins'] >= 60, np.round(np.random.uniform(-0.35, 0.05, size=num_rows), 2), np.round(np.random.uniform(0.25, 1.10, size=num_rows), 2))

    # 6. Export segmented relational engine structures to local disk
    os.makedirs("data", exist_ok=True)
    df_habits.to_csv("data/blueprint_habits.csv", index=False)
    df_sleep.to_csv("data/blueprint_sleep.csv", index=False)
    df_vitals.to_csv("data/blueprint_vitals.csv", index=False)
        
    print("PREPROCESSING PIPELINE COMPLETE MATCHING LOCAL CORES.")

if __name__ == "__main__":
    data_preprocessing(filepath)