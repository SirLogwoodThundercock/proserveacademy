"""Remove solid edge-connected backgrounds from government logo images.
Replicates the flood-fill algorithm from logo-transparent-maker.html.
"""
import numpy as np
from PIL import Image
from collections import deque
import os

SRC = os.path.join(os.path.dirname(__file__), "src")
OUT = os.path.join(os.path.dirname(__file__), "..")

FILES = [
    ("fmle-header.jpg", "federal-ministry-labour-transparent.png", "auto", 45),
    ("nbte.jpg", "nbte-transparent.png", "auto", 45),
    ("itf.jpeg", "itf-transparent.png", "auto", 45),
    ("lastveb.jpg", "lastveb-transparent.png", "auto", 45),
    ("lsetf.jpg", "lsetf-transparent.png", "auto", 45),
]


def remove_background(img_path, mode="auto", tol=45):
    im = Image.open(img_path).convert("RGBA")
    w, h = im.size
    data = np.array(im).astype(np.int16)
    rgb = data[:, :, :3].astype(np.float32)

    # Determine background colour from corner pixels (auto mode)
    corners = [
        rgb[0, 0], rgb[0, w - 1], rgb[h - 1, 0], rgb[h - 1, w - 1],
    ]
    bg = np.median(np.array(corners), axis=0)

    # Distance from background colour
    dist = np.sqrt(((rgb - bg) ** 2).sum(axis=2) / 3.0)

    visited = np.zeros((h, w), dtype=bool)
    queue = deque()

    def seed(x, y):
        if 0 <= x < w and 0 <= y < h and not visited[y, x] and dist[y, x] <= tol:
            visited[y, x] = True
            queue.append((x, y))

    for x in range(w):
        seed(x, 0)
        seed(x, h - 1)
    for y in range(h):
        seed(0, y)
        seed(w - 1, y)

    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx] and dist[ny, nx] <= tol:
                visited[ny, nx] = True
                queue.append((nx, ny))

    alpha = data[:, :, 3].astype(np.float32)

    # Clear visited (background) pixels
    alpha[visited] = 0

    # Soften pixels adjacent to background (vectorized)
    v = visited
    beside = np.zeros_like(v)
    beside[:, 1:] |= v[:, :-1]
    beside[:, :-1] |= v[:, 1:]
    beside[1:, :] |= v[:-1, :]
    beside[:-1, :] |= v[1:, :]
    beside &= ~v
    a = np.clip((dist - tol) / 35.0, 0.12, 1.0)
    alpha[beside] = alpha[beside] * a[beside]

    data[:, :, 3] = np.clip(alpha, 0, 255).astype(np.int16)
    result = Image.fromarray(data.astype(np.uint8), "RGBA")
    # Downscale for web (max 400px on longest side)
    result.thumbnail((400, 400), Image.LANCZOS)
    return result


for src_name, out_name, mode, tol in FILES:
    src_path = os.path.join(SRC, src_name)
    out_path = os.path.join(OUT, out_name)
    result = remove_background(src_path, mode, tol)
    result.save(out_path)
    # Also save a trimmed version? Keep full size for now.
    print(f"{src_name} -> {out_name} ({result.size[0]}x{result.size[1]})")
