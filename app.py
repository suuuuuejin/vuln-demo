from flask import Flask, request, make_response
import sqlite3
import os

app = Flask(__name__)

# Intentional hardcoded secret for scanner testing
app.config["SECRET_KEY"] = "super-secret-dev-key-do-not-use"

DB_PATH = "test.db"


def get_db():
    return sqlite3.connect(DB_PATH)


@app.route("/")
def index():
    return """
    <h1>Vulnerable Demo App</h1>
    <ul>
      <li>/login?username=alice&password=password123</li>
      <li>/search?q=test</li>
      <li>/read?name=notes.txt</li>
    </ul>
    """


@app.route("/login")
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")

    conn = get_db()
    cur = conn.cursor()

    # VULN 1: SQL Injection
    query = f"SELECT id, username FROM users WHERE username = '{username}' AND password = '{password}'"
    cur.execute(query)
    row = cur.fetchone()

    conn.close()

    if row:
        return {"status": "ok", "user": row[1]}
    return {"status": "fail"}


@app.route("/search")
def search():
    q = request.args.get("q", "")

    # VULN 2: Reflected XSS
    html = f"""
    <html>
      <body>
        <h1>Search</h1>
        <p>You searched for: {q}</p>
      </body>
    </html>
    """
    return make_response(html)


@app.route("/read")
def read_file():
    name = request.args.get("name", "notes.txt")

    # VULN 3: Path Traversal / Arbitrary File Read
    path = os.path.join("files", name)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    return f"<pre>{content}</pre>"


@app.route("/admin")
def admin():
    # Just here so scanners see another simple route
    return {"admin": True, "message": "demo admin page"}


if __name__ == "__main__":
    # Intentionally broad bind for testing
    app.run(host="0.0.0.0", port=5000, debug=True)