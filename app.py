from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# MySQL Database Connection
conn = mysql.connector.connect(
    host="localhost", 
    user="root", 
    password="root", 
    database="chatbot_db"
)
cursor = conn.cursor()

# Predefined Responses
responses = {
    "hello": "Hi there! How can I assist you?",
    "how are you": "I'm just a bot, but I'm doing well! How about you?",
    "what is your name": "I'm a chatbot powered by Flask and MySQL!",
    "bye": "Goodbye! Have a great day!",
    "services": "saving your deatils "
}

# Function to get bot response
def get_response(user_input):
    user_input = user_input.lower()
    for key in responses:
        if key in user_input:
            return responses[key]
    return "I'm not sure how to respond to that."

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    bot_response = get_response(user_message)
    
    # Store the message in MySQL
    cursor.execute("INSERT INTO messages (user_message, bot_response) VALUES (%s, %s)", (user_message, bot_response))
    conn.commit()
    
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
