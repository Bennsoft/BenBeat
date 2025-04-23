from config import Config
import numpy as np
import sounddevice as sd
import pygame
import colorsys
from musical_data import musicalData
from musical_values import MusicalValues
from waveform import Waveform 
import colorsys
from enum import Enum

class State(Enum):
    TICKING = 0
    SPINNING = 1
  

DEVICE_INDEX = 10  # Your Stereo Mix device
SAMPLERATE = 44100
BLOCKSIZE = 1024
md = musicalData(BLOCKSIZE)
dominant_freq = 0.0

def audio_callback(indata, frames, time, status):
    global md
    global dominant_freq
    if status:
        print("Audio stream status:", status)
    # Compute RMS volume
    md.volume = np.linalg.norm(indata) * 10
    mono = np.mean(indata, axis=1)
    fft = np.fft.rfft(mono)
    md.fft_magnitude = np.abs(fft)
    md.dominant_index = np.argmax(fft)
    freqs = np.fft.rfftfreq(len(mono), d=1/SAMPLERATE)
    dominant_freq = freqs[md.dominant_index]



# === Frequency Band Index Ranges ===
# These depend on sample rate and block size:
# e.g., 0–100Hz = bass, 100–1000Hz = mids, 1000Hz+ = treble
def get_band_energy(magnitude, low_bin, high_bin):
    return np.mean(magnitude[low_bin:high_bin]) if high_bin > low_bin else 0

def frequency_to_hue(freq, min_freq=50, max_freq=4000):
    # Clamp frequency range and map to [0, 1]
    freq = max(min(freq, max_freq), min_freq)
    hue = (freq - min_freq) / (max_freq - min_freq)  # Range: 0.0 to 1.0
    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    return int(r * 255), int(g * 255), int(b * 255)

def rotate_points(points, theta, p):
    """
    Rotate an array of 2D points around point p by angle theta (in radians).
    
    :param points: Nx2 NumPy array of 2D points
    :param theta: Angle in radians
    :param p: Tuple or array-like (px, py) - the point to rotate around
    :return: Nx2 NumPy array of rotated points
    """
    # Convert to numpy array
    points = np.asarray(points)
    p = np.asarray(p)

    # Translate points to origin
    translated = points - p

    # Rotation matrix
    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])


    # Apply rotation
    rotated = translated.dot(rotation_matrix.T)

    # Translate back
    result = rotated + p
    return result

def rotate_rgb(rgb, angle_degrees):
    """
    Rotate an RGB color on the color wheel.
    
    :param rgb: Tuple (r, g, b) with values in 0-255
    :param angle_degrees: Angle to rotate hue, in degrees (e.g., 180 = complementary color)
    :return: Rotated RGB tuple (r, g, b), each in 0-255
    """
    # Normalize RGB to [0, 1]
    r, g, b = [x / 255.0 for x in rgb]

    # Convert to HSV
    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    # Rotate hue
    h = (h + angle_degrees / 360.0) % 1.0

    # Convert back to RGB
    r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s, v)

    # Scale back to 0-255 and return as ints
    return tuple(int(round(x * 255)) for x in (r_new, g_new, b_new))

def draw_knot2(surface, center, color, rad, theta, thickness, base_waveform,n):
    trange = np.linspace(rad - thickness // 2, rad + thickness // 2, thickness)
    center = np.array(center)

    colrot=1
    for r in trange:
        col = rotate_rgb(color, r * colrot)

        # Scale base waveform
        points = (base_waveform * r + center)[:n]

        # Rotate all points around center
        points = rotate_points(points, theta, center)

        # Draw
        pygame.draw.lines(surface, col, False, points, 2)



def main():
    config = Config()
    waves = Waveform(config.points_num)
    knotform = None
    animation_phase = 0.0
    spin_countdown = 0

    pygame.init()
    WIDTH, HEIGHT = 800, 800
    SENSITIVITY = 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Real-Time Music Visualizer")
    clock = pygame.time.Clock()


    # === Audio Volume Holder ===
   
    num_points = 500
    mv = MusicalValues()
    complete_loops = 0


    # === Start Audio Stream ===
    stream = sd.InputStream(
        callback=audio_callback,
        channels=2,
        samplerate=SAMPLERATE,
        blocksize=BLOCKSIZE,
        device=DEVICE_INDEX
    )
    stream.start()
    smoothed_freq = 0.0
    smoothed_bass = 0.0
    smoothed_mids = 0.0
    smoothed_treble = 0.0
    
    state = State.TICKING
    # === Main Loop ===
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill((15, 15, 40))

        bass = get_band_energy(md.fft_magnitude, 1, 10)
        mids = get_band_energy(md.fft_magnitude, 10, 100)
        treble = get_band_energy(md.fft_magnitude, 100, 1000)
        mv.bass = bass
        mv.mids = mids  
        mv.treble = treble
        mv.frequency = dominant_freq
    
        smoothed_freq = (1 - config.smoothing_alpha) * smoothed_freq + config.smoothing_alpha * mv.frequency
        smoothed_bass = (1 - config.smoothing_alpha) * smoothed_bass + config.smoothing_alpha * mv.bass
        smoothed_mids = (1 - config.smoothing_alpha) * smoothed_mids + config.smoothing_alpha * mv.mids
        smoothed_treble = (1 - config.smoothing_alpha) * smoothed_treble + config.smoothing_alpha * mv.treble

        print(f"          freq{mv.frequency:.2f}  Hz, Bass: {mv.bass:.2f}, Mids: {mv.mids:.2f}, Treble: {mv.treble:.2f}")
        print(f"Smoooooth freq{smoothed_freq:.2f} Hz, Bass: {smoothed_bass:.2f}, Mids: {smoothed_mids:.2f}, Treble: {smoothed_treble:.2f}")
        circle_color = frequency_to_hue(smoothed_freq)

        t2 = int(animation_phase) 

        if state == State.TICKING:
            if t2 == 0:
                 w1 = np.random.randint(0,waves.get_waveformCount()-1)
                 w2 = np.random.randint(0,waves.get_waveformCount()-1)
                 if (w1==w2):
                    knotform = waves.get_waveform_by_index(w1)
                 else:
                    blend = np.random.uniform(0,1)
                    name1 = waves.get_waveform_name(w1)
                    name2 = waves.get_waveform_name(w2)
                    knotform = waves.get_waveform_blend(name1,name2,blend)

            elif t2 == num_points-1:
                #complete loop
                complete_loops += 1
                
                state = State.SPINNING
                spin_countdown = config.spins
                animation_phase = 0.0

        elif state == State.SPINNING:
            if t2 == config.points_num-1:
                # Spin complete
                spin_countdown -= 1
                animation_phase = 0.0 
                complete_loops += 1  
                if spin_countdown == 0:
                    state = State.TICKING

        pygame.display.set_caption(f"Real-Time Music Visualizer - Loops: {complete_loops}")              
        animation_speed =  smoothed_mids  # adjust constants to taste
        animation_phase += animation_speed
        knot_rad =  config.radius+(smoothed_bass*config.radband)
        theta = np.radians(animation_phase)
        thickness = (int)(config.thickness+(smoothed_treble*config.thickband))
        print(f"{t2} knotrad {knot_rad} thickness: {thickness}")
       
        timeval = t2 if state == State.TICKING else num_points-1   
        if timeval>2:
            draw_knot2(screen,(WIDTH/2,HEIGHT/2), circle_color,knot_rad,theta,thickness,knotform,timeval)

        pygame.display.flip()
        clock.tick(60)


    # === Cleanup ===
    stream.stop()
    stream.close()
    pygame.quit()







if __name__ == "__main__":
    main()