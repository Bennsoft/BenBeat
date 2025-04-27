from config import Config
import numpy as np
import sounddevice as sd
import pygame
import colorsys
from musical_data import musicalData
from musical_values import MusicalValues
from waveform import Waveform 
from numwave import Numwave
import colorsys
from enum import Enum
import math
from visual_mapping import VisualMapping

class State(Enum):
    TICKING = 0
    SPINNING = 1
    PULSE = 2
    CONNCENTIC = 3
  

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

def draw_knot2(surface, center, color, rad, theta, thickness, base_waveform,n,colrot = 10):
    trange = np.linspace(rad - thickness // 2, rad + thickness // 2, thickness)
    center = np.array(center)

    for r in trange:
        col = rotate_rgb(color, r * colrot)

        # Scale base waveform
        points = (base_waveform * r + center)[:n]

        # Rotate all points around center
        points = rotate_points(points, theta, center)

        # Draw
        pygame.draw.lines(surface, col, False, points, 2)


def unwrap_angle(angle_rad):
    full_turn = 2 * math.pi
    loops = int(angle_rad // full_turn)        # number of full 2π loops
    current_angle = angle_rad % full_turn      # remainder within current loop
    return loops, current_angle


mapping_a = VisualMapping('frequency', scale=5.0, offset=2.0, smoothing_alpha=0.05)
mapping_b = VisualMapping('treble', scale=5.0, offset=1.0, smoothing_alpha=0.05)
mapping_c = VisualMapping('mids', scale=5.0, offset=1.0, smoothing_alpha=0.05)
mapping_knot_radius = VisualMapping('bass', scale=400.0, offset=100.0, smoothing_alpha=0.05)
mapping_thickness = VisualMapping('treble', scale=30.0, offset=2.0, smoothing_alpha=0.1)
mapping_tick_speed = VisualMapping('mids', scale=10.0, offset=0.0, smoothing_alpha=0.05)


def main():
    config = Config()
    waves = Waveform(config.points_num)
    numwave = None
    knotform = None
    tick_phase = 0
    rotation_angle =0
    tick_speed = 0
    angular_speed = 0
    rotation_target = 0
    display_text = ""
    a=0
    b=0
    c=0
    pulse_taget = 0
    firstpass = False
    smoothing_alpha = 0.05
    pygame.init()
    WIDTH, HEIGHT = 1000, 800
    SENSITIVITY = 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Real-Time Music Visualizer")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)  # None = default font, 36 = size


    # === Audio Volume Holder ===
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
    smoothed_freq = 0.5
    smoothed_bass = 0.5
    smoothed_mids = 0.5
    smoothed_treble = 0.5
    
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
    
        if state == State.PULSE:
            smoothing_alpha = config.smoothing_alpha_pulse
        else:
            smoothing_alpha = config.smoothing_alpha

        smoothed_freq = (1 - config.smoothing_alpha) * smoothed_freq + smoothing_alpha * mv.frequency
        smoothed_bass = (1 - config.smoothing_alpha) * smoothed_bass + smoothing_alpha * mv.bass
        smoothed_mids = (1 - config.smoothing_alpha) * smoothed_mids + smoothing_alpha * mv.mids
        smoothed_treble = (1 - config.smoothing_alpha) * smoothed_treble + smoothing_alpha * mv.treble

  #      print(f"          freq{mv.frequency:.2f}  Hz, Bass: {mv.bass:.2f}, Mids: {mv.mids:.2f}, Treble: {mv.treble:.2f}")
   #     print(f"Smoooooth freq{smoothed_freq:.2f} Hz, Bass: {smoothed_bass:.2f}, Mids: {smoothed_mids:.2f}, Treble: {smoothed_treble:.2f}")
        circle_color = smoothed_bass*255, smoothed_mids*255, smoothed_treble*255
        if state == State.TICKING or state == State.SPINNING:
            t = int(tick_phase) % config.points_num
            tick_speed = mapping_tick_speed.update(mv)
            tick_phase+=tick_speed
            angular_speed = smoothed_bass*2
            rotation_angle += angular_speed

            
            complete_loops,current_rad_angle = unwrap_angle(np.radians(rotation_angle))
            if (state==State.TICKING or state == State.SPINNING):
                knot_rad = mapping_knot_radius.update(mv)

            if state == State.TICKING:
                if t == 0:
                    choices=[3,4,5,6]
                    wavepick = np.random.choice(choices)
                    numwave = waves.get_waveform_by_index(wavepick)
                    display_text = f" {waves.get_waveform_name(wavepick)} a {a} b {b} c{c}"
                    a=numwave.get_a(np.random.uniform(0,1))
                    b=numwave.get_b(np.random.uniform(0,1))
                    c=numwave.get_c(np.random.uniform(0,1))
                    knotform = numwave.get_linspace(a,b,c)
                    text = font.render(display_text, True, (255, 255, 255))
                    text_rect = text.get_rect(topleft=(10, 10)) 

                elif t == config.__points_num__-1:                
                    state = State.SPINNING
                    rotation_target = rotation_angle + config.spins*360
            elif state == State.SPINNING:
                    if rotation_angle >= rotation_target:
                        state = State.PULSE
                        pulse_taget = pygame.time.get_ticks() + 20000

            thickness = (int)(config.thickness+(smoothed_treble*config.thickband))
            timeval = t if state == State.TICKING else config.__points_num__-1   
            

        elif state == State.PULSE:                
           a = mapping_a.update(mv)
           b = mapping_b.update(mv)
           c = mapping_c.update(mv)

           knotform = numwave.get_linspace(a,b,c)
           timeval = config.__points_num__-1
           current_time = pygame.time.get_ticks()
           
           if current_time >= pulse_taget:
                state = State.TICKING
                tick_phase = 0
                rotation_angle = 0
                complete_loops = 0
           else:
                display_text = f"Pulsing a {a} b {b} c {c}" 
                text = font.render(display_text, True, (255, 255, 255))
                text_rect = text.get_rect(topleft=(10, 10)) 

        if numwave.hollow:
            if timeval>2:
                rads = np.linspace(1,knot_rad,4)
                for r in rads:
                    draw_knot2(screen,(WIDTH/2,HEIGHT/2), circle_color,r,current_rad_angle,thickness,knotform,timeval) 

        else:
            if timeval>2:
                draw_knot2(screen,(WIDTH/2,HEIGHT/2), circle_color,knot_rad,current_rad_angle,thickness,knotform,timeval) 
        pygame.display.set_caption(f"Real-Time Music Visualizer - Loops: {complete_loops}")              
       
       
        screen.blit(text,text_rect)
        pygame.display.flip()
        clock.tick(60)


    # === Cleanup ===
    stream.stop()
    stream.close()
    pygame.quit()







if __name__ == "__main__":
    main()