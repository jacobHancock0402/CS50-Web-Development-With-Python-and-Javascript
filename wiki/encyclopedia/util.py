import re
import markdown2

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage



def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.html$", "", filename)
                for filename in filenames if filename.endswith(".html")))


def save_entry(title, content, html=True):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    if html:
        filename = f"entries/{title}.html"
        title = markdown2.markdown(title)
        content = markdown2.markdown(content)
    else:
        filename = f"entries/{title}.md"

    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title, html=True):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    if html:
        try:
            f = default_storage.open(f"entries/{title}.html")
            return f.read().decode("utf-8")
        except FileNotFoundError:
            return None
    else:
        try:
            f = default_storage.open(f"entries/{title}.md")
            return f.read().decode("utf-8")
        except FileNotFoundError:
            return None
