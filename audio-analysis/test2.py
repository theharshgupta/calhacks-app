import requests
api_key = 'kRG6NgjvEMrRjrKwGItRSQR9pSybdkk2'
url = "https://proxy.api.deepaffects.com/audio/generic/api/v2/sync/recognise_emotion?apikey=kRG6NgjvEMrRjrKwGItRSQR9pSybdkk2"
l = requests.post(url=url)
print(l)