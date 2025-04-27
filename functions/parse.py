# --- functions/parse.py ---
import re

def parse_coordinates(text):
    tokens = re.split(r'[\s\n]+', text.strip())
    coords = []
    i = 0
    while i < len(tokens):
        token = tokens[i]

        # --- Nhận dạng mã hiệu E/N ---
        if re.fullmatch(r"[EN]\d{8}", token):
            x, y = None, None
            prefix = token[0]
            number = token[1:]
            if prefix == "E":
                y = int(number)
            else:
                x = int(number)

            if i+1 < len(tokens) and re.fullmatch(r"[EN]\d{8}", tokens[i+1]):
                next_prefix = tokens[i+1][0]
                next_number = tokens[i+1][1:]
                if next_prefix == "E":
                    y = int(next_number)
                else:
                    x = int(next_number)
                i += 1

            if x is not None and y is not None:
                coords.append(["", float(x), float(y), 0])
            i += 1
            continue

        # --- Nếu có 4 token liên tiếp (STT X Y Z) ---
        if i + 3 < len(tokens):
            stt = tokens[i]
            try:
                x = float(tokens[i+1].replace(",", "."))
                y = float(tokens[i+2].replace(",", "."))
                h = float(tokens[i+3].replace(",", "."))
                coords.append([stt, x, y, h])
                i += 4
                continue
            except:
                pass

        # --- Nếu chỉ có 2 hoặc 3 token (X Y [Z]) ---
        chunk = []
        for _ in range(3):
            if i < len(tokens):
                try:
                    chunk.append(float(tokens[i].replace(",", ".")))
                except:
                    break
                i += 1
        if len(chunk) == 2:
            chunk.append(0.0)
        if len(chunk) == 3:
            coords.append(["", chunk[0], chunk[1], chunk[2]])
        else:
            i += 1

    # --- Lọc hợp lệ ---
    filtered = []
    for ten_diem, x, y, h in coords:
        if 500_000 <= x <= 2_650_000 and 330_000 <= y <= 670_000 and -1000 <= h <= 3200:
            filtered.append([ten_diem, x, y, h])
    return filtered