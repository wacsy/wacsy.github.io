from bs4 import BeautifulSoup
import cssutils
import os

def get_css_files(root_path):
    css_files = []
    for dirpath, _, filenames in os.walk(root_path):
        for file in filenames:
            if file.endswith(".css"):
                # relative_path = os.path.relpath(os.path.join(dirpath, file), root_path)
                relative_path = os.path.join(dirpath, file)
                css_files.append(relative_path)
    return css_files

def get_using_cla(html_path="_site/index.html"):
    used_classes = set()
    with open(html_path) as f:
        soup = BeautifulSoup(f, "html.parser")
        for tag in soup.find_all(True):
            classes = tag.get("class")
            if classes:
                used_classes.update(classes)
    return used_classes

def get_style_css(css_path="_site/css/main.css"):
    parser = cssutils.CSSParser()
    stylesheet = parser.parseFile(css_path)
    cleaned_css = ""

    for rule in stylesheet:
        if rule.type == rule.STYLE_RULE:
            selectors = rule.selectorText.split(",")
            keep = False
            for sel in selectors:
                sel = sel.strip()
                if sel.startswith(".") and sel[1:] in used_classes:
                    keep = True
            if keep:
                cleaned_css += rule.cssText + "\n"
    return cleaned_css

# 示例用法
if __name__ == "__main__":
    used_classes = get_using_cla()

    path = "./_site/css"  # 替换为你的目录路径
    css_paths = get_css_files(path)
    cleaned_css = ""
    for p in css_paths:
        if not "cleaned" in p:
            cleaned_css += get_style_css(p) + "\n"

    with open("cleaned.css", "w") as out:
        out.write(cleaned_css)
