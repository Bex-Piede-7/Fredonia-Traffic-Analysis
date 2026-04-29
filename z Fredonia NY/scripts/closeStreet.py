import traci
import os
import csv

# --- PATH SETUP ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SUMO_CONFIG = os.path.join(SCRIPT_DIR, "..", "net", "osm.sumocfg")

def load_schedule(file_name):
    """Reads a CSV and returns a list of closure dictionaries."""
    schedule = []
    path = os.path.join(SCRIPT_DIR, "..", file_name)
    with open(path, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert strings to integers for time
            schedule.append({
                "start": int(row['start']),
                "end": int(row['end']),
                "edge": row['edge_id']
            })
    return schedule

def run_simulation(schedule):
    traci.start(["sumo-gui", "-c", SUMO_CONFIG])
    
    while traci.simulation.getMinExpectedNumber() > 0:
        current_time = traci.simulation.getTime()
        
        # Check every item in our schedule list
        for item in schedule:
            if current_time == item['start']:
                print(f"[t={current_time}] CLOSING: {item['edge']}")
                traci.edge.setAllowed(item['edge'], [])
            
            elif current_time == item['end']:
                print(f"[t={current_time}] REOPENING: {item['edge']}")
                traci.edge.setAllowed(item['edge'], ["passenger"])
        
        traci.simulationStep()
    traci.close()

if __name__ == "__main__":
    # Now you just tell the script which schedule file to use!
    # Usage: python scripts/closeStreet.py schedule.csv
    import sys
    if len(sys.argv) > 1:
        my_schedule = load_schedule(sys.argv[1])
        run_simulation(my_schedule)
    else:
        print("Please provide a schedule CSV file.")