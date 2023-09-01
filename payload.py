import requests
def send_to_ubidots(payload):
    DEVICE_LABEL =  "bme680"
    url = "https://industrial.api.ubidots.com/api/v1.6/devices/{}".format(DEVICE_LABEL)
    headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": "BBFF-0gTo987xsbB0WFQ8odR1qqvK7YEFWr"
            # "X-Auth-Token" : "BBFF-nrtpAC0FQHGzSdg1aeI7bMyr5r6L55"
        }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Data berhasil diunggah ke Ubidots")
    else:
        print("Gagal mengunggah data ke Ubidots. Kode status:", response.status_code)


