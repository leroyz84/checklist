from pathlib import Path
from string import Template
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

CHECKLIST_DIR = Path("checklists")  # directory with .txt files
CHECKLIST_DIR.mkdir(exist_ok=True)

# Store checkbox states in memory
selections = {}

HTML_TEMPLATE = Template("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>$title</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #DDDDDD; font-family: Arial, sans-serif; margin: 20px; font-size: 18pt; }
        h1 { color: #333; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 5px 0; }
        input[type="checkbox"] { margin-right: 10px; }
        label { cursor: pointer; }
        form { display: inline; font-size: 18pt; }
        a { color: #0099FF;   }
        button.save { font-size: 14pt; background: #99FF99; }
        button.reset { font-size: 14pt; background: #FF9999; }

    </style>
</head>
<body>
    <h1>$title</h1>
    <form method="POST">
        <ul>
            $items
        </ul>
    </form>
</body>
</html>
""")


def generate_checklist(file_path, title):
    """Generate HTML list items with labels linked to checkboxes."""
    tasks = [
        line.strip()
        for line in Path(file_path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    file_key = str(file_path)
    current_selection = selections.get(file_key, set())

    items = []
    for i, task in enumerate(tasks):
        if task.lstrip().startswith("---"):
            # Render as bold header, strip leading dashes and whitespace
            header_text = task.strip("-").strip()
            if i > 0:
                items.append(f'<br><li><strong>{header_text}</strong></li>')
            else:
                items.append(f'<li><strong>{header_text}</strong></li>')
        else:
            checked = "checked" if task in current_selection else ""
            items.append(
                f'<li>'
                f'<input type="checkbox" id="item{i}" name="item{i}" {checked}>'
                f'<label for="item{i}">{task}</label>'
                f'</li>'
            )

    items_html = "\n".join(items)

    back = """
    <br>
    <form method="POST" style="margin-top:10px;">
        <button type="submit" class="save" name="action" value="save">Save</button>
        <button type="submit" class="reset" name="action" value="reset">Reset</button>
    </form>
    <p><a href="/">Back to file list</a></p>
    """
    return HTML_TEMPLATE.substitute(title=title, items=items_html+back)



@app.route("/")
def home():
    """Show a list of available checklist files."""
    files = sorted([f for f in CHECKLIST_DIR.iterdir() if f.suffix.lower() == ".txt"])

    if not files:
        return f"""
            <h1>No checklists found</h1>
            <p>Put .txt files into: {CHECKLIST_DIR.resolve()}</p>
        """

    file_links = [
        f'<li><a href="{url_for("view_checklist", filename=f.name)}">{f.name}</a></li>'
        for f in files
    ]

    items_html = f"""
        <ul>
            {''.join(file_links)}
        </ul>
    """
    return HTML_TEMPLATE.substitute(title="Checklists", items=items_html)


@app.route("/checklist/<filename>", methods=["GET", "POST"])
def view_checklist(filename):
    """View and update a specific checklist."""
    file_path = CHECKLIST_DIR / filename

    if not file_path.exists():
        return "Checklist not found.", 404

    if request.method == "POST":
        action = request.form.get("action")

        tasks = [
            line.strip()
            for line in file_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        file_key = str(file_path)

        if action == "save":
            selected = {tasks[i] for i in range(len(tasks)) if f"item{i}" in request.form}
            selections[file_key] = selected

        elif action == "reset":
            selections[file_key] = set()

        return redirect(url_for("view_checklist", filename=filename))

    html_content = generate_checklist(file_path, filename)
    return render_template_string(html_content)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)

