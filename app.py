
import requests
SPOONACULAR_API_KEY = "Paste API Key"

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ------------------ DATABASE ------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ------------------ LOGIN MANAGER ------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ------------------ USER MODEL ------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------ ROUTES ------------------

# Home → redirect to login
@app.route("/")
def home():
    return redirect(url_for("login"))

# -------- REGISTER --------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for("register"))

        # Hash password
        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# -------- LOGIN --------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials!", "danger")

    return render_template("login.html")

# -------- DASHBOARD (index.html) --------

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    recipe = None
    ingredients_list = []
    instructions = None
    image = None

    if request.method == "POST":
        ingredients = request.form.get("ingredients")

        # Step 1: Search recipe by ingredients
        search_url = "https://api.spoonacular.com/recipes/findByIngredients"
        search_params = {
    "ingredients": ingredients,
    "number": 1,
    "ranking": 1,
    "ignorePantry": True,
    "apiKey": SPOONACULAR_API_KEY
}

        search_response = requests.get(search_url, params=search_params)

        if search_response.status_code == 200:
            data = search_response.json()

            if data:
                recipe_id = data[0]["id"]
                recipe = data[0]["title"]
                image = data[0]["image"]

                # Step 2: Get full recipe details
                details_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
                details_params = {
                    "apiKey": SPOONACULAR_API_KEY
                }

                details_response = requests.get(details_url, params=details_params)

                if details_response.status_code == 200:
                    details = details_response.json()

                    # Ingredients
                    ingredients_list = [
                        item["original"] for item in details["extendedIngredients"]
                    ]

                    # Instructions
                    instructions = details.get("instructions", "No instructions available.")

            else:
                recipe = "No recipe found."

        else:
            recipe = "API Error. Check your API key."

    return render_template(
        "index.html",
        recipe=recipe,
        ingredients_list=ingredients_list,
        instructions=instructions,
        image=image
    )

# -------- LOGOUT --------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))

# ------------------ MAIN ------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
