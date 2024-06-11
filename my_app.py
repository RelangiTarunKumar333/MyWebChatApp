import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from groq import Groq
from dotenv import load_dotenv
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Load environment variables from .env2 file
load_dotenv('.env2')
groq_api_key = os.getenv('GROQ_API_KEY')
pexels_api_key = os.getenv('PEXELS_API_KEY')
youtube_api_key = os.getenv('YOUTUBE_API_KEY')
secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = secret_key
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

client = Groq()

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

def fetch_image(query):
    response = requests.get(f"https://api.pexels.com/v1/search?query={query}", headers={"Authorization": pexels_api_key})
    data = response.json()
    if data['photos']:
        img_url = data['photos'][0]['src']['medium']
        return img_url
    return None

def fetch_video(query):
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={youtube_api_key}&type=video&maxResults=1"
    response = requests.get(search_url)
    data = response.json()
    if data['items']:
        video_id = data['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url
    return None

@app.route('/')
def home():
    if 'username' in session:
        return render_template('my_index.html')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return 'Username or email already exists'
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('my_register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = user.username
            return redirect(url_for('home'))
        return 'Invalid credentials'
    return render_template('my_login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/chat', methods=['POST'])
def chat():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="llama3-8b-8192",
        )
        bot_message = chat_completion.choices[0].message.content

        image_url = fetch_image(user_message)
        video_url = fetch_video(user_message)

        response = {"message": bot_message}
        if image_url:
            response["image_url"] = image_url
        if video_url:
            response["video_url"] = video_url

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": f"Unable to get response from Groq API. {e}"}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
