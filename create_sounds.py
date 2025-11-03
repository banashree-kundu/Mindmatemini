import wave
import numpy as np
import os

def create_tone(filename, duration_ms=3000, freq=440):
    # Generate a simple sine wave
    sample_rate = 44100
    t = np.linspace(0, duration_ms/1000, int(sample_rate * duration_ms/1000))
    signal = np.sin(2 * np.pi * freq * t)
    signal = np.int16(signal * 32767)
    
    # Create directory if needed
    os.makedirs("static/sounds", exist_ok=True)
    
    # Save as WAV
    with wave.open(f"static/sounds/{filename}.wav", 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(signal.tobytes())

# Create placeholder sounds
create_tone("soft-chime", duration_ms=500, freq=880)  # Higher pitch for chime
create_tone("ambient-waves", duration_ms=5000, freq=220)  # Lower pitch for waves
create_tone("calm-music", duration_ms=5000, freq=440)  # Middle pitch for music

print("Created placeholder audio files in static/sounds/")