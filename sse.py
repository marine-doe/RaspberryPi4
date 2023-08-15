from flask import Flask, Response
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/events')
def events():
    def generate():
        count = 0
        while True:
            time.sleep(1)  # 1초마다 데이터 전송
            yield f"data: Hello, {count}\n\n"
            count += 1

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(port=8888)
