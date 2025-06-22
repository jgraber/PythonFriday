import pyaudio

# Initialize PyAudio
p = pyaudio.PyAudio()

# List all devices
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"Device {i}: {info['name']} [{info['maxInputChannels']} in, {info['maxOutputChannels']} out]")

# Optionally, get default input device info
default_input = p.get_default_input_device_info()
print()
print("Default input device:")
print(f"  Name: {default_input['name']}")
print(f"  Max input channels: {default_input['maxInputChannels']}")

p.terminate()