#!/usr/bin/env python3
"""Convert Google Sites HTML tutorials to clean Markdown files."""

import os
import re
import shutil
from html import unescape
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path("/home/tngai/data/Tutorials")
SOURCE_DIR = BASE_DIR / "old tutorials" / "DIGITAL FUTURES - GIS" / "DRAFT"
OUTPUT_DIR = BASE_DIR / "_tutorials"
ASSETS_DIR = BASE_DIR / "assets" / "images"

# Tutorial metadata
TUTORIALS = {
    "Digital Topography": {
        "title": "Digital Topography",
        "subtitle": "Processing and visualizing elevation data for design contexts",
        "tools": ["QGIS", "Rhino 7", "3DS Max"],
        "difficulty": "intermediate",
        "date": "2022-03-15",
    },
    "Drought": {
        "title": "Drought Analysis",
        "subtitle": "Analyzing drought patterns using satellite data",
        "tools": ["QGIS"],
        "difficulty": "beginner",
        "date": "2022-04-01",
    },
    "Ecological Analysis": {
        "title": "Ecological Analysis",
        "subtitle": "GIS-based ecological assessment methods",
        "tools": ["QGIS"],
        "difficulty": "intermediate",
        "date": "2022-04-10",
    },
    "Home": {
        "title": "GIS Tutorials Home",
        "subtitle": "Overview of Pratt Digital Futures GIS curriculum",
        "tools": [],
        "difficulty": "beginner",
        "date": "2022-01-01",
    },
    "Indexed Image": {
        "title": "Indexed Image Analysis",
        "subtitle": "Working with indexed color images in GIS",
        "tools": ["QGIS", "Adobe Photoshop"],
        "difficulty": "intermediate",
        "date": "2022-05-01",
    },
    "Land Cover": {
        "title": "Land Cover Classification",
        "subtitle": "Classifying land cover types from satellite imagery",
        "tools": ["QGIS"],
        "difficulty": "intermediate",
        "date": "2022-05-15",
    },
    "LiDAR Processing": {
        "title": "LiDAR Processing",
        "subtitle": "Processing LiDAR point cloud data for 3D modeling",
        "tools": ["QGIS", "Rhino 7", "3DS Max"],
        "difficulty": "advanced",
        "date": "2022-06-01",
    },
    "Meteor": {
        "title": "Meteor Impact Analysis",
        "subtitle": "Analyzing meteor crater topography",
        "tools": ["QGIS"],
        "difficulty": "intermediate",
        "date": "2022-06-15",
    },
    "Mineral Resources": {
        "title": "Mineral Resources Mapping",
        "subtitle": "Mapping mineral deposits using remote sensing",
        "tools": ["QGIS"],
        "difficulty": "intermediate",
        "date": "2022-07-01",
    },
    "Multidimensional Data": {
        "title": "Multidimensional Data",
        "subtitle": "Working with multidimensional raster datasets",
        "tools": ["QGIS"],
        "difficulty": "advanced",
        "date": "2022-07-15",
    },
    "Multispectral Imagery": {
        "title": "Multispectral Imagery",
        "subtitle": "Analyzing multispectral satellite data for land studies",
        "tools": ["QGIS"],
        "difficulty": "intermediate",
        "date": "2022-08-01",
    },
    "NASA Earth Observations": {
        "title": "NASA Earth Observations",
        "subtitle": "Accessing and visualizing NASA satellite data",
        "tools": ["QGIS"],
        "difficulty": "beginner",
        "date": "2022-08-15",
    },
    "NYC Building Activities": {
        "title": "NYC Building Activities",
        "subtitle": "Analyzing building construction activity in New York City",
        "tools": ["QGIS"],
        "difficulty": "intermediate",
        "date": "2022-09-01",
    },
    "Photogrammetry": {
        "title": "Photogrammetry",
        "subtitle": "Creating 3D models from photographic data",
        "tools": ["QGIS", "Rhino 7", "3DS Max", "Reality Capture"],
        "difficulty": "advanced",
        "date": "2022-09-15",
    },
    "Sea Level Rise": {
        "title": "Sea Level Rise",
        "subtitle": "Modeling sea level rise impacts on coastal areas",
        "tools": ["QGIS"],
        "difficulty": "intermediate",
        "date": "2022-10-01",
    },
    "Solar Potential": {
        "title": "Solar Potential Analysis",
        "subtitle": "Assessing solar energy potential using GIS data",
        "tools": ["QGIS"],
        "difficulty": "intermediate",
        "date": "2022-10-15",
    },
    "Storm Surge Modeling": {
        "title": "Storm Surge Modeling",
        "subtitle": "Modeling storm surge scenarios for coastal planning",
        "tools": ["QGIS"],
        "difficulty": "advanced",
        "date": "2022-11-01",
    },
    "Urban Heat Island Effect": {
        "title": "Urban Heat Island Effect",
        "subtitle": "Analyzing urban heat patterns using thermal imagery",
        "tools": ["QGIS"],
        "difficulty": "intermediate",
        "date": "2022-11-15",
    },
}


def slugify(name):
    """Convert tutorial name to slug."""
    return name.lower().replace(" ", "-")


def extract_youtube_videos(content):
    """Extract YouTube video IDs and labels from iframe embeds."""
    videos = []
    pattern = r'<iframe[^>]*aria-label="YouTube Video, ([^"]+)"[^>]*src="https://www\.youtubeeducation\.com/embed/([a-zA-Z0-9_-]+)'
    for match in re.finditer(pattern, content):
        label = unescape(match.group(1))
        video_id = match.group(2)
        videos.append({"label": label, "id": video_id})
    return videos


def extract_images_from_folder(folder_path):
    """Get all image files from a tutorial's companion folder."""
    images = []
    if not folder_path.exists():
        return images
    for f in sorted(folder_path.iterdir()):
        if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
            images.append(f)
    return images


def extract_content_sections(content):
    """Extract content sections from Google Sites HTML using BeautifulSoup."""
    soup = BeautifulSoup(content, "html.parser")
    sections = []

    # Find all content elements with class zfr3Q (Google Sites text class)
    # Can be h1, h2, h3, p elements
    content_elements = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p"])

    for el in content_elements:
        classes = " ".join(el.get("class", []))
        if "zfr3Q" not in classes:
            continue

        text = el.get_text(strip=True)
        if not text or len(text) < 2:
            continue

        # Extract links from within the element
        links = []
        for a in el.find_all("a", href=True):
            href = a.get("href", "")
            link_text = a.get_text(strip=True)
            if "google.com/url" in href:
                match = re.search(r"q=([^&]+)", href)
                if match:
                    href = unescape(match.group(1))
            if href.startswith("http") and link_text:
                links.append({"text": link_text, "href": href})

        # Determine section type
        if "duRjpb" in classes or el.name == "h1":
            sections.append({"type": "title", "text": text})
        elif "JYVBee" in classes or el.name in ("h2", "h3", "h4", "h5", "h6"):
            sections.append({"type": "heading", "text": text})
        elif "OmQG5e" in classes or "NHD4Gf" in classes:
            sections.append({"type": "heading", "text": text})
        else:
            sections.append({"type": "text", "text": text, "links": links})

    return sections


def copy_and_rename_images(tutorial_name, slug, image_files):
    """Copy images to assets directory with descriptive names."""
    dest_dir = ASSETS_DIR / slug
    dest_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    for i, img_path in enumerate(image_files):
        ext = img_path.suffix.lower()
        if len(image_files) == 1:
            new_name = f"{slug}-header{ext}"
        else:
            new_name = f"{slug}-{i + 1:02d}{ext}"

        dest = dest_dir / new_name
        shutil.copy2(img_path, dest)
        copied.append(new_name)

    return copied


def format_text_with_links(text, links):
    """Replace link text with markdown links."""
    result = text
    for link in links:
        link_text = link["text"]
        link_href = link["href"]
        md_link = f"[{link_text}]({link_href})"
        # Replace the plain text with the markdown link
        result = result.replace(link_text, md_link)
    return result


def generate_markdown(tutorial_name, meta, sections, videos, image_names, slug):
    """Generate clean Markdown with YAML frontmatter."""
    lines = []

    # YAML Frontmatter
    lines.append("---")
    lines.append(f'title: "{meta["title"]}"')
    lines.append(f'subtitle: "{meta["subtitle"]}"')
    lines.append(f'date: "{meta["date"]}"')
    lines.append("category: GIS")
    if meta["tools"]:
        tools_str = ", ".join(f'"{t}"' for t in meta["tools"])
        lines.append(f"tools: [{tools_str}]")
    else:
        lines.append("tools: []")
    lines.append(f'difficulty: "{meta["difficulty"]}"')
    if videos:
        vid_ids = ", ".join(f'"{v["id"]}"' for v in videos)
        lines.append(f"youtube_ids: [{vid_ids}]")
    else:
        lines.append("youtube_ids: []")
    if image_names:
        lines.append(f'thumbnail: "../assets/images/{slug}/{image_names[0]}"')
    else:
        lines.append("thumbnail: ''")
    lines.append("---")
    lines.append("")

    # Title
    lines.append(f"# {meta['title']}")
    lines.append("")

    # YouTube Videos Section
    if videos:
        lines.append("## Video Tutorials")
        lines.append("")
        for v in videos:
            lines.append(f"[{v['label']}](https://www.youtube.com/watch?v={v['id']})")
            lines.append("")
        lines.append("---")
        lines.append("")

    # Hero image
    if image_names:
        lines.append(f"![{meta['title']}](../assets/images/{slug}/{image_names[0]})")
        lines.append("")

    # Content sections
    for section in sections:
        if section["type"] == "title":
            # Skip the title since we already have it in frontmatter
            continue
        elif section["type"] == "heading":
            text = section["text"]
            # Skip tool names that appear as bold items in a tools list
            lines.append(f"## {text}")
            lines.append("")
        elif section["type"] == "text":
            text = section["text"]
            links = section.get("links", [])
            if links:
                text = format_text_with_links(text, links)
            lines.append(text)
            lines.append("")

    return "\n".join(lines)


def process_tutorial(html_file, folder_name):
    """Process a single tutorial HTML file."""
    slug = slugify(folder_name)
    meta = TUTORIALS.get(
        folder_name,
        {
            "title": folder_name,
            "subtitle": "",
            "tools": ["QGIS"],
            "difficulty": "intermediate",
            "date": "2022-01-01",
        },
    )

    print(f"\nProcessing: {folder_name} -> {slug}.md")

    # Read HTML content
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract components
    videos = extract_youtube_videos(content)
    print(f"  Found {len(videos)} YouTube videos")

    sections = extract_content_sections(content)
    print(f"  Found {len(sections)} content sections")

    # Copy images
    img_folder = SOURCE_DIR / folder_name
    image_files = extract_images_from_folder(img_folder)
    image_names = []
    if image_files:
        image_names = copy_and_rename_images(folder_name, slug, image_files)
        print(f"  Copied {len(image_names)} images")

    # Generate markdown
    md_content = generate_markdown(
        folder_name, meta, sections, videos, image_names, slug
    )

    # Write output
    output_file = OUTPUT_DIR / f"{slug}.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"  Written: {output_file}")

    return {
        "name": folder_name,
        "slug": slug,
        "videos": len(videos),
        "sections": len(sections),
        "images": len(image_names),
    }


def main():
    """Process all HTML tutorials."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    results = []

    for html_file in sorted(SOURCE_DIR.glob("*.html")):
        folder_name = html_file.stem
        result = process_tutorial(html_file, folder_name)
        results.append(result)

    # Summary
    print("\n" + "=" * 60)
    print("CONVERSION SUMMARY")
    print("=" * 60)
    total_videos = 0
    total_images = 0
    for r in results:
        print(
            f"  {r['slug']:30s} | {r['sections']:3d} sections | {r['videos']:2d} videos | {r['images']:3d} images"
        )
        total_videos += r["videos"]
        total_images += r["images"]
    print("-" * 60)
    print(
        f"  TOTAL: {len(results)} tutorials, {total_videos} videos, {total_images} images"
    )
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print(f"Assets directory: {ASSETS_DIR}")


if __name__ == "__main__":
    main()
