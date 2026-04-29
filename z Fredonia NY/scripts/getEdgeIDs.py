import sumolib
import csv
import os

def export_edges_to_csv(net_file, output_csv):
    try:
        # Load the network
        net = sumolib.net.readNet(net_file)
        data_to_write = []
        
        for edge in net.getEdges():
            eid = str(edge.getID())
            
            # Filter out internal junction edges
            if not eid.startswith(':'):
                street_name = "Unnamed Road"
                
                # Method 1: Try the standard name attribute
                if hasattr(edge, 'getName') and edge.getName():
                    street_name = edge.getName()
                
                # Method 2: Try to pull from the raw XML attribute dictionary
                # Most versions of sumolib store attributes in a dict called 'attr'
                elif hasattr(edge, 'attr') and 'name' in edge.attr:
                    street_name = edge.attr['name']
                
                # Method 3: Check if it's stored in a private attribute (older versions)
                elif hasattr(edge, '_Edge__attr') and 'name' in edge._Edge__attr:
                    street_name = edge._Edge__attr['name']
                
                data_to_write.append([eid, street_name])

        # Write to CSV
        with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Edge_ID', 'Street_Name']) 
            writer.writerows(data_to_write)
            
        return len(data_to_write)

    except Exception as e:
        print(f"Error: {e}")
        return 0

if __name__ == "__main__":
    PATH_TO_NET = r"C:\Users\becca\Sumo\Fredonia NY\osm.net.xml.gz"
    OUTPUT_FILE = "fredonia_street_list.csv"

    count = export_edges_to_csv(PATH_TO_NET, OUTPUT_FILE)
    
    if count > 0:
        print(f"Success! Exported {count} edges to {os.path.abspath(OUTPUT_FILE)}")
    else:
        print("Export failed.")