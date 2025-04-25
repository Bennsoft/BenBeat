import sounddevice as sd

for i, device in enumerate(sd.query_devices()):
    print(f"{i}: {device['name']} ({device['hostapi']})")
