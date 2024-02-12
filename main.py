import requests
from datetime import datetime
import os

#   Nutritionix API
APP_ID = os.environ["nutritionix_APP_ID"]
API_KEY = os.environ["nutritionix_API_KEY"]

nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_text = input("Tell me which exercise you did: ")
#   Weight in kg
WEIGHT = 55
#   Height in cm
HEIGHT = 167.64
AGE = 30

exercise_params = {
    "query": exercise_text,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,
}

headers = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY,
}

exercise_response = requests.post(url=nutritionix_endpoint, json=exercise_params, headers=headers)
exercise_response.raise_for_status()
result = exercise_response.json()
print(result)

#   Sheety API
sheety_endpoint = os.environ["sheety_endpoint"]
SHEETY_TOKEN = os.environ["SHEETY_TOKEN"]

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

sheety_headers = {
    "Authorization": f'Bearer {os.environ["SHEETY_TOKEN"]}'
}

for exercise in result["exercises"]:
    sheety_inputs = {
        "sheet1": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheety_response = requests.post(url=sheety_endpoint, json=sheety_inputs, headers=sheety_headers)
    sheety_response.raise_for_status()
    print(sheety_response.text)
