import requests
from bs4 import BeautifulSoup


def decode_secret_message(url):
    html = requests.get(url, timeout=30).text
    rows = BeautifulSoup(html, "html.parser").find("table").find_all("tr")

    # Map column names from the header row so column order doesn't matter
    header = [c.get_text(strip=True).lower() for c in rows[0].find_all(["td", "th"])]
    x_col = next(i for i, h in enumerate(header) if h.startswith("x"))
    y_col = next(i for i, h in enumerate(header) if h.startswith("y"))
    char_col = next(i for i, h in enumerate(header) if "char" in h)

    points = {}
    for row in rows[1:]:
        cells = [c.get_text() for c in row.find_all(["td", "th"])]
        if len(cells) < 3:
            continue
        x, y = int(cells[x_col].strip()), int(cells[y_col].strip())
        points[(x, y)] = cells[char_col].strip() or " "

    max_x = max(x for x, _ in points)
    max_y = max(y for _, y in points)

    # y increases upward, so print from the top row (max_y) down to 0
    for y in range(max_y, -1, -1):
        print("".join(points.get((x, y), " ") for x in range(max_x + 1)))


decode_secret_message("https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub")