import requests, json
import numpy as np
from datetime import date
from datetime import timedelta


def get_name(user_auth):
    fitbit_web_api_request_url = "https://api.fitbit.com/1/user/-/profile.json"
    resp = requests.get(fitbit_web_api_request_url, headers=user_auth).json()
    return resp['user']['fullName']
    

def get_heartrate(user_auth):
    fitbit_web_api_request_url = "https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1sec.json"
    resp = requests.get(fitbit_web_api_request_url, headers=user_auth).json()
    return resp['activities-heart-intraday']['dataset'][-1]


def get_steps(user_auth):
    fitbit_web_api_request_url = "https://api.fitbit.com/1/user/-/activities/steps/date/today/1d.json"
    resp = requests.get(fitbit_web_api_request_url, headers=user_auth).json()
    return resp['activities-steps'][0]['value']


def get_sleep(user_auth):
    # Get yesterday's date
    today = date.today()
    yesterday = today - timedelta(days = 1)
    
    fitbit_web_api_request_url = "https://api.fitbit.com/1.2/user/-/sleep/date/" + str(yesterday) + ".json"
    resp = requests.get(fitbit_web_api_request_url, headers=user_auth).json()
    return resp['summary']['totalMinutesAsleep']


def get_activeness(user_auth):
    fitbit_web_api_request_url = "https://api.fitbit.com/1/user/-/activities/minutesSedentary/date/today/1d.json"
    resp_sedentary = requests.get(fitbit_web_api_request_url, headers=user_auth).json()
    
    fitbit_web_api_request_url = "https://api.fitbit.com/1/user/-/activities/minutesLightlyActive/date/today/1d.json"
    resp_light_active = requests.get(fitbit_web_api_request_url, headers=user_auth).json()
    
    fitbit_web_api_request_url = "https://api.fitbit.com/1/user/-/activities/minutesFairlyActive/date/today/1d.json"
    resp_fairly_active = requests.get(fitbit_web_api_request_url, headers=user_auth).json()
        
    fitbit_web_api_request_url = "https://api.fitbit.com/1/user/-/activities/minutesVeryActive/date/today/1d.json"
    resp_highly_active = requests.get(fitbit_web_api_request_url, headers=user_auth).json()
    
    return int(resp_sedentary['activities-minutesSedentary'][0]['value']), int(resp_light_active['activities-minutesLightlyActive'][0]['value']),\
           int(resp_fairly_active['activities-minutesFairlyActive'][0]['value']), int(resp_highly_active['activities-minutesVeryActive'][0]['value'])
    

if __name__ == "__main__":
    user_auth = {'Authorization':'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhRTkQiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBybnV0IHJwcm8gcnNsZSByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkyMzIyMzQ0LCJpYXQiOjE2NjA3ODYzNDR9.-kAqRq3x5D5J0nCgzOm-2ATMbz9e7EZYXUiitEt6h4k'}
    
    print(get_name(user_auth))
    
    recent_heartrate = get_heartrate(user_auth)
    print(f"Your most recent heart rate recorded at {recent_heartrate['time']} is {recent_heartrate['value']} beats per minute")
    
    num_steps = get_steps(user_auth)
    print(f"Your total step count today is {num_steps} steps")
    
    sedentary, light_active, fair_active, high_active = get_activeness(user_auth)
    active = light_active + fair_active + high_active
    print(f"Today you were sedentary for {int(np.floor(sedentary/60))} hours and {sedentary%60} minutes and active for {int(np.floor(active/60))} hours and {active%60} minutes with {int(np.floor(high_active/60))} hours and {high_active%60} minutes in the very high activity zone.")
    
    sleep_time = get_sleep(user_auth)
    print(f"You slept for {int(np.floor(sleep_time/60))} hours and {sleep_time%60} minutes last night")
