import traci 
 
traci.start(["sumo-gui", "-c", "reversal_config.sumocfg"]) 
 
while traci.simulation.getMinExpectedNumber() > 0: 
    step = traci.simulation.getTime() 
     
    if step == 150: 
        # Reverse one lane to help outbound direction 
        print("Reversing lane 0 of E1 at t=", step) 
        traci.lane.setDisallowed("E1_0", ["passenger"])  # close lane A→B 
        traci.lane.setAllowed("E2_1", ["passenger"])     # open extra lane B→A 
     
    if step == 400: 
        # Restore original directions 
        print("Restoring normal lanes at t=", step) 
        traci.lane.setAllowed("E1_0", ["passenger"]) 
        traci.lane.setDisallowed("E2_1", ["passenger"]) 
 
    traci.simulationStep() 
 
traci.close()