import urllib.request, time
while True:
    try:
        urllib.request.urlopen("https://web-production-6ceec.up.railway.app/")
        print("Server alive!")
    except Exception as e:
        print(f"Failed: {e}")
    time.sleep(300)
