#!/usr/bin/env python3
"""アイコン生成（icon-512.png / icon-180.png）。デザイン変更時だけ再実行すればよい。"""
import os

from PIL import Image, ImageChops, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
BG = (20, 86, 78)        # 深い緑（テーマカラー）
FG = (244, 241, 234)     # 和紙色

S = 1024                 # 作業解像度（あとで縮小）
SS = 4                   # アンチエイリアス用の倍率
W = S * SS

img = Image.new("RGB", (W, W), BG)

# 見張る目＝2つの円の交差でアーモンド形をつくる
cx, cy = W / 2, W / 2
r = W * 0.62
off = W * 0.40
mask = None
for dy in (+off, -off):
    layer = Image.new("L", (W, W), 0)
    ImageDraw.Draw(layer).ellipse([cx - r, cy + dy - r, cx + r, cy + dy + r], fill=255)
    mask = layer if mask is None else ImageChops.multiply(mask, layer)

img.paste(Image.new("RGB", (W, W), FG), (0, 0), mask)

d = ImageDraw.Draw(img)
pr = W * 0.155                                    # 瞳
d.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=BG)
hr = W * 0.052                                    # ハイライト
d.ellipse([cx + pr * 0.15 - hr, cy - pr * 0.45 - hr,
           cx + pr * 0.15 + hr, cy - pr * 0.45 + hr], fill=FG)

# 下部に波（サバ＝海）を3本
for i, (yy, half, th) in enumerate([(0.795, 0.20, 0.020),
                                    (0.855, 0.135, 0.017),
                                    (0.905, 0.075, 0.014)]):
    y = W * yy
    d.rounded_rectangle([cx - W * half, y - W * th, cx + W * half, y + W * th],
                        radius=W * th, fill=FG)

img = img.resize((512, 512), Image.LANCZOS)
img.save(os.path.join(HERE, "icon-512.png"))
img.resize((180, 180), Image.LANCZOS).save(os.path.join(HERE, "icon-180.png"))
print("wrote icon-512.png / icon-180.png")
