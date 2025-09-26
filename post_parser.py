#!/usr/bin/env python3
import sys
import os
import re
from datetime import date
from pathlib import Path

def format_title(filename: str) -> str:
    """Convert filename like 'windows-pe-analysis.md' to 'Windows PE Analysis'"""
    name = Path(filename).stem  # remove extension
    return " ".join(word.capitalize() for word in name.replace("-", " ").split())

def update_image_paths(content: str, folder_name: str) -> str:
    """
    Update markdown image paths.
    Example: ![image.png](image.png) -> ![image.png](the-payload/image.png)
    """
    pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
    
    def replacer(match):
        alt_text, path = match.groups()
        # Only modify relative images (not URLs or already have folder paths)
        if not (path.startswith("http://") or path.startswith("https://") or "/" in path):
            return f"![{alt_text}]({folder_name}/{path})"
        return match.group(0)
    
    return pattern.sub(replacer, content)

def main():
    if len(sys.argv) < 4:
        print("Usage: python script.py <file.md> <category> <tag1> [tag2] [tag3] ...")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    category = sys.argv[2]
    tags = sys.argv[3:]

    if not file_path.exists():
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    # Format title from filename
    title = format_title(file_path.name)

    # Create folder with same name as file (without extension)
    folder_name = file_path.stem
    folder_path = file_path.parent / folder_name
    folder_path.mkdir(exist_ok=True)

    # Get current date
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

    # Read original file content
    with open(file_path, "r", encoding="utf-8") as f:
        original_content = f.read()

    # Update image paths
    updated_content = update_image_paths(original_content, folder_name)

    # Prepend YAML front matter
    new_content = "\n".join(front_matter) + "\n" + updated_content

    # Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"MetaData, Date, and Image paths updated successfully in {file_path}")

if __name__ == "__main__":
    main()