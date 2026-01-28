import csv
import json
import logging

logger = logging.getLogger(__name__)

def export_json(data, path="outputs/result.json"):
    logger.info("Exporting JSON")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def export_csv(data: dict, path="outputs/results.csv"):
    logger.info("Exporting CSV")
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        for k, v in data.items():
            writer.writerow([k,v])