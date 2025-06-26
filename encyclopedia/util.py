import re
import os

from django.conf import settings

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    entries_dir = os.path.join(settings.BASE_DIR, "entries")
    _, _, filenames = next(os.walk(entries_dir))
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))

def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown content.
    Overwrites existing entry with the same title (case-insensitive).
    """
    entries_dir = os.path.join(settings.BASE_DIR, "entries")
    # Find if an entry with this title (case-insensitive) already exists and overwrite it
    for filename in os.listdir(entries_dir):
        if filename.lower() == f"{title}.md".lower():
            filepath = os.path.join(entries_dir, filename)
            break
    else:
        filepath = os.path.join(entries_dir, f"{title}.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title (case-insensitive).
    Returns the content as a string, or None if no such entry exists.
    """
    entries_dir = os.path.join(settings.BASE_DIR, "entries")
    for filename in os.listdir(entries_dir):
        if filename.lower() == f"{title}.md".lower():
            filepath = os.path.join(entries_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
    return None