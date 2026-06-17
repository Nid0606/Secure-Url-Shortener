from flask import Flask, request, jsonify
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

@app.route('/api/shorten', methods=['POST'])
def test_shorten():
    data=request.get_json()

    if not data or 'long_url' in data:
        return jsonify("error":"Missing long_url parameter")
    
    print(f" Backend recieved URL successfully: {data['long_url']}")

    return jsonify({
        "message":"Connection Established!"
        "short_url": "https://your-codespace-url-here/test123"
    }), 200

if __name__=="__main__":
    app.run(debug=True, port=5000)