from flask import Flask, render_template
import mysql.connector
import redis
import os

app = Flask(__name__)

def check_mysql():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME")
        )
        connection.close()
        return "MySQL Connection Successful ✅"
    except Exception as e:
        return f"MySQL Connection Failed ❌ ({e})"

def check_redis():
    try:
        r = redis.Redis(host="redis", port=6379)
        r.ping()
        return "Redis Connection Successful ✅"
    except Exception as e:
        return f"Redis Connection Failed ❌ ({e})"

@app.route("/")
def home():
    mysql_status = check_mysql()
    redis_status = check_redis()
    return render_template(
        "index.html",
        mysql_status=mysql_status,
        redis_status=redis_status
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
