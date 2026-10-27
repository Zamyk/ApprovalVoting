from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.widgets import Slider
from PIL import Image

HERE = Path(__file__).resolve().parent
PLOTS = HERE / "plots"
ORIGINALS = HERE / "original_plots"
RESULTS = HERE / "results"

CHOICES = {
    "1": {
        "label": "triangle",
        "csv": RESULTS / "results_triangle_iterations.csv",
        "original": ORIGINALS / "original_triangle.png",
        "bare_save": PLOTS / "triangle_seq_iterations_bare.png",
    },
    "2": {
        "label": "gaussian",
        "csv": RESULTS / "results_gaussian_iterations.csv",
        "original": ORIGINALS / "original_gaussian.png",
        "bare_save": PLOTS / "gaussian_seq_iterations_bare.png",
    },
}


def ask_choice():
    print("Compare seqAV min-max iterations vs original (plot area only).\n")
    for key, item in CHOICES.items():
        print(f"  {key}) {item['label']}")
    print()
    while True:
        pick = input("Enter 1 or 2: ").strip()
        if pick in CHOICES:
            return CHOICES[pick]
        print("Invalid choice, try again.")


def resolve_image(path):
    if path.exists():
        return path
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        alt = path.with_suffix(ext)
        if alt.exists():
            return alt
    raise FileNotFoundError(
        f"Missing original screenshot: {path}\n"
        f"Put a crop of just the plot area in {ORIGINALS}/"
    )


def render_bare(csv_path, save=None):
    """Draw curves only; save/export the axes rectangle (no title/labels/legend/ticks)."""
    grouped = pd.read_csv(csv_path)
    fig, ax = plt.subplots(figsize=(8, 4), dpi=150)
    for d_val in grouped["d"].unique():
        subset = grouped[grouped["d"] == d_val].sort_values("alpha")
        line, = ax.plot(subset["alpha"], subset["mean"])
        ax.fill_between(
            subset["alpha"],
            subset["min"].clip(lower=0, upper=1),
            subset["max"].clip(lower=0, upper=1),
            color=line.get_color(),
            alpha=0.15,
        )
    ax.axvline(x=0.5, color="black", linestyle="--")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("")
    fig.canvas.draw()
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches=bbox, pad_inches=0)
    if save is not None:
        Path(save).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save, dpi=150, bbox_inches=bbox, pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGB")


def load_aligned(pil_ours, pil_original):
    size1, size2 = pil_ours.size, pil_original.size
    if size1 == size2:
        print(f"Already aligned ({size1[0]}x{size1[1]}).")
        target = size1
    elif size1[0] * size1[1] >= size2[0] * size2[1]:
        print(f"Stretching original {size2} -> {size1}")
        pil_original = pil_original.resize(size1, Image.Resampling.LANCZOS)
        target = size1
    else:
        print(f"Stretching ours {size1} -> {size2}")
        pil_ours = pil_ours.resize(size2, Image.Resampling.LANCZOS)
        target = size2
    img1 = np.array(pil_ours, dtype=float) / 255.0
    img2 = np.array(pil_original, dtype=float) / 255.0
    return img1, img2, target


def show_mixer(img_ours, img_original, title, size_label):
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.subplots_adjust(bottom=0.2, left=0.05, right=0.95, top=0.93)
    fig.canvas.manager.set_window_title(title)

    alpha0 = 0.5
    im = ax.imshow(img_ours * alpha0 + img_original * (1.0 - alpha0), vmin=0, vmax=1)
    ax.axis("off")
    ax.set_title(f"{title} | 50/50 | {size_label[0]}x{size_label[1]}")

    ax_slider = plt.axes([0.20, 0.08, 0.60, 0.03])
    slider = Slider(
        ax=ax_slider,
        label="original <-> ours",
        valmin=0.0,
        valmax=1.0,
        valinit=alpha0,
        color="#FF5733",
    )

    def update(alpha):
        im.set_data(img_ours * alpha + img_original * (1.0 - alpha))
        ax.set_title(
            f"{title} | ours {alpha * 100:.0f}% / original {(1 - alpha) * 100:.0f}% | "
            f"{size_label[0]}x{size_label[1]}"
        )
        fig.canvas.draw_idle()

    slider.on_changed(update)
    print("Slider: left = original screenshot, right = our bare plot area.")
    plt.show()


def main():
    ORIGINALS.mkdir(exist_ok=True)
    PLOTS.mkdir(exist_ok=True)
    choice = ask_choice()
    if not choice["csv"].exists():
        raise FileNotFoundError(f"Missing results CSV: {choice['csv']}")

    print(f"Rendering bare plot area from {choice['csv'].name}...")
    ours = render_bare(choice["csv"], save=choice["bare_save"])
    print(f"Also saved: {choice['bare_save']}")

    original_path = resolve_image(choice["original"])
    print(f"Original: {original_path}")
    original = Image.open(original_path).convert("RGB")

    img_ours, img_original, size = load_aligned(ours, original)
    show_mixer(img_ours, img_original, choice["label"], size)


if __name__ == "__main__":
    main()
