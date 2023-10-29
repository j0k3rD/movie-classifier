import joblib
import json
import os

def convert_model_to_json():
    # Load the model from the file
    logistic_model = joblib.load('main/models/output_directory_regression/logistic_regression.pkl')

    # Check if the model.json is already created
    if not os.path.exists('main/models/output_directory_regression/model.json'):
        # Convert the model to a format that can be serialized to JSON
        logistic_model_json = logistic_model.get_params()

        # Save the converted JSON model in a file
        with open('main/models/output_directory_regression/model.json', 'w') as json_file:
            json.dump(logistic_model_json, json_file)