from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from PIL import Image

# 1. Setup paths
current_dir = Path(__file__).resolve().parent
img1_path = current_dir / "img1.png"
img2_path = current_dir / "img2.png"

if not img1_path.exists() or not img2_path.exists():
    raise FileNotFoundError(
        f"Required images ('img.png' and 'img2.png') not found in: {current_dir}"
    )

# 2. Advanced Loading & Auto-Resizing using Pillow (PIL)
print("Loading and aligning images...")
raw_pil1 = Image.open(img1_path)
raw_pil2 = Image.open(img2_path)

# Compare sizes (width, height)
size1 = raw_pil1.size
size2 = raw_pil2.size

processed_pil1 = raw_pil1
processed_pil2 = raw_pil2

if size1 != size2:
    print(f"Size mismatch detected: Img1={size1}, Img2={size2}")
    
    # Calculate total pixel area to find the largest image
    area1 = size1[0] * size1[1]
    area2 = size2[0] * size2[1]
    
    if area1 >= area2:
        print(f"Stretching Img2 ({size2}) to match Img1 ({size1})...")
        # Resize Img2 using Lanczos interpolation for high-quality stretching
        processed_pil2 = raw_pil2.resize(size1, Image.Resampling.LANCZOS)
        target_size_label = f"Match Img1 ({size1[0]}x{size1[1]})"
    else:
        print(f"Stretching Img1 ({size1}) to match Img2 ({size2})...")
        processed_pil1 = raw_pil1.resize(size2, Image.Resampling.LANCZOS)
        processed_pil2 = raw_pil2 # img2 is already the correct size
        target_size_label = f"Match Img2 ({size2[0]}x{size2[1]})"
else:
    print(f"Images are already aligned ({size1[0]}x{size1[1]}).")
    target_size_label = f"{size1[0]}x{size1[1]}"

# 3. Convert to Numpy arrays and normalize to 0.0 - 1.0
# We use standard Matplotlib color conversion to ensure RGB format
img1 = np.array(processed_pil1.convert('RGB')).astype(float)
img2 = np.array(processed_pil2.convert('RGB')).astype(float)

# Scale pixel values from [0, 255] down to [0.0, 1.0] for math blending
img1 /= 255.0
img2 /= 255.0


# 4. Set up the Interface
fig, ax = plt.subplots(figsize=(10, 7))
# Adjust margins to leave space for slider at the bottom
plt.subplots_adjust(bottom=0.2, left=0.05, right=0.95, top=0.93)
fig.canvas.manager.set_window_title('Screenshot Stretcher & Mixer')

# Initial blend (50/50 mix)
initial_alpha = 0.5
initial_mix = (img1 * initial_alpha) + (img2 * (1.0 - initial_alpha))

# Display the mix
# Forced limits prevent weird color shifting during blending
im_display = ax.imshow(initial_mix, vmin=0, vmax=1)
ax.axis('off')  # Hide axis rulers

# Set initial title showing stretch info
ax.set_title(f"Mixing at 50% | Base Resolution: {target_size_label}")

# 5. Create the Slider Widget
ax_slider = plt.axes([0.20, 0.08, 0.60, 0.03])  # Position: [left, bottom, width, height]
mix_slider = Slider(
    ax=ax_slider,
    label='Mixer: Img2 <-> Img1',
    valmin=0.0,
    valmax=1.0,
    valinit=initial_alpha,
    color='#FF5733' # Distinct orange color
)

# 6. Interactivity Update Logic
def update_mix(alpha):
    """
    Computes new image: (img1 * alpha) + (img2 * (1.0 - alpha))
    Value 1.0 = Pure Img1
    Value 0.0 = Pure Img2
    """
    beta = 1.0 - alpha
    new_blend = (img1 * alpha) + (img2 * beta)
    
    # Update the data currently on screen
    im_display.set_data(new_blend)
    ax.set_title(f"Mixing: Img1({alpha*100:.0f}%) / Img2({beta*100:.0f}%)")
    
    # Fast redraw
    fig.canvas.draw_idle()

# Connect the update function to the slider movement
mix_slider.on_changed(update_mix)

print("\nReady! Use the orange slider to compare the stretched screenshots.")
plt.show()