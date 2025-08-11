from pathlib import Path
from string import Template
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = Template("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>$title</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 5px 0; }
        input[type="checkbox"] { margin-right: 10px; }
    </style>
</head>
<body>
    <h1>$title</h1>
    <ul>
        $items
    </ul>
</body>
</html>""")


def generate_checklist(file_path, title):
    """Read tasks from a text file and generate an HTML checklist."""
    tasks = [
        line.strip()
        for line in Path(file_path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    items_html = "\n".join(
        f'<li><input type="checkbox"> {task}</li>'
        for task in tasks
    )

    return HTML_TEMPLATE.substitute(title=title, items=items_html)


@app.route("/", methods=["GET", "POST"])
def home():
    """Main page: upload a .txt file and view the checklist."""
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        title = request.form.get("title", "My Checklist")

        if uploaded_file and uploaded_file.filename.endswith(".txt"):
            temp_path = Path("uploaded.txt")
            uploaded_file.save(temp_path)
            html_content = generate_checklist(temp_path, title)
            return render_template_string(html_content)

        return "Please upload a valid .txt file."

    return """
        <!DOCTYPE html>
        <html>
        <head><title>Checklist Generator</title></head>
        <body>
            <h1>Upload a Text File to Create a Checklist</h1>
            <form method="POST" enctype="multipart/form-data">
                Title: <input type="text" name="title" value="My Checklist"><br><br>
                File: <input type="file" name="file"><br><br>
                <input type="submit" value="Generate Checklist">
            </form>
        </body>
        </html>
    """


if __name__ == "__main__":
    app.run(debug=True)

