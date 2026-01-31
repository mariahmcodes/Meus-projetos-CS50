import os
from cs50 import SQL
from flask import Flask, redirect, render_template, request

# Configura aplicação
app = Flask(__name__)

# Garante que os templates sejam recarregados automaticamente
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Conecta ao banco de dados
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Evita cache nos responses"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Pega dados do formulário
        name = request.form.get("friend")
        month = request.form.get("month")
        day = request.form.get("day")

        # Valida os dados
        if not name or not month or not day:
            return redirect("/")

        # Insere no banco
        db.execute(
            "INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)",
            name,
            month,
            day
        )

        return redirect("/")

    else:
        # Pega todas as entradas do banco
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays)
