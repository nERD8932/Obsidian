import re
from pprint import pprint
from pathlib import Path

cwd = Path(r"C:/Users/samir/Downloads/Obsidian/").resolve()
files = {}

for path in cwd.rglob("*"):
    if path.is_dir():
        continue
    rpath = path.relative_to(cwd)
    # skip hidden files/folders anywhere in the path
    if any(part.startswith(".") for part in rpath.parts):
        continue
    if path.suffix.lower() == ".md":
        files[rpath.stem] = rpath
    elif path.suffix.lower() in {".md", ".jpg", ".jpeg", ".png"}:
        files[rpath.name] = rpath

def update_md_format(match):
    text = match.group()
    stem = text[2:-2]
    if stem[0] == '.' or stem[0] == '/':
        stem = stem.split('/')[-1].split('|')[0].split('.')[0]
 
    file = files.get(stem, False)
    if file:
        updated = f"[{stem}](/{str(file).replace('\\', '/').replace('..', '').replace(" ", "%20")})"
        return updated
    else:
        return stem

def update_img_format(match):
    text = match.group()
    if '![[' in text:
        stem = text[3:-2]
        file = files.get(stem.split('/')[-1], False)
        if file:
            updated = f"![{stem}](/{str(file).replace('\\', '/').replace(" ", "%20")})"
            return updated
        else:
            return stem.split('.')[0]
    else:
        return text.replace('..', '').replace(' ', '%20')

# file: pathlib.WindowsPath  
for file in files.values():
    if file.suffix.lower() == '.md':
        try:
            print()
            print(file.name)
            print()
            with open(Path(cwd, file), 'r+', encoding="utf-8") as f:
                contents = f.read()
                replaced_img = re.sub(r"!\[\[([^\]]*)\]\]|!\[([^\]]*)\]\(([^)]*)\)", update_img_format, contents)
                repalced_mds = re.sub(r"\[\[.*?\]\]", update_md_format, replaced_img)
                print(repalced_mds)
                f.seek(0)
                f.write(repalced_mds)
                f.truncate()
        except Exception as e:
            print(f"Error occured for file: {file}")
            raise e