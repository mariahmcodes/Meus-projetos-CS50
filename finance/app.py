import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd

app = Flask(__name__)
app.jinja_env.filters["usd"] = usd

# Configurações de sessão
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Banco de dados
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio"""
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    portfolio = db.execute(
        "SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0",
        session["user_id"]
    )

    grand_total = cash

    for stock in portfolio:
        quote_data = lookup(stock["symbol"])
        if quote_data:
            stock["name"] = quote_data["name"]
            stock["price"] = quote_data["price"]
            stock["total_value"] = stock["total_shares"] * quote_data["price"]
            grand_total += stock["total_value"]
        else:
            stock["name"] = "N/A"
            stock["price"] = 0
            stock["total_value"] = 0

    return render_template("index.html", portfolio=portfolio, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol")
        quote_data = lookup(symbol)
        if quote_data is None:
            return apology("invalid symbol")

        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide positive integer")

        shares = int(shares)
        price = quote_data["price"]
        total_cost = shares * price

        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        if total_cost > user_cash:
            return apology("can't afford")

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            session["user_id"], symbol.upper(), shares, price
        )
        db.execute(
            "UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"]
        )

        return redirect("/")

    return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_to_sell = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol")
        if not shares_to_sell or not shares_to_sell.isdigit() or int(shares_to_sell) <= 0:
            return apology("must provide positive number of shares")

        shares_to_sell = int(shares_to_sell)

        owned = db.execute(
            "SELECT SUM(shares) AS total FROM transactions WHERE user_id = ? AND symbol = ?",
            session["user_id"], symbol
        )
        if not owned or owned[0]["total"] < shares_to_sell:
            return apology("not enough shares to sell")

        quote_data = lookup(symbol)
        if quote_data is None:
            return apology("invalid symbol")
        price = quote_data["price"]

        total_gain = shares_to_sell * price
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_gain, session["user_id"])
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            session["user_id"], symbol, -shares_to_sell, price
        )

        return redirect("/")

    portfolio = db.execute(
        "SELECT symbol, SUM(shares) AS total FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total > 0",
        session["user_id"]
    )
    return render_template("sell.html", portfolio=portfolio)


@app.route("/history")
@login_required
def history():
    transactions = db.execute(
        "SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC",
        session["user_id"]
    )
    return render_template("history.html", transactions=transactions)


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    quote_data = None
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol")
        quote_data = lookup(symbol)
        if quote_data is None:
            return apology("invalid symbol")
    return render_template("quote.html", quote=quote_data)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username")
        if not password:
            return apology("must provide password")
        if password != confirmation:
            return apology("passwords do not match")

        try:
            user_id = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username, generate_password_hash(password)
            )
        except ValueError:
            return apology("username already exists")

        session["user_id"] = user_id
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    if request.method == "POST":
        amount = request.form.get("amount")
        if not amount:
            return apology("must provide amount")
        try:
            amount = float(amount)
            if amount <= 0:
                return apology("amount must be positive")
        except ValueError:
            return apology("invalid amount")

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", amount, session["user_id"])
        return redirect("/")

    return render_template("add_cash.html")
