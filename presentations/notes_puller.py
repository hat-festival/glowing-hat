from pathlib import Path

import markdown

SCROLL_AMOUNT = 7

pres_root = "presentations/reveal.js"

lines = Path(pres_root, "index.html").read_text(encoding="utf-8").split("\n")

notes = []

for line in lines:
    if "emf-2024/slides" in line and "<!--" not in line:
        slide_path = line.split('"')[1]
        slide_text = Path(pres_root, slide_path).read_text(encoding="utf-8").split("\n")
        title = slide_text[0]
        notes.append(title)

        collect = False

        for slide_line in slide_text:
            if collect and slide_line:
                notes.append(slide_line)
            if "Notes" in slide_line:
                collect = True

        # notes.append("---")

template = Path(pres_root, "notes.template").read_text(encoding="utf-8")
pres = template.replace("CONTENT_HERE", markdown.markdown("\n\n".join(notes)))
pres = pres.replace("SCROLL_AMOUNT", str(SCROLL_AMOUNT))
Path(pres_root, "notes.html").write_text(pres, encoding="utf-8")
