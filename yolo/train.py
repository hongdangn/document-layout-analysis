from ultralytics import YOLO
from typing import List
import argparse

def train(saved_model: str, 
          yaml_dataset: str,
          num_epochs: int = 10):
    
    model = YOLO(saved_model)
    results = model.train(data = yaml_dataset, epochs = num_epochs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--saved_model",
                        required=True,
                        help="Saved model link")
    
    parser.add_argument("--yaml_dataset",
                        required=True,
                        help="Yaml file of the dataset")
    
    parser.add_argument("--num_epochs",
                        required=True)
    
    args = parser.parse_args()
    train(args.saved_model, args.yaml_dataset)