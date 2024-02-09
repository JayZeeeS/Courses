import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    positions = {}
    data = db.execute("SELECT * FROM transactions WHERE user_id = ?;", session["user_id"])
    for row in data:
        symbol = row["symbol"]
        amount = row["amount"]
        if symbol not in positions:
            positions[symbol] = 0
        if row["transaction_type"] == "buy":
            positions[symbol] += amount
        else:
            positions[symbol] -= amount

    poslist = [{"symbol": symbol.upper(), "owned": amount, "pps": lookup(symbol)
                ["price"], "total_value": lookup(symbol)["price"] * amount} for symbol, amount in positions.items()]
    for d in poslist:
        if d.get("owned") == 0:
            poslist.remove(d)
    grand = 0
    for item in poslist:
        grand += item["total_value"]
    cash = db.execute("SELECT cash FROM users WHERE id = ?",
                      session["user_id"])
    return render_template("index.html", poslist=poslist, grand=grand+cash[0]["cash"], cash=cash[0]["cash"])


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        amount = request.form.get("shares")
        quote = lookup(symbol)
        if quote == None:
            return apology("Not Found")
        if symbol == "":
            return apology("Symbol field is required")
        if amount == "":
            return apology("Amount of shares field is required")
        if not amount.isdigit():
            return apology("must be a positive integer")
        if float(amount) <= 0:
            return apology("Amount cannot be less than 0")

        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        price = quote["price"]
        if price*float(amount) > user_cash[0]["cash"]:
            return apology("You're Broke!", 403)
        db.execute("INSERT INTO transactions (transaction_type, symbol, amount, price, transaction_time, user_id) VALUES (?,?,?,?,?,?);",
                  "buy", symbol, amount, price, datetime.now(), session["user_id"])
        db.execute("UPDATE users SET cash = ? WHERE id = ?;",
                   user_cash[0]["cash"] - (price * float(amount)), session["user_id"])
        return redirect("/")
    if request.method == "GET":
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = ?;", session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        query = request.form.get("symbol")
        if query == "":
            return apology("Query was empty")
        quote = lookup(query)
        if quote == None:
            return apology("Symbol does not exist")
        return render_template("quoted.html", quote=quote)
    if request.method == "GET":
        return render_template("quote.html")
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        usrname = request.form.get("username")
        pwd = request.form.get("password")
        usernames = db.execute("SELECT * FROM users WHERE username = ?;", usrname)
        if usrname == "":
            return apology("Must input a username")
        if len(usernames) != 0 and not len(db.execute("SELECT * FROM users;")) == 0:
            print(usernames, usrname)
            return apology("Username is already taken")
        if pwd != request.form.get("confirmation"):
            return apology("Passwords do not match")
        if pwd == "":
            return apology("Must input a password")

        pwdHash = generate_password_hash(pwd)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", usrname, pwdHash)
        return render_template("login.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        data = db.execute(
            "SELECT * FROM transactions WHERE user_id = ?;", session["user_id"])
        sySet = {transaction["symbol"].upper() for transaction in data}
        symbols = list(sySet)
        return render_template("sell.html", symbols=symbols)
    if request.method == "POST":
        positions = {}
        data = db.execute(
            "SELECT * FROM transactions WHERE user_id = ?;", session["user_id"])
        for row in data:
            symbol = row["symbol"]
            amount = row["amount"]
            if symbol not in positions:
                positions[symbol] = 0
            if row["transaction_type"] == "buy":
                positions[symbol] += amount
            else:
                positions[symbol] -= amount
        poslist = [{"symbol": symbol, "owned": amount, "pps": lookup(symbol)[
            "price"], "total_value": lookup(symbol)["price"] * amount} for symbol, amount in positions.items()]
        print(poslist)

        sell_symbol = request.form.get("symbol")
        sell_amount = int(request.form.get("shares"))
        user_amount = 0
        for d in poslist:
            if d.get("symbol") == sell_symbol:
                user_amount = d.get("owned")
        if sell_amount > user_amount:
            return apology(f"You only own {user_amount} but tried to sell {sell_amount}...")
        if sell_amount <= 0:
            return apology(f"You can't sell {sell_amount} shares! Silly you~")
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        price = lookup(sell_symbol)["price"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?;",
                   user_cash[0]["cash"] + (price * float(sell_amount)), session["user_id"])
        db.execute("INSERT INTO transactions (transaction_type, symbol, amount, price, transaction_time, user_id) VALUES (?,?,?,?,?,?);",
                   "sell", sell_symbol, sell_amount, price, datetime.now(), session["user_id"])
        return redirect("/")


@app.route("/account", methods=["POST", "GET"])
@login_required
def account():
    if request.method == "GET":
        return render_template("account.html", invisible="invisible")
    if request.method == "POST":
        old_pass = request.form.get("password")
        new_pass = request.form.get("new_password")
        confirmation = request.form.get("new_password2")

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if not check_password_hash(rows[0]["hash"], old_pass):
            return apology("Invalid password", 403)
        if new_pass == "":
            return apology("Password cannot be an empty string")
        if new_pass != confirmation:
            return apology("Passwords do not match")
        if new_pass == old_pass:
            return apology("Cannot change password to the current password")
        pwdHash = generate_password_hash(new_pass)
        db.execute("UPDATE users SET hash=? WHERE id=?;", pwdHash, session["user_id"])
        return render_template("account.html")
