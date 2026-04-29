import xml.etree.ElementTree as ET 
import matplotlib.pyplot as plt 
import numpy as np 
 
# --- Utility function --- 
def parse_tripinfo(filename): 
    tree = ET.parse(filename) 
    root = tree.getroot() 
    durations = [] 
    waiting_times = [] 
    for trip in root.findall("tripinfo"): 
        durations.append(float(trip.attrib["duration"])) 
        waiting_times.append(float(trip.attrib["waitingTime"])) 
    return np.array(durations), np.array(waiting_times) 
 
# --- Load results --- 
scenarios = { 
    "Baseline": "tripinfo_baseline.xml", 
    "Street Closure": "tripinfo_closure.xml"
} 
 
results = {} 
for name, file in scenarios.items(): 
    durations, waits = parse_tripinfo(file) 
    results[name] = { 
        "avg_duration": np.mean(durations), 
        "avg_wait": np.mean(waits) 
    } 
 
# --- Print summary table --- 
print("=== Scenario Summary ===") 
for name, r in results.items(): 
    print(f"{name:15s}  Avg Duration: {r['avg_duration']:.2f}s   Avg Wait: {r['avg_wait']:.2f}s") 
 
# --- Plot comparison --- 
labels = list(results.keys()) 
avg_durations = [results[k]["avg_duration"] for k in labels] 
avg_waits = [results[k]["avg_wait"] for k in labels] 
 
x = np.arange(len(labels)) 
width = 0.35 
 
fig, ax = plt.subplots(figsize=(7, 5)) 
ax.bar(x - width/2, avg_durations, width, label='Avg Travel Duration (s)') 
ax.bar(x + width/2, avg_waits, width, label='Avg Waiting Time (s)') 
 
ax.set_xticks(x) 
ax.set_xticklabels(labels) 
ax.set_ylabel("Seconds") 
ax.set_title("Traffic Performance Comparison") 
ax.legend() 
ax.grid(axis='y', linestyle='--', alpha=0.6) 
 
plt.tight_layout() 
plt.show() 
 