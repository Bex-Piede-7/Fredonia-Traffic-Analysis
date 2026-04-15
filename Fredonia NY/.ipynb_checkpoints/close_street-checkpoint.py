import traci 

# Start SUMO-GUI 
traci.start(["sumo-gui", "-c", "osm.sumocfg"]) 

  

# Define multiple edges to close 
closed_edges = ["5670803#0","1051750427#0", "-384649121#7", "384649121#0", "-195743208#6", "195743208#0", "492489884#0", "195743190#0", "464515259#5", "1207834768#0", "600848485#0", "1157664114#0", "767683114#0", "1027181005#0", "1027181006#0", "-420509471#6"]  # <-- list of edge IDs you want to close 

  

while traci.simulation.getMinExpectedNumber() > 0: 
    step = traci.simulation.getTime() 
    
    # Close edges at t = 200 seconds 
    if step == 200: 
        print(f"Closing edges {closed_edges} at t = {step}")
        for edge in closed_edges: 
            traci.edge.setAllowed(edge, [])  # disallow all vehicles 

    # Reopen edges at t = 2500 seconds 
    if step == 2000: 
        print(f"Reopening edges {closed_edges} at t = {step}") 
        for edge in closed_edges: 
            traci.edge.setAllowed(edge, ["passenger"])
    traci.simulationStep() 

traci.close()