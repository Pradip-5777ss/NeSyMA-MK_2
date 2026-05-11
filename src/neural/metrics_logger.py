import json
import os

def log_metrics(data: dict):
    filepath = "data/evaluation_metrics.json"
    
    # Load existing if available
    metrics = []
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                metrics = json.load(f)
        except json.JSONDecodeError:
            pass
            
    metrics.append(data)
    
    with open(filepath, "w") as f:
        json.dump(metrics, f, indent=4)
