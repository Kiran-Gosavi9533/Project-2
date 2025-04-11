from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import logging
from chatbot_functions import query_ollama  # Import the Ollama function

app = Flask(__name__)
CORS(app)

# Set up a secret key for session management (Change this for production use!)
app.secret_key = 'your_secure_secret_key'  # Replace with a secure key in production

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Home route
@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        logging.info(f"Login attempt - Username: {username}")

        # Replace this with a proper authentication mechanism
        if username == 'admin' and password == 'password':  # Change this for production
            session['username'] = username
            logging.info("Login successful")
            return redirect(url_for('home'))
        else:
            logging.warning("Invalid login attempt")
            return render_template('login.html', error="Invalid credentials. Please try again.")
    
    return render_template('login.html')

# Chatbot route
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            logging.warning("Empty message received")
            return jsonify({"error": "Message cannot be empty"}), 400

        bot_reply = query_ollama(user_message)
        return jsonify({"reply": bot_reply})

    except Exception as e:
        logging.exception("Unexpected Error")
        return jsonify({"error": "An unexpected error occurred."}), 500

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    logging.info("User logged out")
    return redirect(url_for('login'))

# Serve static files
@app.route('/static/<path:filename>')
def static_file(filename):
    return app.send_static_file(filename)

if __name__ == '__main__':
    app.run(debug=True)

