import yaml
import os

with open("selectors.yml", "r", encoding="utf-8") as f:
        SELECTORS = yaml.safe_load(f)   
        
with open("variables.yml", "r", encoding="utf-8") as f:
        VARIABLES = yaml.safe_load(f)