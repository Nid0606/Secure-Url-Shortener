import string
import secrets
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from security import is_brand_impersonation, is_url_malicious

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
    custom_code = data.get('custom_code')
    requested_length = data.get('length', 6) 
    
    if is_url_malicious(original_url):
        return jsonify({
            "error": "SECURITY_BLOCK",
            "message": "Access Denied: The destination URL has been flagged as malicious or suspicious by safety APIs."
        }), 400
    
    if custom_code:
        custom_code = custom_code.strip()

        already_exists = URLMapping.query.filter_by(short_code=custom_code).first()
        if already_exists:
            return jsonify({
                "error": "ALREADY_TAKEN",
                "message": "This custom alias is already taken."
            }), 400
        
        if is_brand_impersonation(custom_code):
            return jsonify({
                "error": "BRAND_PROTECTION_BLOCK",
                "message": "Security Restriction: Custom alias contains a protected trademark to prevent phishing."
            }), 403
        
        short_code = custom_code
    else:
        short_code = generate_short_code(length=int(requested_length))
    
    
    new_mapping = URLMapping(long_url=original_url, short_code=short_code)
    db.session.add(new_mapping)
    db.session.commit()
    
    return jsonify({
        "message": "URL successfully shortened!",
        "short_code": short_code,
        "long_url": original_url 
    }), 200

@app.route('/api/redirect/<short_code>', methods=['GET'])
def get_destination_url(short_code):
    url_record = URLMapping.query.filter_by(short_code=short_code).first()
    
    if not url_record:
        return jsonify({"error": "Shortened URL not found"}), 404
        
    if url_record.is_suspended:
        return jsonify({
            "error": "URL_SUSPENDED",
            "message": "This link has been blocked because it was flagged as unsafe by the community."
        }), 403
        
    return jsonify({
        "short_code": short_code,
        "long_url": url_record.long_url
    }), 200

@app.route('/api/report', methods=['POST'])
def report_url():
    data = request.get_json()
    
    if not data or 'short_code' not in data:
        return jsonify({"error": "Missing short_code parameter"}), 400
        
    short_code = data['short_code'].strip()
    url_record = URLMapping.query.filter_by(short_code=short_code).first()
    
    if not url_record:
        return jsonify({"error": "Shortened URL not found"}), 404
        
    if url_record.is_suspended:
        return jsonify({
            "message": "This URL is already suspended.",
            "is_suspended": True
        }), 200

    url_record.report_count += 1
    
    REPORT_THRESHOLD = 5
    if url_record.report_count >= REPORT_THRESHOLD:
        url_record.is_suspended = True
        print(f"🚫 [COMMUNITY BLOCK] URL {short_code} suspended due to excessive reports ({url_record.report_count}).")
        
    db.session.commit()
    
    return jsonify({
        "message": "Report submitted successfully.",
        "report_count": url_record.report_count,
        "is_suspended": url_record.is_suspended
    }), 200

if __name__=="__main__":
    app.run(debug=True, port=5000)