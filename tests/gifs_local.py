"""README GIFs for NimbusPL without Docker: builds a local Berry interpreter, runs
dist/nimbus-tc002.ax against a software framebuffer with the firmware's small 3x5 font, captures
frames and writes docs/meteoalarm.gif (sheet face: carousel -> alert tile + full-width message ->
carousel incl. the weather panel: small icon + purple description, static when it fits and
scrolling left when it does not), docs/meteoalarm-big.gif (big face: 5-letter weekday + date ->
ALARM + hazard time), docs/weather-*.gif (one animated GIF per WMO weather state) and
docs/moon.gif (the moon-phase carousel panel).

Usage: python3 tests/gifs_local.py
Requires: network (downloads berry-lang once), gcc and make; writes docs/*.gif
"""
import io
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BERRY_URL = "https://codeload.github.com/berry-lang/berry/tar.gz/refs/heads/master"
CACHE = ROOT / "tests" / ".berry-cache"
W, H = 52, 16


def build_berry(cache=CACHE):
    """The Berry CLI in cache/, built once."""
    bin = cache / "berry"
    if bin.exists():
        return bin
    tarball = cache / "berry.tar.gz"
    urllib.request.urlretrieve(BERRY_URL, tarball)
    with tarfile.open(tarball) as tf:
        tf.extractall(cache)
    src = cache / "berry-master"
    makefile = src / "Makefile"
    makefile.write_text(makefile.read_text()
                        .replace("    CFLAGS    += -DUSE_READLINE_LIB", "    CFLAGS    += -DNO_READLINE")
                        .replace("    LIBS      += -lreadline -ldl", "    LIBS      += -ldl"))
    subprocess.run(["make", "-j2"], cwd=src, check=True, stdout=subprocess.DEVNULL)
    shutil.copy(src / "berry", bin)
    return bin


CAPS = ("##/#.#/###/#.#/#.#", "##/#.#/##/#.#/##", ".#/#.#/#/#.#/.#", "##/#.#/#.#/#.#/##", "###/#/###/#/###",
        "###/#/###/#/#", ".##/#/#.#/#.#/.##", "#.#/#.#/###/#.#/#.#", "#/#/#/#/#", "..#/..#/..#/#.#/.#",
        "#.#/#.#/##/#.#/#.#", "#/#/#/#/###", "#...#/##.##/#.#.#/#...#/#...#", "#..#/##.#/#.##/#..#/#..#",
        ".#/#.#/#.#/#.#/.#", "###/#.#/##/#/#", ".#/#.#/#.#/#.#/.###", "###/#.#/##/#.#/#.#", "###/#/###/..#/###",
        "###/.#/.#/.#/.#", "#.#/#.#/#.#/#.#/###", "#.#/#.#/#.#/#.#/.#", "#...#/#...#/#...#/#.#.#/.#.#",
        "#.#/#.#/.#/#.#/#.#", "#.#/#.#/###/..#/##", "###/..#/.#/#/###")

LOWC = (".#./#.#/###/#.#/#.#", "##./#.#/##./#.#/##.", ".##/#../#../#../.##", ".##/#.#/#.#/#.#/.##",
        "###/#../###/#../###", ".##/#../##./#../#..", ".##/#../#.##/#.#/.##", "#.#/#.#/###/#.#/#.#",
        ".#./.../.#./.#./.#.", "..#/.../..#/..#/##.", "#.#/#.#/##./#.#/#.#", "#../#../#../#../###",
        "###/#.#/#.#/#.#/#.#", "##./#.#/#.#/#.#/#.#", ".#./#.#/#.#/#.#/.#.", "##./#.#/##./#../#..",
        ".#./#.#/#.#/##./..#", "##./#.#/#../#../#..", ".##/#../.#./..#/##.", ".#./##./.#./.#./..#",
        "#.#/#.#/#.#/#.#/.##", "#.#/#.#/#.#/#.#/.#.", "#.#/#.#/#.#/#.#/###", "#.#/#.#/.#./#.#/#.#",
        "#.#/#.#/.##/..#/##.", "###/..#/.#./#../###")

DIGITS = {"0": "###/#.#/#.#/#.#/###", "1": ".#./##./.#./.#./###", "2": "###/..#/###/#../###",
          "3": "###/..#/###/..#/###", "4": "#.#/#.#/###/..#/..#", "5": "###/#../###/..#/###",
          "6": "###/#../###/#.#/###", "7": "###/../#/../#/..", "8": "###/#.#/###/#.#/###",
          "9": "###/#.#/###/..#/###", "-": ".../.../###/.../...", ":": "./#/./#/.",
          ".": "././././#", " ": ".../.../.../.../...", "%": "#.#/../#/.#./#../#.#"}

# Polish diacritics for the firmware font emulation (6 rows = accent above / ogonek below)
PL = {
    "Ą": "##./#.#/###/#.#/##.#",
    "Ć": ".#/.#/#.#/#/#.#/.#",
    "Ę": "###/#../###/#../###/..#",
    "Ł": "#./#./##./#./###",
    "Ń": ".#/##./#.#/#.#/#.#/#.#",
    "Ó": ".#/.#/#.#/#.#/#.#/.#",
    "Ś": ".#/.##/#../.#./..#/##.",
    "Ź": ".#/###/..#/.#./#../###",
    "Ż": ".#./###/..#/.#./#../###",
}

# every WMO weather state shown in its own GIF: (scene marker, file name, weather_code, is_day)
WEATHER = [
    ("W0", "slonecznie", 0, 1),
    ("WN", "slonecznie-noc", 0, 0),
    ("W1", "przewaznie-slonecznie", 1, 1),
    ("W2", "zachmurzenie", 2, 1),
    ("W3", "chmury", 3, 1),
    ("W45", "mgla", 45, 1),
    ("W48", "szadz", 48, 1),
    ("W51", "mzawka", 51, 1),
    ("W55", "silna-mzawka", 55, 1),
    ("W56", "mzawka-marznaca", 56, 1),
    ("W57", "silna-mzawka-marznaca", 57, 1),
    ("W61", "deszcz", 61, 1),
    ("W65", "ulewa", 65, 1),
    ("W66", "deszcz-marznacy", 66, 1),
    ("W67", "silny-deszcz-marznacy", 67, 1),
    ("W71", "snieg", 71, 1),
    ("W75", "sniezyca", 75, 1),
    ("W77", "krupa-sniezna", 77, 1),
    ("W80", "przelotny-deszcz", 80, 1),
    ("W82", "ulewny-przelotny-deszcz", 82, 1),
    ("W85", "przelotny-snieg", 85, 1),
    ("W86", "silny-przelotny-snieg", 86, 1),
    ("W95", "burza", 95, 1),
    ("W96", "burza-z-gradem", 96, 1),
    ("W99", "burza-z-silnym-gradem", 99, 1),
]


HARNESS = r'''
import string
import math

# ---------- the firmware's small 3x5 font ----------
var CAPSL = [%s]
var LOWCL = [%s]
var DIGL = {%s}
var F = {}
var i = 0
while i < 26
  F["ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]] = string.split(CAPSL[i], "/")
  F["abcdefghijklmnopqrstuvwxyz"[i]] = string.split(LOWCL[i], "/")
  i += 1
end
var dkeys = "0123456789-:. %%"
i = 0
while i < size(dkeys)
  F[dkeys[i]] = string.split(DIGL[dkeys[i]], "/")
  i += 1
end
%s

# ---------- the framebuffer ----------
var BUF = []
i = 0
while i < 832
  BUF.push(0)
  i += 1
end
def clear()
  i = 0
  while i < 832
    BUF[i] = 0
    i += 1
  end
end
def pixel(x, y, c)
  if x >= 0 && x < 52 && y >= 0 && y < 16
    BUF[y * 52 + x] = c
  end
end
def rect_fill(x, y, w, h, c)
  var yy = y
  while yy < y + h
    var xx = x
    while xx < x + w
      pixel(xx, yy, c)
      xx += 1
    end
    yy += 1
  end
end
def rect(x, y, w, h, c) end
def line(x0, y0, x1, y1, c) end
def circle(x, y, r, c) end
def circle_fill(x, y, r, c) end
def bar_chart(v, c) end
def line_chart(v, c) end
def progress(v, a, b) end
def effect(n) end
def overlay(n) end
def icon(n, x, y) return true end
def font(n) end
def rgb(r, g, b) return (r << 16) | (g << 8) | b end
def hsv(h, s, v) return 0xFFFFFF end
def clamp(v, lo, hi)
  if v < lo return lo end
  if v > hi return hi end
  return v
end
def round(x) return int(x + 0.5) end
def num(x) return real(x) end
def width() return 52 end
def height() return 16 end

var _NOW = 100000
var _H = 9
var _Mi = 37
var _S = 0
var _D = 4
var _M = 11
var _Y = 2026
var _WD = 3
def now_ms() return _NOW end
def epoch_ms() return 1700000000000 end
def hour() return _H end
def minute() return _Mi end
def second() return _S end
def weekday() return _WD end
def day() return _D end
def month() return _M end
def year() return _Y end

# ---------- text ----------
def textw(s)
  var t = 0
  var i = 0
  while i < size(s)
    var ch = s[i .. i]
    var adv = 1
    if i + 1 < size(s)
      var ch2 = s[i .. i + 1]
      if F.find(ch2) != nil
        ch = ch2
        adv = 2
      end
    end
    var g = F.find(ch)
    t += g == nil ? 4 : size(g[0]) + 1
    i += adv
  end
  return t > 0 ? t - 1 : 0
end
def draw_text(x, y, s, col, clipx, clipw)
  var cx = x
  var i = 0
  while i < size(s)
    var ch = s[i .. i]
    var adv = 1
    if i + 1 < size(s)
      var ch2 = s[i .. i + 1]
      if F.find(ch2) != nil
        ch = ch2
        adv = 2
      end
    end
    var g = F.find(ch)
    if g == nil
      cx += 4
      i += adv
      continue
    end
    var r = 0
    while r < size(g)
      var c = 0
      while c < size(g[r])
        if g[r][c] == "#"
          var px = cx + c
          var py = y - 5 + r
          if px >= clipx && px < clipx + clipw && py >= 0 && py < 16
            BUF[py * 52 + px] = col
          end
        end
        c += 1
      end
      r += 1
    end
    cx += size(g[0]) + 1
    i += adv
  end
  return cx
end
def text(x, y, s, col)
  draw_text(x, y, s, col, 0, 52)
  return textw(s) + 1
end
def scroll_text(x, y, w, s, col, o)
  var tw = textw(s)
  if tw <= w
    draw_text(int(x + (w - tw) / 2), y, s, col, x, w)
  else
    var gap = 10
    if o != nil && o.find("gap") != nil
      gap = o.find("gap")
    end
    var sp = 8.4
    var t = (_NOW * sp / 1000.0) %% (tw + gap)
    draw_text(int(x + w - t), y, s, col, x, w)
  end
  return 0
end
def ramp_text(x, y, s, p) return text(x, y, s, 0xFFFFFF) end
def text_ink_width(s) return textw(s) end
def text_width(s) return textw(s) + 1 end

# ---------- firmware services ----------
class _Store
  var m
  def init(face)
    self.reset(face)
  end
  def reset(face)
    self.m = {
      "sweep": true, "t24": true, "tlz": true, "tsep": "stały", "tcol": 0xFFFFFF,
      "chc": 0xFF0000, "ctc": 0x000000, "cbc": 0xFFFFFF, "wbar": true, "wmon": true,
      "wtd": 0xFFFFFF, "wod": 0x666666, "wtw": 0xFFFFFF, "wow": 0x666666,
      "tran": "przetarcie", "ddur": 2, "pdur": 2, "wdur": 2, "moon": true, "wind": true, "rcol": 0xFFFFFF, "hcol": 0x00AAFF,
      "nauto": false, "nfrom": 22, "nto": 7, "nbar": true, "npause": false, "nbri": 0,
      "face": face, "canim": false, "dfmt": "dd.mm.yy", "showpm": true,
      "order": "", "lat": 52.23, "lon": 21.01,
      "wref": 15, "wlang": "Polski", "wtext": "", "rtopic": "", "htopic": "",
      "night": false, "ntopic": "", "meteoalarm_enabled": true, "maref": 10,
      "madur": 8, "mafreq": 5, "mafreqb": 60, "materyt": ""
    }
  end
  def get(k, d)
    var v = self.m.find(k)
    return v == nil ? d : v
  end
  def set(k, v) self.m[k] = v end
end

class _Settings
  def get(k)
    if k == "useCelsius" return true end
    if k == "transitionDurationMs" return 500 end
    return nil
  end
  def set(k, v) end
end

class _Sensor
  def temperature() return 21.5 end
  def humidity() return 45.0 end
end

class _Mqtt
  def subscribe(t, cb) end
end

class _Rotation
  def show() end
  def pause() end
  def resume() end
end

class _Re
  def _group(g, s, j)
    var out = ""
    if g == "[^\"]+"
      while j < size(s) && s[j] != "\"" out += s[j] j += 1 end
    elif g == "[-0-9.]+"
      while j < size(s) && (s[j] == "-" || s[j] == "." || (s[j] >= "0" && s[j] <= "9")) out += s[j] j += 1 end
    elif g == "[0-9]+"
      while j < size(s) && s[j] >= "0" && s[j] <= "9" out += s[j] j += 1 end
    elif g == "[0-9]"
      if j < size(s) && s[j] >= "0" && s[j] <= "9" out += s[j] end
    end
    return out
  end
  def search(pat, s)
    var p = string.find(pat, "(")
    if p < 0 return nil end
    var lit = p == 0 ? "" : pat[0 .. p - 1]
    var i = lit == "" ? 0 : string.find(s, lit)
    if i < 0 return nil end
    var q = size(pat) - 1
    while q > p && pat[q] != ")" q -= 1 end
    var g = pat[p + 1 .. q - 1]
    var out = self._group(g, s, i + size(lit))
    if size(out) == 0 return nil end
    return [pat, out]
  end
  def matchall(pat, s)
    var out = []
    var cur = ""
    var i = 0
    while i < size(s)
      var ch = s[i]
      var ok = (ch >= "a" && ch <= "z") || (ch >= "0" && ch <= "9")
      if ok
        cur += ch
      else
        if size(cur) > 0 out.push(cur) cur = "" end
      end
      i += 1
    end
    if size(cur) > 0 out.push(cur) end
    return out
  end
end

var _WC = 2
var _DAY = 1
var _PM = 12.3
var _WG = 25
class _Http
  def get(url, cb, opts)
    if string.find(url, "imgw") >= 0
      cb('[{"id":"Sk2","nazwa_zdarzenia":"Silny wiatr","stopien":"3","prawdopodobienstwo":"80","obowiazuje_do":"2026-11-04 10:00:00","obowiazuje_od":"2026-11-04 01:00:00","opublikowano":"2026-11-03 11:38:00","tresc":"x","komentarz":"Brak.","biuro":"y","teryt":["1465"]}]', 200)
    elif string.find(url, "air-quality") >= 0
      cb('{"current":{"pm2_5":' + str(_PM) + '}}', 200)
    else
      cb('{"current":{"temperature_2m":21.5,"weather_code":' + str(_WC) + ',"is_day":' + str(_DAY) + ',"wind_gusts_10m":' + str(_WG) + '}}', 200)
    end
  end
end

var store = _Store("kartka")
var settings = _Settings()
var sensor = _Sensor()
var mqtt = _Mqtt()
var rotation = _Rotation()
var re = _Re()
var http = _Http()

# ---------- frame dump ----------
def hexbuf()
  var h = "0123456789abcdef"
  var s = ""
  var i = 0
  while i < 832
    var n = BUF[i]
    var c = 5
    while c >= 0
      s += h[(n >> (c * 4)) & 15]
      c -= 1
    end
    i += 1
  end
  return s
end

# ---------- scenes ----------
var app = compile("nimbus-tc002.ax", "file")()
var mk = compile("return NimbusPL()", "string")

def run_scene(face, seconds, marker, cfg)
  store.reset(face)
  if cfg != nil
    for k : cfg.keys()
      store.set(k, cfg[k])
    end
    var wcv = cfg.find("wcode")
    if wcv != nil _WC = wcv end
    var dv = cfg.find("isday")
    if dv != nil _DAY = dv end
    var pmv = cfg.find("pm25")
    if pmv != nil _PM = pmv end
    var wgv = cfg.find("windgust")
    if wgv != nil _WG = wgv end
  end
  var n = mk()
  n.init()
  print(marker)
  if cfg != nil && cfg.find("warm") != nil
    n.loop()
  end
  var f = 0
  while f < seconds * 10
    _NOW += 100
    if _NOW %% 1000 == 0
      n.loop()
    end
    n.draw()
    print("F" + hexbuf())
    f += 1
  end
end

run_scene("kartka", 32, "S1", nil)
run_scene("duży", 18, "S2", nil)
run_scene("kartka", 6, "S3", {
  "meteoalarm_enabled": false, "order": "1", "wpan": false, "wind": false, "dpan": false, "tpan": false, "showpm": false, "rpan": false, "hpan": false, "moon": false, "wpan": true, "wdur": 8,
  "wtext": "słonecznie,przeważnie słonecznie,ZACHMURZENIE Z PRZELOTNYMI OPADAMI,chmury,mgła,szadź,mżawka,silna mżawka,mżawka marznąca,silna mżawka marznąca,deszcz,ulewa,deszcz marznący,silny deszcz marznący,śnieg,śnieżyca,krupa śnieżna,przelotny deszcz,ulewny przelotny deszcz,przelotny śnieg,silny przelotny śnieg,burza,burza z gradem"
})
run_scene("kartka", 6, "S4", {
  "meteoalarm_enabled": false, "order": "1", "wpan": false, "wind": false, "dpan": false, "tpan": false, "showpm": false, "rpan": false, "hpan": false, "moon": false, "wpan": true, "wdur": 8, "wcode": 66
})
run_scene("kartka", 5, "S5", {
  "meteoalarm_enabled": false, "order": "8", "wpan": false, "wind": false, "dpan": false, "tpan": false, "showpm": false, "rpan": false, "hpan": false, "moon": false, "moon": true, "warm": true
})
run_scene("kartka", 22, "S6", {
  "meteoalarm_enabled": false, "warm": true
})
run_scene("kartka", 4, "S7", {
  "meteoalarm_enabled": false, "order": "3", "wpan": false, "wind": false, "dpan": false, "tpan": false, "showpm": false, "rpan": false, "hpan": false, "moon": false, "dpan": true, "warm": true
})
run_scene("pierścień", 4, "S8", {
  "meteoalarm_enabled": false, "order": "3", "wpan": false, "wind": false, "dpan": false, "tpan": false, "showpm": false, "rpan": false, "hpan": false, "moon": false, "dpan": true, "warm": true
})
run_scene("duży", 4, "S9", {
  "meteoalarm_enabled": false, "order": "3", "wpan": false, "wind": false, "dpan": false, "tpan": false, "showpm": false, "rpan": false, "hpan": false, "moon": false, "dpan": true, "warm": true
})
run_scene("kartka", 4, "S10", {
  "meteoalarm_enabled": false, "order": "5", "wpan": false, "wind": false, "dpan": false, "tpan": false, "showpm": false, "rpan": false, "hpan": false, "moon": false, "showpm": true, "warm": true, "pm25": 100
})
run_scene("kartka", 4, "S11", {
  "meteoalarm_enabled": false, "order": "5", "wpan": false, "wind": false, "dpan": false, "tpan": false, "showpm": false, "rpan": false, "hpan": false, "moon": false, "showpm": true, "warm": true, "pm25": 200
})
run_scene("kartka", 8, "S12", {
  "meteoalarm_enabled": false, "moon": false, "warm": true, "windgust": 100, "wcode": 2,
  "wpan": true, "dpan": true, "tpan": false, "showpm": false, "rpan": false, "hpan": false
})
run_scene("kartka", 5, "S13", {
  "meteoalarm_enabled": false, "wpan": true, "dpan": true, "wind": true, "tpan": false,
  "showpm": false, "rpan": false, "hpan": false, "moon": false, "warm": true, "windgust": 85, "wthr": 90
})
var WC = [%s]
var wi = 0
while wi < size(WC)
  run_scene("kartka", 4, WC[wi][2], {"meteoalarm_enabled": false, "order": "1", "wpan": false, "wind": false, "dpan": false, "tpan": false, "showpm": false, "rpan": false, "hpan": false, "moon": false, "wpan": true, "wdur": 8, "wcode": WC[wi][0], "isday": WC[wi][1], "warm": true})
  wi += 1
end
print("DONE")
''' % (", ".join('"%s"' % c for c in CAPS), ", ".join('"%s"' % c for c in LOWC),
       ", ".join('"%s": "%s"' % (k, v) for k, v in DIGITS.items()),
       "\n".join('  F["%s"] = string.split("%s", "/")' % (ch, gl) for ch, gl in PL.items()),
       ", ".join('[%d, %d, "%s"]' % (code, day, marker) for marker, name, code, day in WEATHER))


def parse_frames(output):
    """{marker: [frames]} where a frame is a list of 832 ints."""
    scenes = {}
    current = None
    for line in output.splitlines():
        m = re.match(r"^([SW]\w+)$", line)
        if m:
            current = m.group(1)
            scenes[current] = []
        elif line.startswith("F") and current:
            hx = line[1:]
            if len(hx) == 832 * 6:
                scenes[current].append([int(hx[i:i + 6], 16) for i in range(0, len(hx), 6)])
    return scenes


def render(frame, scale=8, gap=3):
    from PIL import Image
    img = Image.new("RGB", (W * scale, H * scale), (0, 0, 0))
    px = img.load()
    for y in range(H):
        for x in range(W):
            c = frame[y * W + x]
            r, g, b = (c >> 16) & 255, (c >> 8) & 255, c & 255
            for yy in range(y * scale, (y + 1) * scale):
                for xx in range(x * scale, (x + 1) * scale):
                    if (xx % scale >= scale - gap) or (yy % scale >= scale - gap):
                        px[xx, yy] = (0x18, 0x18, 0x18)
                    else:
                        px[xx, yy] = (r, g, b)
    return img


def write_gif(path, frames, duration_ms=100, scale=8, gap=3):
    """LED-matrix look: every pixel becomes a (scale-gap) block with a dark gap between LEDs."""
    from PIL import Image
    GAPC = 0x181818
    colors = sorted({GAPC} | {c for f in frames for c in f})
    assert len(colors) <= 256, len(colors)
    idx = {c: i for i, c in enumerate(colors)}
    pal = []
    for c in colors:
        pal += [(c >> 16) & 255, (c >> 8) & 255, c & 255]
    pal += [0, 0, 0] * (256 - len(colors))
    imgs = []
    for f in frames:
        im = Image.new("P", (W * scale, H * scale))
        im.putpalette(pal)
        data = [idx[GAPC]] * (W * scale * H * scale)
        for y in range(H):
            for x in range(W):
                c = idx[f[y * W + x]]
                for yy in range(y * scale, y * scale + scale - gap):
                    for xx in range(x * scale, x * scale + scale - gap):
                        data[yy * W * scale + xx] = c
        im.putdata(data)
        imgs.append(im)
    imgs[0].save(path, save_all=True, append_images=imgs[1:], duration=duration_ms,
                 loop=0, optimize=False)
    return path


def dump(f):
    print("colors:", sorted({c for c in f if c}))
    out = []
    for y in range(H):
        line = ""
        for x in range(W):
            c = f[y * W + x]
            line += "#" if c == 0xFFFFFF else ("R" if c == 0xFF0000 else
                     ("Y" if c in (0xFFC800, 0xFF7800) else ("." if c == 0 else "o")))
        out.append(line)
    return "\n".join(out)


def check_help_limits():
    """AWTRIX NG truncates @config help texts to 96 bytes (kMaxHelpLen in ScriptConfig.cpp,
    counted over UTF-8 bytes - Polish letters take two)."""
    src = (ROOT / "dist" / "nimbus-tc002.ax").read_text(encoding="utf-8")
    for m in re.finditer(r'help="([^"]*)"', src):
        assert len(m.group(1).encode("utf-8")) <= 96, "help longer than 96 bytes: " + m.group(1)


def checks(scenes):
    s1 = scenes["S1"]
    # sheet face: the alert shows as a red message strip on rows 10-14 (appears after ~2 s
    # and lasts ~8 s). Find it programmatically instead of relying on a hardcoded frame.
    alert = [i for i, f in enumerate(s1)
             if any(f[y * W + x] == 0xFF0000 for y in range(10, 15) for x in range(W))]
    assert alert, "no alert frames in S1"
    f = s1[min(alert[0] + 12, len(s1) - 1)]
    print(dump(f))
    assert f[0] == 0xFF0000, "tile not at the top-left"
    assert not any(f[15 * W + x] for x in range(17, 51)), "week bar visible during the message"
    # after the message the carousel comes back and the week bar returns
    f = s1[-1]
    assert not any(f[y * W + x] == 0xFF0000 for y in range(10, 15) for x in range(W)), "message still visible"
    assert any(f[15 * W + x] for x in range(17, 51)), "week bar missing after the message"
    # weather panel: small icon (sun yellow) in the 15-px field at the top +
    # the purple description across the full width under the clock; "ZACHMURZENIE" fits, so it
    # is drawn once, statically, and does not scroll
    weather = [i for i, f in enumerate(s1)
               if any(f[y * W + x] in (0xFFC800, 0xFF7800) for y in range(1, 9) for x in range(15))]
    assert weather, "no weather-panel frames in S1"
    # the first weather stretch is cut short by the meteoalarm message: find a stretch
    # of >= 8 consecutive weather frames and compare two frames inside it
    runs = []
    rs = weather[0]
    for i in range(1, len(weather)):
        if weather[i] != weather[i - 1] + 1:
            runs.append((rs, weather[i - 1]))
            rs = weather[i]
    runs.append((rs, weather[-1]))
    run = next((r for r in runs if r[1] - r[0] >= 8), None)
    assert run, "no long weather stretch in S1"
    fw = s1[run[0] + 1]
    print(dump(fw))
    assert any(fw[y * W + x] == 0xC24CFF for y in range(10, 15) for x in range(16, 52)), \
        "purple weather description not visible across the full width"
    # left-aligned: the short description starts at the left edge and ends before x=48
    assert any(fw[y * W + x] == 0xC24CFF for y in range(10, 15) for x in range(0, 4)), \
        "weather description is not left-aligned"
    assert not any(fw[y * W + x] == 0xC24CFF for y in range(10, 15) for x in range(48, 52)), \
        "weather description should not reach the right edge"
    fz = s1[run[0] + 7]
    assert all(fw[y * W + x] == fz[y * W + x] for y in range(10, 15) for x in range(16, 52)), \
        "short weather description should be static"
    s3 = scenes["S3"]
    # a long description scrolls left across the width (purple, week bar hidden)
    assert any(f[y * W + x] == 0xC24CFF for y in range(10, 15) for x in range(16, 52)
               for f in s3[10:]), "no purple description in S3"
    assert not any(s3[20][15 * W + x] in (0xFFFFFF, 0x666666) for x in range(17, 51)), "week bar visible during weather panel (S3)"
    assert any(s3[20][y * W + x] != s3[40][y * W + x] for y in range(10, 15) for x in range(16, 52)), \
        "long weather description is not scrolling"
    s4 = scenes["S4"]
    # WMO code 66 = freezing rain: cloud icon + ice-blue dots + scrolling "DESZCZ MARZNACY"
    assert any(s4[20][y * W + x] == 0x80D8FF for y in range(1, 10) for x in range(15)), \
        "no ice-blue precipitation dots for freezing rain"
    assert any(s4[20][y * W + x] == 0xC24CFF for y in range(10, 15) for x in range(16, 52)), \
        "no purple freezing-rain description"
    assert any(s4[20][y * W + x] != s4[40][y * W + x] for y in range(10, 15) for x in range(16, 52)), \
        "freezing-rain description is not scrolling"
    assert not any(s4[20][15 * W + x] in (0xFFFFFF, 0x666666) for x in range(17, 51)), "week bar visible during weather panel (S4)"


def anyc(frames, col, y0, y1, x0, x1, start=10):
    """True if col appears anywhere in the given region of any settled frame."""
    return any(frames[i][y * W + x] == col for i in range(start, len(frames))
               for y in range(y0, y1) for x in range(x0, x1))


def check_weather_gifs(scenes):
    """Every WMO state: purple description, hidden week bar, and the state-specific animation."""
    # wmo code -> expected precipitation dot color inside the icon field
    dots = {51: 0x64B5F6, 55: 0x64B5F6, 56: 0x80D8FF, 57: 0x80D8FF, 61: 0x2890FF, 65: 0x0055FF,
            66: 0x80D8FF, 67: 0x80D8FF, 71: 0xFFFFFF, 75: 0xE0F7FA, 77: 0xFFFFFF, 80: 0x2890FF,
            82: 0x0055FF, 85: 0xFFFFFF, 86: 0xFFFFFF, 96: 0xFFFFFF, 99: 0xFFFFFF}
    for marker, name, code, day in WEATHER:
        fs = scenes[marker]
        f = fs[20]
        assert any(f[y * W + x] == 0xC24CFF for y in range(10, 15) for x in range(W)), \
            "%s: no purple description" % marker
        assert not any(f[15 * W + x] in (0xFFFFFF, 0x666666) for x in range(17, 51)), \
            "%s: week bar visible" % marker
        if code in dots:
            assert anyc(fs, dots[code], 1, 10, 0, 15), "%s: no precipitation dots" % marker
    assert anyc(scenes["W0"], 0xFFC800, 1, 9, 0, 15), "W0: no yellow sun"
    assert anyc(scenes["WN"], 0xF0DC8C, 1, 9, 0, 15), "WN: no moon"
    assert anyc(scenes["W1"], 0xFFC800, 1, 9, 0, 15), "W1: no sun behind the cloud"
    for marker in ("W95", "W96"):
        assert anyc(scenes[marker], 0xFFC800, 1, 10, 0, 15), "%s: no lightning flash" % marker
    # fog alternates between its two layer bitmaps (700 ms apart)
    fs = scenes["W45"]
    assert any(fs[i][y * W + x] != fs[i + 7][y * W + x]
               for i in range(12, 20) for y in range(1, 10) for x in range(15)), "fog is not animated"
    # the moon panel appears at the end of the carousel cycle: warm-white lit moon on black
    s1m = scenes["S1"]
    moonf = [i for i, f in enumerate(s1m)
             if any(f[y * W + x] == 0xF0DC8C for y in range(0, 15) for x in range(15))]
    assert moonf, "no moon-panel frames in S1"
    f = s1m[min(moonf[0] + 6, len(s1m) - 1)]
    assert any(f[15 * W + x] for x in range(17, 51)), "week bar missing during the moon panel"
    s5 = scenes["S5"]
    f = s5[10]
    assert any(f[y * W + x] == 0xF0DC8C for y in range(0, 15) for x in range(15)), "S5: no lit moon"
    assert any(f[y * W + x] == 0x3C3C3C for y in range(0, 15) for x in range(15)), "S5: no moon outline"
    assert any(f[15 * W + x] for x in range(17, 51)), "S5: week bar missing during the moon panel"
    # the demo carousel cycle: date card, weather, pm25 and the moon all appear
    s6 = scenes["S6"]
    assert any(s6[i][0] == 0xFF0000 for i in range(len(s6))), "S6: no date card"
    assert any(s6[i][y * W + x] == 0xC24CFF for i in range(len(s6)) for y in range(10, 15) for x in range(W)), \
        "S6: no weather description"
    assert any(s6[i][y * W + x] == 0x00FF00 for i in range(len(s6)) for y in range(0, 16) for x in range(15)), \
        "S6: no pm25 panel"
    assert any(s6[i][y * W + x] == 0xF0DC8C for i in range(len(s6)) for y in range(0, 15) for x in range(15)), \
        "S6: no moon panel"
    # face previews are non-empty
    for marker in ("S7", "S8", "S9"):
        assert any(scenes[marker][5]), "%s: empty preview frame" % marker
    # PM2.5 100 -> purple, 200 -> navy
    s10 = scenes["S10"]
    assert any(s10[10][y * W + x] == 0xC24CFF for y in range(0, 16) for x in range(15)), \
        "S10: pm25 panel is not purple"
    s11 = scenes["S11"]
    assert any(s11[10][y * W + x] == 0x0033AA for y in range(0, 16) for x in range(15)), \
        "S11: pm25 panel is not navy"
    # wind gusts > 40 km/h: the wind panel joins the rotation (icon + speed, week bar hidden)
    s12 = scenes["S12"]
    windf = [i for i, f in enumerate(s12)
             if f[0] == 0 and any(f[y * W + x] in (0xFFFFFF, 0xC24CFF) for y in range(7, 14) for x in range(15))]
    assert windf, "S12: no wind panel frames"
    f = s12[windf[len(windf) // 2]]
    assert not any(f[15 * W + x] in (0xFFFFFF, 0x666666) for x in range(31, 51)), \
        "S12: week bar visible during the wind panel"
    m = windf[len(windf) // 2]
    assert any(s12[windf[i + 5]][y * W + x] != s12[windf[i]][y * W + x]
               for i in range(0, len(windf) - 5)
               for y in range(0, 7) for x in range(15)), "S12: wind icon is not animated"
    # fixed order: weather first, the wind panel right after it (and before the date)
    weatherf = [i for i, f in enumerate(s12)
                if any(f[y * W + x] in (0xFFC800, 0xFF7800) for y in range(1, 9) for x in range(15))]
    assert weatherf, "S12: no weather panel"
    datef = [i for i, f in enumerate(s12) if f[0] == 0xFF0000]
    assert datef, "S12: no date panel"
    assert weatherf[len(weatherf) // 2] < m < datef[len(datef) // 2], \
        "S12: the wind panel is not between the weather and the date"
    # below the threshold (wthr=90 vs gust 85): the wind panel must not join the rotation
    s13 = scenes["S13"]
    wind13 = [i for i, f in enumerate(s13)
              if f[0] == 0 and any(f[y * W + x] == 0xF40214 for y in (1, 2) for x in range(15))]
    assert not wind13, "S13: wind panel shown below the threshold"
    s2 = scenes["S2"]
    # big face: 5-letter red weekday + white date line at the bottom (the date panel is
    # no longer first in the carousel, so find its frames)
    datef = [i for i, f in enumerate(s2)
             if any(f[y * W + x] == 0xFFFFFF for y in range(11, 16) for x in range(20, 52))
             and any(f[y * W + x] == 0xFF0000 for y in range(11, 16) for x in range(25))]
    assert datef, "no big-face date panel in S2"
    f = s2[datef[len(datef) // 2]]
    # big face: ALARM panel with the red scrolling hazard text
    f = s2[50]
    assert any(f[y * W + x] == 0xFF0000 for y in range(11, 16) for x in range(10, 52)), "no alert text"


def main():
    cache = CACHE
    cache.mkdir(parents=True, exist_ok=True)
    berry = build_berry(cache)
    run_dir = cache / "run"
    run_dir.mkdir(exist_ok=True)
    (run_dir / "harness.ax").write_text(HARNESS, encoding="utf-8")
    script = run_dir / "nimbus-tc002.ax"
    script.write_text((ROOT / "dist" / "nimbus-tc002.ax").read_text(encoding="utf-8"), encoding="utf-8")
    out = None
    try:
        out = subprocess.run([str(berry), "harness.ax"], cwd=run_dir, check=True,
                             capture_output=True, text=True).stdout
    except subprocess.CalledProcessError as e:
        print("--- stdout ---\n%s" % e.stdout[-3000:])
        print("--- stderr ---\n%s" % e.stderr[-3000:])
        raise
    scenes = parse_frames(out)
    assert "S1" in scenes and "S2" in scenes and "S3" in scenes and "S4" in scenes and "S5" in scenes, (out[-500:])
    assert all(k in scenes for k in ("S6", "S7", "S8", "S9", "S10", "S11", "S12", "S13")), (out[-500:])
    check_help_limits()
    checks(scenes)
    check_weather_gifs(scenes)
    docs = ROOT / "docs"
    write_gif(docs / "meteoalarm.gif", scenes["S1"])
    write_gif(docs / "meteoalarm-big.gif", scenes["S2"])
    write_gif(docs / "moon.gif", scenes["S5"])
    write_gif(docs / "demo-carousel.gif", scenes["S6"])
    write_gif(docs / "wind.gif", scenes["S12"])
    render(scenes["S7"][5]).save(docs / "tc002-sheet.png")
    render(scenes["S8"][5]).save(docs / "tc002-ring.png")
    render(scenes["S9"][5]).save(docs / "tc002-big.png")
    for name in ("meteoalarm.gif", "meteoalarm-big.gif"):
        p = docs / name
        print("%s (%d frames, %d KB)" % (p, len(scenes["S1" if "big" not in name else "S2"]),
                                         p.stat().st_size // 1024))
    for marker, name, code, day in WEATHER:
        p = docs / ("weather-%s.gif" % name)
        write_gif(p, scenes[marker])
        print("%s (%d frames, %d KB)" % (p, len(scenes[marker]), p.stat().st_size // 1024))


if __name__ == "__main__":
    main()
