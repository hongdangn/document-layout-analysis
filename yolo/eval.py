from ultralytics import YOLO
from typing import List
import argparse

def evaluate(saved_model: str, yaml_dataset: str):
    model = YOLO(saved_model)
    results = model.val(data = yaml_dataset)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--saved_model",
                        required=True,
                        help="Saved model link")
    
    parser.add_argument("--yaml_dataset",
                        required=True,
                        help="Yaml file of the dataset")
    
    args = parser.parse_args()
    evaluate(args.saved_model, args.yaml_dataset)