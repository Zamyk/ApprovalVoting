from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent


def plot_sample(result, save, title, show=True, path=None, rule_label="S-PAV", ylabel="distance from voter mean"):
  df = pd.read_csv(path or result)
  plt.figure(figsize=(8, 4))
  for d_val in df["d"].unique():
    subset = df[df["d"] == d_val].sort_values("alpha")
    plt.plot(subset["alpha"], subset["distance"], label=f"d = {d_val}")
  plt.axvline(x=0.5, color="black", linestyle="--", label=rule_label)
  plt.title(title)
  plt.xlabel(r"$\alpha$")
  plt.ylabel(ylabel)
  plt.ylim(0, 1.0)
  plt.xlim(0, 1.0)
  plt.legend()
  plt.grid(False)
  plt.tight_layout()
  out = Path(save)
  out.parent.mkdir(parents=True, exist_ok=True)
  plt.savefig(out, dpi=150, bbox_inches="tight")
  if show:
    plt.show()
  return out


def plot_iterations(result, save, title, show=True, path=None, rule_label="S-PAV", ylabel="distance from voter mean"):
  grouped = pd.read_csv(path or result)
  plt.figure(figsize=(8, 4))
  for d_val in grouped["d"].unique():
    subset = grouped[grouped["d"] == d_val].sort_values("alpha")
    line, = plt.plot(subset["alpha"], subset["mean"], label=f"d = {d_val}")
    plt.fill_between(
      subset["alpha"],
      subset["min"].clip(lower=0, upper=1),
      subset["max"].clip(lower=0, upper=1),
      color=line.get_color(),
      alpha=0.15,
    )
  plt.axvline(x=0.5, color="black", linestyle="--", label=rule_label)
  plt.title(title)
  plt.xlabel(r"$\alpha$")
  plt.ylabel(ylabel)
  plt.ylim(0, 1.0)
  plt.xlim(0, 1.0)
  plt.legend()
  plt.grid(False)
  plt.tight_layout()
  out = Path(save)
  out.parent.mkdir(parents=True, exist_ok=True)
  plt.savefig(out, dpi=150, bbox_inches="tight")
  if show:
    plt.show()
  return out
