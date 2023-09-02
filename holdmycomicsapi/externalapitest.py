import requests

# api_url = "https://metron.cloud/api/publisher/"
# response = requests.get(api_url, auth=('SeaForeEx', 'TickTockGoesTheMelody'), timeout=60)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     data = response.json()
#     print(data)
# else:
#     print("Request was not successful. Status code:", response.status_code)

api_url = "https://metron.cloud/api/issue/?store_date=2023-09-05"
response = requests.get(api_url, auth=('SeaForeEx', 'TickTockGoesTheMelody'), timeout=60)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Request was not successful. Status code:", response.status_code)
