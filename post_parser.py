#!/usr/bin/env python3
import sys
import os
import re
import shutil
from datetime import date
from pathlib import Path

def format_title(filename: str) -> str:
    """Convert filename like 'windows-pe-analysis.md' to 'Windows PE Analysis'"""
    name = Path(filename).stem
    return " ".join(word.capitalize() for word in name.replace("-", " ").split())

def update_markdown_image_paths(content: str, folder_name: str) -> str:
    """Update standard markdown image paths."""
    pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
    
    def replacer(match):
        alt_text, path = match.groups()
        if not (path.startswith("http://") or path.startswith("https://") or "/" in path):
            return f"![{alt_text}]({folder_name}/{path})"
        return match.group(0)
    
    return pattern.sub(replacer, content)

def find_image_file(md_parent: Path, raw_name: str, folder_path: Path) -> Path:
    """
    Try to locate the image file:
    1. md_parent / raw_name
    2. folder_path / raw_name (if image already inside created folder)
    3. recursive search under md_parent for a file with the same basename
    Returns Path or None
    """
    candidates = [
        md_parent / raw_name,
        folder_path / raw_name,
    ]

    for c in candidates:
        if c.exists():
            return c

    # Recursive search under md_parent (use case: image in a subfolder, or slightly different spacing)
    # Match by exact name first, then case-insensitive fallback
    for p in md_parent.rglob(raw_name):
        if p.is_file():
            return p

    # Case-insensitive search fallback: compare names ignoring case
    lower_raw = raw_name.lower()
    for p in md_parent.rglob('*'):
        if p.is_file() and p.name.lower() == lower_raw:
            return p

    return None

def process_obsidian_images(content: str, folder_name: str, folder_path: Path, md_parent: Path) -> str:
    """
    Handle Obsidian embeds:
    ![[image.png]]
    Caption must be next line:
    Figure 1: <caption text>

    Result:
    ![Figure 1: <caption text>](folder/image-1.png)

    Physically move/rename the image file into folder_path as image-<n>.<ext>
    """
    lines = content.splitlines()
    new_lines = []
    image_counter = 1

    obsidian_pattern = re.compile(r'!\[\[(.*?)\]\]')

    i = 0
    while i < len(lines):
        line = lines[i].rstrip("\n")
        match = obsidian_pattern.search(line)

        if match:
            raw_inner = match.group(1).strip()
            raw_name = raw_inner.split("|")[0].strip()
            ext = os.path.splitext(raw_name)[1] or ""  # keep extension if present

            new_filename = f"image-{image_counter}{ext}"
            new_image_path = folder_path / new_filename

            # Try to find the original file in a few places
            original_path = find_image_file(md_parent, raw_name, folder_path)

            if original_path:
                try:
                    # Ensure destination doesn't already exist (overwrite if it does)
                    if new_image_path.exists():
                        new_image_path.unlink()
                    shutil.move(str(original_path), str(new_image_path))
                except Exception as e:
                    print(f"Warning: failed to move '{original_path}' → '{new_image_path}': {e}")
            else:
                print(f"Warning: image file '{raw_name}' not found under '{md_parent}'. Leaving link but file not renamed.")

            # Caption is expected on the next line (starting with 'Figure' case-insensitive)
            caption = ""
            if i + 1 < len(lines) and lines[i + 1].strip().lower().startswith("figure"):
                caption = lines[i + 1].strip()
                i += 1  # skip caption line

            markdown_img = f"![{caption}]({folder_name}/{new_filename})"
            new_lines.append(markdown_img)

            image_counter += 1
        else:
            new_lines.append(line)

        i += 1

    return "\n".join(new_lines)

def main():
    if len(sys.argv) < 4:
        print("Usage: python script.py <file.md> <category> <tag1> [tag2] ...")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    category = sys.argv[2]
    tags = sys.argv[3:]

    if not file_path.exists():
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    # Format title from filename
    title = format_title(file_path.name)

    # Create folder named after the file (without .md)
    folder_name = file_path.stem
    folder_path = file_path.parent / folder_name
    folder_path.mkdir(exist_ok=True)

    today = date.today().strftime("%Y-%m-%d")

    # YAML front matter
    front_matter = [
        "---",
        f"title: {title}",
        "description: ",
        f"date: {today}",
        "categories:",
        f"  - {category}",
        "tags:",
    ]
    front_matter.extend([f"  - {tag}" for tag in tags])
    front_matter.append(f"cover: {folder_name}/cover.jpg")
    front_matter.append("---\n")

    # Load original content
    original_content = file_path.read_text(encoding="utf-8")

    # First pass: process Obsidian images (rename + captions)
    processed = process_obsidian_images(original_content, folder_name, folder_path, file_path.parent)

    # Second pass: update standard markdown image paths
    processed = update_markdown_image_paths(processed, folder_name)

    # Combine front matter + content
    final_content = "\n".join(front_matter) + "\n" + processed

    # Write file
    file_path.write_text(final_content, encoding="utf-8")

    print(f"MetaData, Image renaming, Captions, and Image paths updated successfully in {file_path}")

if __name__ == "__main__":
    main()