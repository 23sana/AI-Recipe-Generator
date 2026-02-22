#  AI Recipe Generator

AI-powered Recipe Generator built using **Flask**, **Python**, and Spoonacular API.  
This web application generates recipes based on the ingredients provided by the user.

---

## 🚀 Features

- 🔐 User Authentication (Register & Login)
- 🥗 Ingredient-Based Recipe Search
- 📋 Recipe Details (Ingredients, Instructions, Image)
- 🧠 API Integration (Spoonacular)
- 💾 SQLite Database
- 🎨 Clean Dashboard UI

---

## 🛠 Tech Stack

- Python
- Flask
- SQLite
- SQLAlchemy
- HTML
- CSS
- Spoonacular API

---

## 📂 Project Structure

```
AI_Recipe_Generator/
│
├── app.py
├── templates/
├── static/
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/23sana/AI-Recipe-Generator.git
cd AI-Recipe-Generator
```

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Create .env File

Create a `.env` file in the root folder and add:

```
SPOONACULAR_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

### 4️⃣ Run the Application

```
python app.py
```

Open browser and go to:

```
http://127.0.0.1:5000
```

---

## 🧪 Example Usage

If user inputs:

```
milk, bread
```

The application will return recipes related to those ingredients.

---

## 🔒 Security Note

- API keys are stored in `.env`
- `.env` file is excluded using `.gitignore`
- Database file is not pushed to GitHub

---



