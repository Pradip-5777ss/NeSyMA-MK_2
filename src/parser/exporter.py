import json
import os

class DataExporter:
    @staticmethod
    def export_to_json(logic_data: dict, output_path: str):
        """
        7. Data Export Bridge (for Phase 2)
        Converts the parsed data into a structured .json file.
        """
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(logic_data, f, indent=4)
        print(f"Data successfully exported to {output_path}")

    @staticmethod
    def export_to_dict(logic_data: dict) -> dict:
        """
        Returns the data as a Python Dictionary (it's already a dict, just for bridge API consistency).
        """
        return logic_data
