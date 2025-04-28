from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import datetime
import os

# Завантаження змінних з .env
load_dotenv()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")  # Отримуємо з .env або використовуємо дефолт

# Підключення до бази даних
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Модель користувача
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    login_count = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)  # Хешування

# Модель завдань
class Todo(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    todo_list_id = db.Column(db.Integer, default=1)

    def to_dict(self):
        return {
            "id": self.id,
            "task": self.task,
            "is_done": self.is_done,
            "todo_list_id": self.todo_list_id
        }

# Flask-Login
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Роут входу
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            user.login_count += 1
            user.last_login = datetime.utcnow()
            db.session.commit()
            return redirect(url_for("admin"))
        return "Невірні облікові дані", 401
    return render_template("login.html", error="test")

# Роут виходу
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Адмін панель
@app.route("/admin")
@login_required
def admin():
    if current_user.username != "admin":
        return "Доступ заборонено", 403
    return render_template("admin.html", user=current_user)

# CRUD для Todo
@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify([todo.to_dict() for todo in Todo.query.all()])

@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.json
    todo = Todo(task=data["task"], todo_list_id=data.get("todo_list_id", 1))
    db.session.add(todo)
    db.session.commit()
    socketio.emit("add_todo", todo.to_dict())
    return jsonify(todo.to_dict()), 201

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({"error": "Завдання не знайдено"}), 404
    data = request.json
    todo.task = data.get("task", todo.task)
    todo.is_done = data.get("is_done", todo.is_done)
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({"error": "Завдання не знайдено"}), 404
    db.session.delete(todo)
    db.session.commit()
    tasks = [todo.to_dict() for todo in Todo.query.all()]
    socketio.emit("update_todos", tasks)
    return jsonify({"message": "Завдання видалено"})

@socketio.on("connect")
def handle_connect():
    tasks = [todo.to_dict() for todo in Todo.query.all()]
    emit("update_todos", tasks)

# Обробка помилок
@app.errorhandler(401)
def unauthorized(e):
    return redirect(url_for("login"))

@app.errorhandler(403)
def forbidden(e):
    return "403 Forbidden: У вас немає доступу.", 403

@app.errorhandler(404)
def page_not_found(e):
    return "404 Not Found", 404

# Ініціалізація БД та створення адміністратора (якщо його немає)
_first_request = True

@app.before_request
def create_tables():
    global _first_request
    if _first_request:
        db.create_all()
        # Перевірка та створення адміністратора
        admin_username = "admin"
        admin_password = os.getenv("ADMIN_PASSWORD")  # Отримуємо пароль адміністратора з .env

        if not admin_password:
            print("Увага: Не встановлено пароль адміністратора в .env!")
        else:
            admin_user = User.query.filter_by(username=admin_username).first()
            if not admin_user:
                admin = User(username=admin_username, password=admin_password)
                db.session.add(admin)
                db.session.commit()
                print(f"Адміністратора '{admin_username}' створено.")
            else:
                print(f"Адміністратор '{admin_username}' вже існує.")
        _first_request = False

if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)







