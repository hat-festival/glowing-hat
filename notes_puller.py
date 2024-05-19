from pathlib import Path 

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
            if collect:
                if slide_line:
                    notes.append(slide_line)
            if "Notes" in slide_line:
                collect = True

        notes.append("---")

Path(pres_root, "emf-2024", "notes.md").write_text("\n\n".join(notes), encoding="utf-8")