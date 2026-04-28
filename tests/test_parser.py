import os
import sys

# Add src to the python path to import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser.core_parser import LegacyCodeParser
from src.parser.exporter import DataExporter

def main():
    parser = LegacyCodeParser()
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'exports')
    
    scripts = ['calc_1.py', 'calc_2.py', 'calc_3.py']
    
    for script in scripts:
        print(f"\\n{'='*50}")
        print(f"Processing {script}...")
        print(f"{'='*50}")
        
        script_path = os.path.join(data_dir, script)
        with open(script_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
            
        tree = parser.parse(source_code)
        
        print("--- AST Visualization ---")
        parser.visualize(tree.root_node)
        print("-------------------------\\n")
        
        logic_data = parser.extract_logic(tree.root_node, source_code.encode('utf-8'))
        
        output_path = os.path.join(output_dir, f"{script.split('.')[0]}_ast.json")
        DataExporter.export_to_json(logic_data, output_path)
        
        print(f"✅ Successfully parsed and exported {script}")

if __name__ == "__main__":
    main()
