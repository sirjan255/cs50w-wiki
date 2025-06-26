import random
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util
import markdown2

def get_case_insensitive_entry(title):
    """
    Helper function to get the correct-cased entry filename for a given title (case-insensitive).
    Returns (entry_title, content) if found, else (None, None).
    """
    entries = util.list_entries()
    for entry in entries:
        if entry.lower() == title.lower():
            return entry, util.get_entry(entry)
    return None, None

def index(request):
    """
    Show all encyclopedia entries.
    """
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, title):
    """
    Display a single encyclopedia entry, converting Markdown to HTML.
    If not found, show an error page.
    """
    entry_title, content = get_case_insensitive_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": entry_title,
        "content": html_content
    })

def search(request):
    """
    Handle search queries.
    Redirect to entry if exact match, otherwise show results with substrings.
    """
    if request.method == "GET":
        q = request.GET.get("q", "")
        entries = util.list_entries()
        # Exact match (case-insensitive)
        for entry in entries:
            if entry.lower() == q.lower():
                return redirect("entry", title=entry)
        # Partial match (case-insensitive)
        results = [entry for entry in entries if q.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "query": q,
            "results": results
        })

def new(request):
    """
    Create a new encyclopedia entry.
    GET: Render the creation form.
    POST: Save the new entry if title doesn't exist, else show error.
    """
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "")
        entries = util.list_entries()
        # Check for duplicate (case-insensitive)
        for entry in entries:
            if entry.lower() == title.lower():
                return render(request, "encyclopedia/error.html", {
                    "message": "Entry with this title already exists or title is invalid."
                })
        if title == "":
            return render(request, "encyclopedia/error.html", {
                "message": "Title cannot be empty."
            })
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/new.html")

def edit(request, title):
    """
    Edit an existing encyclopedia entry.
    GET: Show edit form pre-filled with Markdown content.
    POST: Save changes and redirect to entry page.
    """
    entry_title, content = get_case_insensitive_entry(title)
    if request.method == "POST":
        new_content = request.POST.get("content", "")
        if entry_title is None:
            return render(request, "encyclopedia/error.html", {
                "message": "The requested page was not found."
            })
        util.save_entry(entry_title, new_content)
        return redirect("entry", title=entry_title)
    else:
        if content is None:
            return render(request, "encyclopedia/error.html", {
                "message": "The requested page was not found."
            })
        return render(request, "encyclopedia/edit.html", {
            "title": entry_title,
            "content": content
        })

def random_page(request):
    """
    Redirect to a random encyclopedia entry.
    """
    entries = util.list_entries()
    if entries:
        selected = random.choice(entries)
        return redirect("entry", title=selected)
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "No entries available."
        })