import serial
from flask import Flask, Response, request, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ser = serial.Serial('COM5', 9600)  # 아두이노와 연결된 시리얼 포트를 사용합니다.
# ser.open()

def OpencvL():
    return 3


def OpencvR():
    return 3

@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


@app.route('/events')
def events():
    def generate():
        count = 0
        while True:
            line = ser.readline().decode('utf-8')
            input_chars = list(line)

            if input_chars[0] == 'L':
                resultL = OpencvL()
                if resultL == 0:
                    input_chars[0] = 'x'
                elif resultL == 1:
                    input_chars[0] = 'y'
                elif resultL == 2:
                    input_chars[0] = 'z'

            if input_chars[1] == 'R':
                resultR = OpencvR()
                if resultR == 0:
                    input_chars[1] = 'X'
                elif resultR == 1:
                    input_chars[1] = 'Y'
                elif resultR == 2:
                    input_chars[1] = 'Z'

            # time.sleep(0.2)
            # print()
            yield f"{''.join(input_chars)}\n"

            # count += 1
    return Response(generate(), mimetype='text/event-stream')



if __name__ == '__main__':
#    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
#    ssl_context.load_cert_chain(certfile='newcert.pem', keyfile='newkey.pem', password='secret')
#    app.run(host="0.0.0.0", port=443, ssl_context=ssl_context)
     app.run(port=8888)
