import csv
import random
import os
from datetime import datetime

def generate_live_data():
    scenarios = ["OPTIMAL", "WARNING", "CRITICAL"]
    current_state = random.choices(scenarios, weights=[40, 40, 20], k=1)[0]
    
    print(f"Simulating morning wearable sync... Generating {current_state} metrics.")
    today_str = datetime.now().strftime("%Y-%m-%d")

    if current_state == "OPTIMAL":
        hrv = random.randint(75, 120)
        stress = random.randint(15, 35)
        curfew = round(random.uniform(3.5, 5.0), 1) 
        strain = round(random.uniform(14.0, 18.0), 1)
    elif current_state == "WARNING":
        hrv = random.randint(46, 60)
        stress = random.randint(40, 60)
        curfew = round(random.uniform(2.0, 3.0), 1) 
        strain = round(random.uniform(10.0, 13.0), 1)
    else: # CRITICAL
        hrv = random.randint(30, 44)
        stress = random.randint(66, 85)
        curfew = round(random.uniform(0.5, 1.5), 1) 
        strain = round(random.uniform(6.0, 9.0), 1)

    # 1. Update Habits (Root Folder)
    with open("blueprint_habits.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["person_id", "supper_curfew_hours", "no_caffeine_after_noon", "blue_light_block_mins", "supplement_compliance_pct"])
        writer.writerow([1, curfew, 1 if current_state == "OPTIMAL" else random.choice([0, 1]), random.randint(60, 120) if current_state != "CRITICAL" else random.randint(10, 45), random.randint(90, 100) if current_state != "CRITICAL" else random.randint(50, 70)])

    # 2. Update Garmin (Root Folder)
    with open("garmin_tracker.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["person_id", "date", "highest_energy_level", "lowest_energy_level", "total_recharge", "average_stress_level", "resting_heart_rate"])
        writer.writerow([1, today_str, random.randint(80, 100) if current_state == "OPTIMAL" else random.randint(40, 70), random.randint(5, 20), random.randint(70, 100) if current_state == "OPTIMAL" else random.randint(20, 50), stress, random.randint(50, 55) if current_state == "OPTIMAL" else random.randint(60, 70)])

    # 3. Update Whoop (Root Folder)
    with open("whoop_tracker.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["person_id", "cycle_id", "recovery_score", "hrv_rmssd_ms", "skin_temp_delta_c", "day_strain", "max_heart_rate"])
        writer.writerow([1, random.randint(1000, 9999), random.randint(70, 95) if current_state == "OPTIMAL" else random.randint(20, 50), hrv, round(random.uniform(-0.2, 0.2), 2), strain, random.randint(165, 185)])

    print("Data successfully written to root CSV schemas.")

if __name__ == "__main__":
    generate_live_data()