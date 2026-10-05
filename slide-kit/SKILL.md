---
name: slide-kit
description: Generate .pptx slide decks in the navy-and-teal corporate tech style extracted from FRT_Vaccine_Approach_Phase1.pdf (dark navy gradient cover/agenda/closing with lightning artwork, 60pt navy header band + white title on white content slides, teal-headed zebra tables, mint/blue sitemap cards, rounded code panels). Use whenever the user asks to create slides/deck/pptx "theo style này", "giống deck Phase1/Vaccine", or loads this kit. Brand-neutral - never insert company logos or brand assets.
---

# Slide kit — navy/teal corporate deck generator

Bộ tool sinh file `.pptx` đúng chuẩn style được trích xuất từ deck tham chiếu: nền navy gradient có artwork tia sét cho slide mở đầu/mục lục/kết thúc, dải header navy + tiêu đề trắng cho slide nội dung, bảng header teal zebra, thẻ sitemap xanh lá/xanh dương, panel code bo tròn. **Kit không chứa logo/thương hiệu** — không được thêm logo nào vào slide.

## Quick start

```bash
python3 <skill_dir>/scripts/gen_deck.py spec.json -o deck.pptx
python3 <skill_dir>/scripts/gen_deck.py <skill_dir>/examples/deck_spec.json -o /tmp/example_deck.pptx
```

QA bắt buộc trước khi giao (render từng slide bằng PowerPoint thật rồi soi từng trang):

```bash
python3 <skill_dir>/scripts/render_preview.py deck.pptx --output-dir /tmp/deck_preview
```

Mở `contact-sheet.jpg` và từng `slide-NN.png`, kiểm tra: text tràn khung/chồng lấn, bảng quá dài, chip/cột lệch, ảnh méo. Sửa spec → gen lại → render lại, đến khi sạch mới giao. **Không tuyên bố hoàn thành trước khi render và kiểm tra từng slide.**

## Spec format (JSON)

```jsonc
{
  "output": "deck.pptx",
  "slides": [
    { "layout": "cover",   "title": "...", "subtitle": "...(optional)", "date": "OCT 29 2026", "title_y": 200, "size": 48 },
    { "layout": "agenda",  "items": ["...", "..."] },          // tự đánh số 01, 02, ...
    { "layout": "content", "title": "1. Section", "body": [ /* blocks */ ],
      "note": "ghi chú chân slide", "note_color": "E02020" },  // note tùy chọn
    { "layout": "thanks",  "title": "THANK YOU", "subtitle": "..." }
  ]
}
```

Mỗi slide hỗ trợ `"notes": "speaker notes"`.

### Body blocks (mảng, xếp dọc trong vùng thân slide; `"h"` = chiều cao pt, bỏ qua thì chia đều)

| type | tham số chính |
|---|---|
| `bullets` | `items`: [{"t": "...", "lvl": 0/1/2, "bold": bool}], `size` 8–12 |
| `heading` | `text`, `size` (16 mặc định) |
| `table` | `header` [], `rows` [[...]], `cols` [tỉ lệ], `align`, `size` (tự chọn 10/9/8), ô `"^"` = trộn dọc với ô trên; trong ô: xuống dòng `\n`, đầu dòng `- `/`o ` |
| `image` | `path` (tương đối = theo thư mục spec), fit-git giữa khung |
| `columns` | `cols`: [block...], `weights`: [0.42, 0.58], `gap` — vd. bảng trái + ảnh phải |
| `code` | `panels`: [{`title`, `code`}], `size` 8, syntax highlight tự động cho JSON/SQL-ish, `//` = comment |
| `cards` | `groups`: [{`title`, `chips`: [{"t", "tone": "green"/"blue"/"peach", "lvl", "link": bool}]}], `legend`: {"label", "swatches": [["92D050","Phase 1"],["73B5FF","Phase 2"]]} |

### Inline markup (dùng trong mọi text)

- `**in đậm**`
- `[[red|chữ đỏ]]` — màu: `red green orange teal tealdark blue gray white ink`

## Style tokens (đã hardcode trong gen_deck.py)

| Token | Giá trị | Dùng cho |
|---|---|---|
| Nền navy | gradient ngang `#003877 → #02275F` (đạt đích ở 42% ngang) | cover/agenda/thanks (asset nền đã compose sẵn) |
| Header band | ảnh `assets/header_band.jpg`, cao 60pt, title Calibri Bold 24pt trắng, x=26pt | mọi slide nội dung |
| Màu chữ | `#29333A` | body text |
| Teal | `#32B2C1` | header bảng, nhấn |
| Zebra | `#E8F2F4` / `#CDE4E9` | dòng bảng xen kẽ |
| Chip xanh/xanh dương | `#A7FFCF` / `#C9DCFF`; legend `#92D050` / `#73B5FF`; dải legend `#D9D9D9` | sitemap cards |
| Cảnh báo / nhấn | đỏ `#E02020`, cam `#F88728`, xanh lá `#00B050`, peach `#FDE0C0` | markup trong bảng/bullet |
| Viền/đường | `#BFBFBF` card, `#2E75B6` code panel, `#2E6FBE` pill agenda | |
| Code | Menlo 8pt: key `#E06C75`, string `#98C379`, comment `#7F848E`, số `#D19A66`, thường `#3B4249` | |
| Font chữ | Calibri (dự phòng Arial nếu máy thiếu), ngày tháng trên bìa Segoe UI 16pt | |
| Kích thước trang | 13.33 × 7.5 in (960×540pt) | |
| Cover title | Calibri Bold 48pt trắng, x=70pt y≈200pt; date pill pill-tròn 172×38pt x=72 y=472 (fill trắng 14.5%, viền trắng 25%) | |
| Agenda | số + pill viền xanh 347×30pt, step ≈46.6pt từ y=24 | |
| Số trang | xám `#7F7F7F` 10pt góc phải-dưới, bắt đầu từ slide agenda | |

## Quy tắc soạn nội dung

- **Không logo, không thương hiệu** — kể cả footer, header, watermark. Kit vốn đã brand-neutral.
- Tiêu đề slide nội dung đánh số theo mục (`"1. ..."`, `"2. ..."`) giống pattern deck gốc.
- Mật độ: tối đa ~6 bullet/slide hoặc bảng ≤ 12 dòng 8pt; 1 slide = 1 ý. Nếu nội dung dày → tách slide.
- Ngôn ngữ slide theo ngôn ngữ người dùng (deck gốc là tiếng Việt có dấu — Calibri hiển thị tốt).
- Ưu tiên bảng + markup in đậm/màu thay vì đoạn văn dài; số liệu quan trọng dùng `**bold**` hoặc `[[red|...]]`.
- Diagram: sinh ảnh PNG (Mermaid/graphviz/draw.io) rồi đưa vào block `image` hoặc `columns`; không dùng screenshot chất lượng thấp (≥ 2x mới dùng).
- Giữ ảnh trong khung: đã auto fit-giữa; nếu ảnh quá dọc/quá ngang thì crop ngoài hoặc đổi sang slide riêng.

## Files

```
slide-kit/
├── SKILL.md                  ← file này
├── assets/                   ← nền navy brand-neutral: bg_cover, bg_agenda (đồ họa constellation+rings sinh tự động), bg_thanks (waves), header_band (.jpg)
├── scripts/gen_deck.py       ← spec JSON → .pptx (python-pptx)
├── scripts/render_preview.py ← .pptx → PNG từng slide + contact sheet (PowerPoint AppleScript, fallback soffice)
├── scripts/build_assets.py   ← sinh lại nền cover/agenda (đồ họa trung lập, seed cố định) — chạy khi muốn đổi artwork
└── examples/deck_spec.json   ← deck mẫu đủ mọi layout (kèm example_diagram.png)
```

Yêu cầu môi trường: Python3 + `python-pptx`, `pillow`, `pymupdf` (chỉ render_preview cần pymupdf), macOS + Microsoft PowerPoint để render QA (hoặc LibreOffice).

## Mở rộng

- Layout mới → thêm renderer vào `BLOCK_RENDERERS` trong gen_deck.py, dùng đúng token màu ở trên; đo đạc vị trí theo pt trên hệ 960×540.
- Đổi artwork nền → thay file trong `assets/` giữ nguyên tên và tỉ lệ 1920×1080 (band: 1920×120).
