import xml.etree.ElementTree as ET
import sys

def extract_edge_ids(edge_file):
    try:
        tree = ET.parse(edge_file)
        root = tree.getroot()

        # Collect all edge IDs
        edge_ids = []
        for edge in root.findall(".//edge"):
            edge_id = edge.get("id")
            if edge_id:
                edge_ids.append(edge_id)

        # Format as ("E1", "E2", "E3")
        formatted = "(" + ", ".join(f'"{eid}"' for eid in edge_ids) + ")"
        return formatted

    except Exception as e:
        print(f"Error reading {edge_file}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_edge_ids.py <edge_file.edg.xml>")
        sys.exit(1)

    edge_file = sys.argv[1]
    result = extract_edge_ids(edge_file)
    print(result)