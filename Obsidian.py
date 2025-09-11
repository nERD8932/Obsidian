import re
from pprint import pprint
from pathlib import Path

cwd = Path(r"C:/Users/samir/Downloads/Obsidian/").resolve()
files = {}
for path in cwd.rglob("*"):
    rpath = path.relative_to(cwd)
    if str(rpath)[0] == '.':
        pass
    elif path.suffix.lower() in {".md", ".jpg", ".png"}:
            files[rpath.stem] = rpath

# pprint(files)
# exit(1)

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
        file = files.get(stem.split('/')[-1].split('.')[0], False)
        if file:
            updated = f"![{stem}](/{str(file).replace('\\', '/').replace(" ", "%20")})"
            return updated
        else:
            return stem
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