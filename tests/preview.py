"""One-off preview: render key frames of the S1/S2 scenes into a contact sheet PNG."""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
sys = __import__("sys")
sys.path.insert(0, str(ROOT / "tests"))
from gifs_local import CACHE, HARNESS, W, H, build_berry, parse_frames  # noqa: E402

SCALE = 6


def gridify(frame, scale=SCALE):
    img = Image.new("RGB", (W * scale, H * scale), (0, 0, 0))
    px = img.load()
    for y in range(H):
        for x in range(W):
            c = frame[y * W + x]
            r, g, b = (c >> 16) & 255, (c >> 8) & 255, c & 255
            for yy in range(y * scale, y * scale + scale - 1):
                for xx in range(x * scale, x * scale + scale - 1):
                    px[xx, yy] = (r, g, b)
    return img


def scenes():
    cache = CACHE
    cache.mkdir(parents=True, exist_ok=True)
    berry = build_berry(cache)
    run_dir = cache / "run"
    run_dir.mkdir(exist_ok=True)
    (run_dir / "harness.ax").write_text(HARNESS, encoding="utf-8")
    (run_dir / "nimbus-tc002.ax").write_text((ROOT / "dist" / "nimbus-tc002.ax").read_text(encoding="utf-8"),
                                             encoding="utf-8")
    out = subprocess.run([str(berry), "harness.ax"], cwd=run_dir, check=True,
                         capture_output=True, text=True).stdout
    return parse_frames(out)


def sheet(frames, indices, name):
    imgs = [gridify(frames[i]) for i in indices]
    pad = 8
    w, h = imgs[0].size
    canvas = Image.new("RGB", (w * len(imgs) + pad * (len(imgs) + 1), h + pad * 2 + 16), (30, 30, 30))
    d = ImageDraw.Draw(canvas)
    for n, img in enumerate(imgs):
        x = pad + n * (w + pad)
        canvas.paste(img, (x, pad + 16))
        d.text((x, 4), "%s @%d" % (name, indices[n]), fill=(220, 220, 220))
    return canvas


def main():
    sc = scenes()
    a = sheet(sc["S1"], [0, 9, 25, 40, 60, 90, 120, 140], "meteoalarm.gif")
    b = sheet(sc["S2"], [0, 10, 30, 50, 80, 110], "meteoalarm-big.gif")
    out = Image.new("RGB", (a.width, a.height + b.height + 12), (20, 20, 20))
    out.paste(a, (0, 0))
    out.paste(b, (0, a.height + 12))
    out.save(ROOT / "tests" / "preview.png")
    print("saved", out.size)


if __name__ == "__main__":
    main()
