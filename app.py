from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from llm import convert_nl_to_sql  # Import the LLM conversion function

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Define a simple model corresponding to your 'users' table
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)

    def __repr__(self):
        return f'<User {self.name}>'

@app.route('/')
def home():
    return "Welcome to the NL-DB-LLM Flask App!"

@app.route('/users')
def get_users():
    # Fetch all users from the database
    users = User.query.all()
    users_data = [{
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'age': user.age
    } for user in users]
    return jsonify(users_data)

@app.route('/nlquery', methods=['POST'])
def nl_query():
    """
    Accepts a JSON payload with a natural language query, converts it to SQL,
    and returns the generated SQL query.
    Example payload: { "query": "Find all users older than 30." }
    """
    data = request.get_json()
    nl_query_text = data.get('query', '')
    if not nl_query_text:
        return jsonify({"error": "No query provided"}), 400
    sql_query = convert_nl_to_sql(nl_query_text)
    return jsonify({"sql_query": sql_query})

if __name__ == '__main__':
    app.run(debug=True)
