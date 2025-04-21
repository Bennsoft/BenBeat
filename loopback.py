import numpy as np
import sounddevice as sd
import pygame
import colorsys
from MusicalData import musicalData
from GeometricObjects.spiral import Spiral

animation_phase = 0.0
smoothing_factor = 0.05

# === Audio Settings ===
DEVICE_INDEX = 10  # Your Stereo Mix device
SAMPLERATE = 44100
BLOCKSIZE = 1024

spirals = list()

iradius = 200
ithickness = 2
radband = 60
thickband = 20

midmax =1e-10
bassmax =1e-10
trebmax =1e-10
# === Pygame Setup ===
pygame.init()
WIDTH, HEIGHT = 1000, 1000
SENSITIVITY = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Real-Time Music Visualizer")
clock = pygame.time.Clock()

# === Audio Volume Holder ===
volume = 0.0
dominant_freq = 0.0
md = musicalData(BLOCKSIZE)

num_points = 500

dots = np.linspace(0, 2 * np.pi, num_points)
base_waveform = np.array([
    [np.sin(7 * t), np.cos(5 * t + np.pi / 2)]
    for t in dots
])

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

def draw_spiral(surface, center, time_value, color, a=0, b=2, num_points=400, rotation_speed=1.0):
    points = []
    max_theta = 6 * np.pi
    for i in range(num_points):
        theta = i * (max_theta / num_points)
        r = a + b * theta
        x = r * np.cos(theta + time_value * rotation_speed)
        y = r * np.sin(theta + time_value * rotation_speed)
        points.append((center[0] + x, center[1] + y))
    if len(points) > 1:
        pygame.draw.lines(surface, color, False, points, 2)

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

import colorsys

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

    for r in trange:
        col = rotate_rgb(color, r * 10)

        # Scale base waveform
        points = (base_waveform * r + center)[:n]

        # Rotate all points around center
        points = rotate_points(points, theta, center)

        # Draw
        pygame.draw.lines(surface, col, False, points, 2)


def draw_knot(surface,center,color,rad,theta,thickness,num_points=500):
    trange = np.linspace(rad-thickness//2, rad+thickness//2, thickness)
    for r in trange:
        points = []
        col = rotate_rgb( color, r*10)
        dots = np.linspace(0, 2 * np.pi, num_points)
        for t in dots:
            x = np.sin(7 * t)*r
            y = ( np.cos(5 * t+np.pi/2))*r      
            points.append((center[0] + x, center[1] + y))

        if len(points) > 1:
            points2 = rotate_points(points, theta, center)
            pygame.draw.lines(surface, col, False, points2, 2)
        
   



# === Start Audio Stream ===
stream = sd.InputStream(
    callback=audio_callback,
    channels=2,
    samplerate=SAMPLERATE,
    blocksize=BLOCKSIZE,
    device=DEVICE_INDEX
)
stream.start()

tick = 1
# === Main Loop ===
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((15, 15, 40))
    
   
   
    circle_color = frequency_to_hue(dominant_freq)

    bass = get_band_energy(md.fft_magnitude, 1, 10)
    mids = get_band_energy(md.fft_magnitude, 10, 100)
    treble = get_band_energy(md.fft_magnitude, 100, 1000)
    if bass > bassmax:
        bassmax = bass
    if mids > midmax:
        midmax = mids   
    if treble > trebmax:
        trebmax = treble
    # Normalize values to 0-1 range 
    bass = bass / bassmax
    mids = mids / midmax
    treble = treble / trebmax
    
    animation_speed = 0.05 + 0.02 * mids  # adjust constants to taste
    animation_phase += animation_speed
    t = animation_phase
    t2 = int(t*5) % num_points

    #print(f"t {t} bass {bass}- mids {mids} - treble {treble} dominant freq {dominant_freq} ")
    # You can plug in volume or dominant_freq to modulate!
    rotation_speed = dominant_freq / 1000  # Higher pitch = faster spin
    tightness = 1 + bass * 5               # Spiral tightens with bass

    knot_rad =  iradius+(bass*radband)
    theta = np.radians(t * 10)
    thickness = (int)(ithickness+(bass*thickband))
    print(f"thickness {thickness} knot_rad {knot_rad} theta {theta}")
   

    if t2>2:
        draw_knot2(screen,(WIDTH/2,HEIGHT/2), circle_color,knot_rad,theta,thickness,base_waveform,t2)

    pygame.display.flip()
    clock.tick(60)
    tick += 1
    

# === Cleanup ===
stream.stop()
stream.close()
pygame.quit()

