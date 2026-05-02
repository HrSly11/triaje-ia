from flask import Flask
from flask_cors import CORS
import bcrypt

app = Flask(__name__)
CORS(app)

password = "admin123"
hash_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
print("Hash bcrypt:", hash_bytes.decode('utf-8'))

@app.route('/health')
def health():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
