---
name: slide-kit
description: Generate .pptx slide decks in the Modernization corporate style extracted from Template3.pptx (navy constellation cover/section/closing art, white content slides with slate Lato 32pt title + eyebrow + 3 accent squares, slate #445469 text, light-blue info boxes, slate/lime flowchart boxes, horizontal timeline, blue-header zebra tables, dark slate code panels, red bold-italic footnotes). Use whenever the user asks to create slides/deck/pptx "theo style này", "giống Template3/Modernization", or loads this kit. Strictly brand-neutral — no company logo or brand asset anywhere; never draw any logo on slides.
argument-hint: "<deck request> [--output-dir <dir>]"
metadata:
  author: baka3k
  version: "1.0.0"
  last_updated: "2026-10-18"
---

# Slide kit — Modernization deck generator (Template3 style)

Bộ tool sinh file `.pptx` đúng chuẩn style được trích xuất từ `Template3.pptx` (deck "Modernization Strategy"): slide bìa/section/kết dùng ảnh nền navy constellation (1920×1080) kèm tiêu đề Lato Bold trắng 50pt; slide nội dung nền trắng có eyebrow + tiêu đề Lato 32pt màu slate `#445469`, 3 ô vuông accent dưới tiêu đề, số trang góc phải-dưới; nội dung thân gồm bullet 18/16pt, infobox xanh nhạt, flowchart bo tròn slate/lime, timeline ngang, bảng header xanh dương zebra xanh nhạt, panel code slate đậm, ghi chú đỏ in đậm nghiêng cuối trang.

## Quick start

```bash
python3 <skill_dir>/scripts/gen_deck.py spec.json -o deck.pptx
python3 <skill_dir>/scripts/gen_deck.py <skill_dir>/examples/deck_spec.json -o /tmp/example_deck.pptx
```

QA bắt buộc trước khi giao (render từng slide bằng PowerPoint thật rồi soi từng trang):

```bash
python3 <skill_dir>/scripts/render_preview.py deck.pptx --output-dir /tmp/deck_preview
```

Mở `contact-sheet.jpg` và từng `slide-NN.png`, kiểm tra: text tràn khung/chồng lấn, bảng quá dài, node/connector lệch, nhãn timeline bị xuống dòng, ảnh méo. Sửa spec → gen lại → render lại, đến khi sạch mới giao. **Không tuyên bố hoàn thành trước khi render và kiểm tra từng slide.**

## Spec format (JSON)

```jsonc
{
  "output": "deck.pptx",
  "eyebrow": "Modernization Strategy",   // dòng nhỏ trên mọi slide nội dung (có thể ghi đè theo slide)
  "slides": [
    { "layout": "cover",   "title": "...", "subtitle": "...(optional)", "title_y": 182.9, "size": 50 },
    { "layout": "section", "title": "..." },                   // trang chia mục, giống cover, không số trang
    { "layout": "content", "title": "...", "eyebrow": "...",   // eyebrow tùy chọn, mặc định lấy root
      "body": [ /* blocks */ ],
      "note": "ghi chú chân slide",                            // tùy chọn: đỏ FF0000 đậm nghiêng 14pt
      "note_size": 14, "note_color": "FF0000" },
    { "layout": "thanks",  "title": "THANK YOU!" }             // title căn giữa 50pt trên nền constellation
  ]
}
```

Mỗi slide hỗ trợ `"notes": "speaker notes"`. Layout cũ `agenda` đã bỏ (template không có) — dùng `content` + bullets đánh số hoặc các trang `section`.

### Body blocks (mảng, xếp dọc trong vùng thân 46.7→919pt, y 88→500pt; `"h"` = chiều cao pt, bỏ qua thì tự đo)

| type | tham số chính |
|---|---|
| `bullets` | `items`: [{"t", "lvl" 0/1/2, "bold"}] — 18/16/14pt, bullet `•`, marL 22.5/58.5/94.5pt (hanging 22.5pt); `size` = cỡ lvl0 (mặc định 18) |
| `heading` | `text`, `size` (18 mặc định), đậm slate |
| `infobox` | `cols`: [[{"title", "text"} hoặc {"paras": [...]}], [...]] — hộp nền `#C9EAF7` 12pt, đầu dòng **đậm**; `row_gap` 23.3, `col_gap` 51.5, `fill` |
| `flow` | `nodes`: [{"id", "x", "y", "w" 114, "h" 61.7, "tone" "slate"/"lime"/"outline", "text", "sub": [dòng nghiêng nhỏ], "size" 16}], `edges`: [{"from", "to", "type" "elbow"/"straight", "from_side"/"to_side" "l/r/t/b", "points", "dash", "arrow" true}] — line slate 2.2pt có mũi tên; tọa độ tuyệt đối theo hệ 960×540 |
| `timeline` | `stages`: ["...", ...] — đường ngang x=91→858, chấm tròn `#45546B`, nhãn đậm 18pt phía trên; `y` (mặc định giữa khối), `x0`, `x1`, `label_size` |
| `table` | `header` [], `rows` [[...]], `cols` [tỉ lệ], `align`, `size` (tự chọn 11→8), ô `"^"` = trộn dọc; header nền `#1986AF` chữ trắng đậm, zebra `#C9EAF7`/`#EAF6FC` |
| `image` | `path` (tương đối = theo thư mục spec), fit-giữa khung; `caption` (14pt nghiêng căn giữa dưới ảnh); `callouts`: [{"text", "xy": [x,y], "point": [x,y]}] — nhãn 18pt + đường đứt cam `#FB8635` 1.5pt chỉ vào ảnh (style slide 11) |
| `columns` | `cols`: [block...], `weights`, `gap` — vd. bảng trái + ảnh phải |
| `code` | `panels`: [{"title", "code"}], nền slate `#46546C` bo tròn, chữ sáng, `size` 8, highlight JSON/SQL-ish, `//` = comment |
| `cards` | `groups`: [{"title", "chips": [{"t", "tone" "green"/"blue"/"peach", "lvl", "link"}]}], `legend` — chip tint lime/blue/cam nhạt theo palette theme |

### Inline markup (dùng trong mọi text)

- `**in đậm**`
- `[[red|chữ đỏ]]` — màu: `red` `#D53E23`, `green` `#21B14B`, `orange` `#FB8635`, `teal` `#1986AF`, `tealdark` `#0E5F7E`, `blue` `#0066B3`, `gray` `#7F7F7F`, `white`, `ink` `#445469`, `lime` `#9CB631`, `slate` `#46546C`

## Style tokens (đã hardcode trong gen_deck.py, đo trực tiếp từ Template3.pptx)

| Token | Giá trị | Dùng cho |
|---|---|---|
| Kích thước trang | 13.33 × 7.5 in (960×540pt) | mọi slide |
| Font chữ | **Lato Regular** toàn deck (số trang dùng "Lato"); dự phòng Arial nếu máy thiếu | |
| Màu chữ | `#445469` (theme dk1/dk2) | eyebrow, title, body, nhãn timeline, caption |
| Nền cover/section | `assets/bg_cover.jpg` 1920×1080 full-bleed (navy constellation + rings) | cover, section |
| Nền thanks | `assets/bg_thanks.jpg` 1920×1080 | thanks |
| Cover title | Lato Bold 50pt trắng, box (32.3, 182.9) 626.6×117.9pt anchor giữa; subtitle 14pt trắng box (33.6, 311.7) 749.9×28.4pt | cover/section |
| Section title | giống cover; `THANK YOU!` căn giữa y=228.7 h=71pt | |
| Eyebrow | 12pt `#445469`, box (30.7, 11.8) 388.1×11.6pt | slide nội dung |
| Title nội dung | Lato 32pt `#445469`, box (30.7, 25.8) 872.3×33.5pt, line spacing 90% | slide nội dung |
| 3 ô vuông | roundRect 8.6×7.2pt tại (33.8/48.3/62.8, 63.3), fill `#0066B3`/`#F36F21`/`#22B24C` | slide nội dung |
| Số trang | "Lato" 10pt `#7F7F7F` center (931.6, 508.9) 28.6×28.8pt + vạch `#A6A6A6` 0.7×21.6pt tại (930.4, 512.1); chỉ trên slide content, đánh số tuyệt đối | |
| Note chân slide | 14pt (10–14 tuỳ chọn) **đậm nghiêng** đỏ `#FF0000`, box (8.9, 460) 942×78.4pt anchor đáy; dòng đầu không bullet, các dòng sau `•` | |
| Bullets | `•` Arial, 18/16/14pt theo lvl, marL 22.5/58.5/94.5pt hanging 22.5pt | |
| Infobox | fill `#C9EAF7` (accent2 lum20/80), 12pt slate, gap dọc 23.3pt, gap cột 51.5pt | |
| Flow box | roundRect 114×61.7pt bo 16.7%, line 2.2pt: slate `#46546C` (fill trắng chữ slate cho `outline`, fill slate chữ trắng mặc định), lime `#9CB631` chữ trắng; sub-line nghiêng 11pt | |
| Timeline | line `#8A93A0` 1.5pt x=91→858, chấm `#45546B` r=4.5pt, nhãn đậm 18pt phía trên | |
| Bảng | header `#1986AF` trắng đậm, zebra `#C9EAF7`/`#EAF6FC`, chữ slate | |
| Callout ảnh | đường đứt `#FB8635` 1.5pt (prstDash dash), nhãn 18pt slate | |
| Chips cards | tint `#EFF5DA`/`#D9EDF8`/`#FDE4D0`; legend band `#EDEFF2`; swatch mẫu `#9CB631`/`#1986AF` | |
| Code panel | fill `#46546C`: key `#E06C75`, string `#98C379`, comment `#97A3B3`, số `#D19A66`, thường `#E8ECF1`, Menlo 8pt | |
| Màu nhấn markup | đỏ `#D53E23`, xanh lá `#21B14B`, cam `#FB8635`, xanh dương `#0066B3`, lime `#9CB631` | |

## Quy tắc soạn nội dung

- **Brand-neutral tuyệt đối** — slide không có logo; không chèn logo/thương hiệu công ty nào (kể cả footer, watermark), kể cả khi user cung cấp file logo.
- Eyebrow đặt theo deck ("Modernization Strategy" trong template) — đặt 1 lần ở root `eyebrow`.
- Tiêu đề slide nội dung là cụm ngắn (không bắt buộc đánh số như deck cũ).
- Mật độ: tối đa ~6 bullet/slide hoặc bảng ≤ 12 dòng; 1 slide = 1 ý. Nếu nội dung dày → tách slide.
- Ngôn ngữ slide theo ngôn ngữ người dùng (template gốc tiếng Việt có dấu — Lato hiển thị tốt).
- Ưu tiên infobox/bảng + markup in đậm/màu thay vì đoạn văn dài; điểm cần chú ý dùng `note` đỏ cuối trang.
- Diagram: dùng block `flow`/`timeline` cho đúng style, hoặc sinh ảnh PNG (≥2x) rồi đưa vào `image`/`columns`; ảnh screenshot có thể kèm `callouts` đứt cam.
- Tọa độ `flow`/`callouts` đo theo hệ pt 960×540 (giống template: node 114×61.7pt, cột cách 169.9pt dọc).

## Files

```
slide-kit/
├── SKILL.md                  ← file này
├── assets/                   ← bg_cover.jpg, bg_thanks.jpg (ảnh nền template)
├── scripts/gen_deck.py       ← spec JSON → .pptx (python-pptx)
├── scripts/render_preview.py ← .pptx → PNG từng slide + contact sheet (PowerPoint AppleScript, fallback soffice)
└── examples/deck_spec.json   ← deck mẫu đủ mọi layout/block (kèm example_diagram.png)
```

Yêu cầu môi trường: Python3 + `python-pptx`, `pillow`; macOS + Microsoft PowerPoint để render QA (hoặc LibreOffice). Máy cần font **Lato** để ra đúng chữ (thiếu thì fallback Arial, vẫn giữ layout).

## Mở rộng

- Layout/block mới → thêm renderer vào `BLOCK_RENDERERS` trong gen_deck.py, dùng đúng token màu ở trên; đo đạc vị trí theo pt trên hệ 960×540.
- Đổi artwork nền → thay file trong `assets/` giữ nguyên tên và tỉ lệ 1920×1080.
