import string
import secrets
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class URLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(20), unique=True, nullable=False)
    report_count = db.Column(db.Integer, default=0)
    is_suspended = db.Column(db.Boolean, default=False)

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(secrets.choice(characters) for _ in range(length))
        already_exists = URLMapping.query.filter_by(short_code=code).first()
        if not already_exists:
            return code
        
with app.app_context():
    db.create_all()

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    
    if not data or 'long_url' not in data:
        return jsonify({"error": "Missing long_url parameter"}), 400
        
    original_url = data['long_url']
    requested_length = data.get('length', 6) 
    
    short_code = generate_short_code(length=int(requested_length))
    
    new_mapping = URLMapping(long_url=original_url, short_code=short_code)
    db.session.add(new_mapping)
    db.session.commit()
    
    return jsonify({
        "message": "URL successfully shortened!",
        "short_code": short_code,
        "long_url": original_url 
    }), 200

if __name__=="__main__":
    app.run(debug=True, port=5000)