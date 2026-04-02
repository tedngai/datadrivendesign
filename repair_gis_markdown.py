#!/usr/bin/env python3

import re
import shutil
from html import unescape
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from bs4 import BeautifulSoup, NavigableString, Tag


BASE_DIR = Path("/home/tngai/data/Tutorials")
SOURCE_DIR = BASE_DIR / "old tutorials" / "DIGITAL FUTURES - GIS" / "DRAFT"
OUTPUT_DIR = BASE_DIR / "_tutorials"
ASSETS_DIR = BASE_DIR / "assets" / "images"

TUTORIALS = [
    "Digital Topography",
    "Drought",
    "Ecological Analysis",
    "Home",
    "Indexed Image",
    "Land Cover",
    "LiDAR Processing",
    "Meteor",
    "Mineral Resources",
    "Multidimensional Data",
    "Multispectral Imagery",
    "NASA Earth Observations",
    "NYC Building Activities",
    "Photogrammetry",
    "Sea Level Rise",
    "Solar Potential",
    "Storm Surge Modeling",
    "Urban Heat Island Effect",
]


def slugify(name: str) -> str:
    return name.lower().replace(" ", "-")


def decode_google_url(href: str) -> str:
    if "google.com/url" not in href:
        return href
    query = parse_qs(urlparse(href).query)
    if "q" in query and query["q"]:
        return query["q"][0]
    return href


def collapse_spaces(text: str) -> str:
    text = unescape(text).replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:?!])", r"\1", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    return text.strip()


def render_inline(node) -> str:
    if isinstance(node, NavigableString):
        return str(node)
    if not isinstance(node, Tag):
        return ""
    if node.name == "br":
        return "\n"
    if node.name == "a":
        href = decode_google_url(node.get("href", "").strip())
        label = collapse_spaces(
            "".join(render_inline(child) for child in node.children)
        )
        if href and label:
            return f"[{label}]({href})"
        return label
    return "".join(render_inline(child) for child in node.children)


def get_root(soup: BeautifulSoup) -> Tag:
    return soup.find(attrs={"jsname": "ZBtY8b"}) or soup.body or soup


def is_content_tag(tag: Tag) -> bool:
    if tag.find_parent(["header", "nav", "script", "style"]):
        return False
    if tag.name == "p" and tag.find_parent("li"):
        return False
    if tag.name in {"h1", "h2", "h3", "h4", "h5", "h6", "p"}:
        return "zfr3Q" in tag.get("class", [])
    if tag.name == "li":
        return True
    if tag.name == "iframe":
        return "embed/" in tag.get("src", "")
    if tag.name == "img":
        src = unquote(tag.get("src", ""))
        return bool(src) and src.lower().endswith(
            (".jpg", ".jpeg", ".png", ".gif", ".webp")
        )
    return False


def collect_image_map(root: Tag, tutorial_name: str, slug: str) -> dict[str, str]:
    source_dir = SOURCE_DIR / tutorial_name
    source_files = (
        {
            file.name: file
            for file in sorted(source_dir.iterdir())
            if file.is_file()
            and file.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp"}
        }
        if source_dir.exists()
        else {}
    )

    ordered = []
    seen = set()
    for img in root.find_all("img"):
        src = unquote(img.get("src", ""))
        name = Path(src).name
        if name in source_files and name not in seen:
            seen.add(name)
            ordered.append(name)

    for name in source_files:
        if name not in seen:
            ordered.append(name)

    out_dir = ASSETS_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    mapping = {}
    for idx, name in enumerate(ordered, start=1):
        src = source_files[name]
        ext = src.suffix.lower()
        dest_name = f"{slug}-{idx:02d}{ext}"
        shutil.copy2(src, out_dir / dest_name)
        mapping[name] = dest_name
    return mapping


def extract_video_link(tag: Tag) -> str | None:
    src = tag.get("src", "")
    match = re.search(r"/embed/([A-Za-z0-9_-]+)", src)
    if not match:
        return None
    video_id = match.group(1)
    label = tag.get("aria-label", "YouTube Video")
    label = re.sub(r"^YouTube Video,\s*", "", label).strip() or "YouTube Video"
    return f"[{label}](https://www.youtube.com/watch?v={video_id})"


def build_body(html_path: Path, tutorial_name: str, title: str) -> tuple[str, str]:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    root = get_root(soup)
    slug = slugify(tutorial_name)
    image_map = collect_image_map(root, tutorial_name, slug)

    lines = [f"# {title}", ""]
    emitted_images = set()

    for tag in root.find_all(
        ["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "iframe", "img"]
    ):
        if not is_content_tag(tag):
            continue

        if tag.name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            text = collapse_spaces(render_inline(tag))
            if not text:
                continue
            if tag.name == "h1":
                continue
            level = min(int(tag.name[1]), 4)
            lines.extend([f"{'#' * level} {text}", ""])
            continue

        if tag.name == "p":
            text = collapse_spaces(render_inline(tag))
            if text:
                lines.extend([text, ""])
            continue

        if tag.name == "li":
            text = collapse_spaces(render_inline(tag))
            if text:
                lines.extend([f"- {text}", ""])
            continue

        if tag.name == "iframe":
            link = extract_video_link(tag)
            if link:
                lines.extend([link, ""])
            continue

        if tag.name == "img":
            src = unquote(tag.get("src", ""))
            name = Path(src).name
            if name not in image_map or name in emitted_images:
                continue
            emitted_images.add(name)
            alt = collapse_spaces(tag.get("alt", "")) or title
            lines.extend([f"![{alt}](../assets/images/{slug}/{image_map[name]})", ""])

    body = "\n".join(lines).strip() + "\n"
    thumbnail = (
        f"../assets/images/{slug}/{next(iter(image_map.values()))}" if image_map else ""
    )
    return body, thumbnail


def split_markdown(text: str) -> tuple[str, str, str]:
    match = re.match(r"^---\n.*?\n---\n", text, re.S)
    if not match:
        raise ValueError("Missing frontmatter")
    frontmatter = match.group(0)
    rest = text[match.end() :]
    lines = rest.splitlines(keepends=True)

    resources_idx = None
    for idx, line in enumerate(lines):
        if line.strip() == "## Resources & Further Reading":
            resources_idx = idx

    if resources_idx is None:
        body_start = re.search(r"(?m)^# ", rest)
        if not body_start:
            return frontmatter, rest, ""
        prefix = rest[: body_start.start()]
        body = rest[body_start.start() :]
        return frontmatter, prefix, body

    saw_resource_item = False
    split_idx = len(lines)
    for idx in range(resources_idx + 1, len(lines)):
        stripped = lines[idx].strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            saw_resource_item = True
            continue
        if saw_resource_item:
            split_idx = idx
            break

    prefix = "".join(lines[:split_idx])
    body = "".join(lines[split_idx:])
    return frontmatter, prefix, body


def set_thumbnail(frontmatter: str, thumbnail: str) -> str:
    replacement = f'thumbnail: "{thumbnail}"' if thumbnail else 'thumbnail: ""'
    if re.search(r"(?m)^thumbnail:.*$", frontmatter):
        return re.sub(r"(?m)^thumbnail:.*$", replacement, frontmatter)
    return frontmatter.rstrip() + "\n" + replacement + "\n"


def extract_title(frontmatter: str) -> str:
    match = re.search(r'(?m)^title:\s*"([^"]+)"', frontmatter)
    if match:
        return match.group(1)
    match = re.search(r"(?m)^title:\s*(.+)$", frontmatter)
    if match:
        return match.group(1).strip().strip('"')
    raise ValueError("Missing title field")


def repair_tutorial(tutorial_name: str) -> None:
    slug = slugify(tutorial_name)
    md_path = OUTPUT_DIR / f"{slug}.md"
    html_path = SOURCE_DIR / f"{tutorial_name}.html"
    original = md_path.read_text(encoding="utf-8")
    frontmatter, prefix, _old_body = split_markdown(original)
    title = extract_title(frontmatter)
    new_body, thumbnail = build_body(html_path, tutorial_name, title)
    frontmatter = set_thumbnail(frontmatter, thumbnail)
    md_path.write_text(frontmatter + prefix + new_body, encoding="utf-8")


def main() -> None:
    for tutorial_name in TUTORIALS:
        repair_tutorial(tutorial_name)
        print(f"Repaired {slugify(tutorial_name)}.md")


if __name__ == "__main__":
    main()
