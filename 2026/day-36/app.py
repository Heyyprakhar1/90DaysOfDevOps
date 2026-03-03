import os
import time
import pymysql
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_db_connection():
    for i in range(10):  # retry 10 times
        try:
            connection = pymysql.connect(
                host=os.getenv("MYSQL_HOST", "mysql"),
                user=os.getenv("MYSQL_USER", "mysql"),
                password=os.getenv("MYSQL_PASSWORD", "root"),
                database=os.getenv("MYSQL_DB", "mydb"),
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Connected to MySQL!")
            return connection
        except pymysql.err.OperationalError as e:
            print(f"MySQL not ready, retrying... {i+1}/10")
            time.sleep(3)

    raise RuntimeError("Database connection failed after retries")

def init_db():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                message TEXT NOT NULL,
                rating INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    connection.commit()
    connection.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit_feedback():
    name = request.form["name"]
    message = request.form["message"]
    rating = request.form["rating"]

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO feedback (name, message, rating) VALUES (%s, %s, %s)",
            (name, message, rating)
        )
    connection.commit()
    connection.close()

    return redirect("/feedbacks")


@app.route("/feedbacks")
def feedbacks():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM feedback ORDER BY created_at DESC")
        data = cursor.fetchall()

        cursor.execute("SELECT AVG(rating) as avg_rating FROM feedback")
        avg_rating = cursor.fetchone()["avg_rating"]

    connection.close()

    return render_template("feedbacks.html", feedbacks=data, avg_rating=avg_rating)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000)
