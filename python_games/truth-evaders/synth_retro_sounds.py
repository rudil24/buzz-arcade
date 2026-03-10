import wave
import struct
import math
import random
import os

def synth(filename, func, duration, rate=44100):
    print(f"Synthesizing {filename}...")
    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(rate)
        # Generate frames
        frames = b''
        for i in range(int(rate * duration)):
            t = float(i) / rate
            val = func(t)
            # clamp and scale
            v = int(max(-1, min(1, val)) * 32767)
            frames += struct.pack('<h', v)
        f.writeframes(frames)
            
# shot: fast descending square wave with slight noise
def shot(t):
    freq = max(100, 800 - 4000*t)
    sq = math.copysign(1, math.sin(2 * math.pi * freq * t))
    env = max(0, 1.0 - t*4)
    return (sq * 0.4 + (random.random()*2-1)*0.1) * env

# rip/hit: burst of white noise
def rip(t):
    env = max(0, 1.0 - t*6)
    return (random.random() * 2 - 1) * env * 0.7

# march: low electronic blip
def march(t):
    freq = max(40, 150 - 500*t)
    env = max(0, 1.0 - t*12)
    return math.sin(2 * math.pi * freq * t) * env

def boss_hit(t):
    # triple burst of the "shot" sound but much higher pitched
    local_t = t % 0.2
    
    freq = max(400, 1800 - 6000*local_t)
    sq = math.copysign(1, math.sin(2 * math.pi * freq * local_t))
    
    env = 0.0
    if 0 < t < 0.15: env = 1.0 - (local_t/0.15)
    elif 0.2 < t < 0.35: env = 1.0 - (local_t/0.15)
    elif 0.4 < t < 0.55: env = 1.0 - (local_t/0.15)
    
    return (sq * 0.4 + (random.random()*2-1)*0.1) * env

if __name__ == "__main__":
    os.makedirs("/Users/rudil24/Documents/webdev/buzz-arcade/python_games/truth-evaders/assets/sounds", exist_ok=True)
    synth("/Users/rudil24/Documents/webdev/buzz-arcade/python_games/truth-evaders/assets/sounds/shot.wav", shot, 0.3)
    synth("/Users/rudil24/Documents/webdev/buzz-arcade/python_games/truth-evaders/assets/sounds/rip.wav", rip, 0.2)
    synth("/Users/rudil24/Documents/webdev/buzz-arcade/python_games/truth-evaders/assets/sounds/march.wav", march, 0.1)
    synth("/Users/rudil24/Documents/webdev/buzz-arcade/python_games/truth-evaders/assets/sounds/boss_hit.wav", boss_hit, 0.6)
    print("Done!")
