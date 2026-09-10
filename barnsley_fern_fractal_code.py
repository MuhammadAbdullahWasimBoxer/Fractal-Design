"""
Barnsley Fern Fractal Generator
--------------------------------
Uses an Iterated Function System (IFS) with 4 affine transformations,
each chosen with a specific probability, to plot points that
converge to the famous fern shape.
"""

import numpy as np
import matplotlib.pyplot as plt


def barnsley_fern(n_points=1_000_000):
    """Generate n_points (x, y) coordinates of the Barnsley fern."""

    # Affine transformation coefficients: (a, b, c, d, e, f, probability)
    # x' = a*x + b*y + e
    # y' = c*x + d*y + f
    transforms = [
        # f1: stem (maps almost everything to a line segment)
        (0.00,  0.00, 0.00, 0.16, 0.00, 0.00, 0.01),
        # f2: successively smaller leaflets
        (0.85,  0.04, -0.04, 0.85, 0.00, 1.60, 0.85),
        # f3: largest left-hand leaflet
        (0.20, -0.26, 0.23, 0.22, 0.00, 1.60, 0.07),
        # f4: largest right-hand leaflet
        (-0.15, 0.28, 0.26, 0.24, 0.00, 0.44, 0.07),
    ]

    probs = np.array([t[6] for t in transforms])
    cum_probs = np.cumsum(probs)

    x, y = 0.0, 0.0
    points = np.empty((n_points, 2), dtype=np.float64)

    # Precompute random choices for speed
    r = np.random.random(n_points)
    choices = np.searchsorted(cum_probs, r)

    for i in range(n_points):
        a, b, c, d, e, f, _ = transforms[choices[i]]
        x, y = a * x + b * y + e, c * x + d * y + f
        points[i] = (x, y)

    return points


def plot_fern(points, save_path="barnsley_fern.png"):
    x, y = points[:, 0], points[:, 1]

    fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
    ax.scatter(
        x, y,
        s=0.3,
        color="#1a5c1a",      # solid dark green, no fade at the base
        marker=".",
        linewidths=0,
        alpha=0.85
    )

    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")
    ax.set_xlim(x.min() - 1, x.max() + 1)
    ax.set_ylim(y.min() - 1, y.max() + 1)
    ax.set_aspect("equal")
    ax.axis("off")

    plt.tight_layout(pad=0)
    plt.savefig(save_path, facecolor=fig.get_facecolor(), bbox_inches="tight", dpi=200)
    plt.show()


if __name__ == "__main__":
    pts = barnsley_fern(n_points=1_000_000)
    plot_fern(pts)
