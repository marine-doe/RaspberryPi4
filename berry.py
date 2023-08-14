import cv2
import tensorflow as tf
from PIL import Image

labels = ["accept", "reject", "none"]
# .tflite 모델 파일 경로
model_path = 'classify_plastic.tflite'

# TensorFlow Lite 모델 로드
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# 입력 및 출력 텐서 정보 가져오기
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def get_image():
    capture = cv2.VideoCapture(0)
    if not capture.isOpened(): #카메라가 정상 인식이 안되면
        print('error : Can\'t detect camera. Please connect it again.')  # 카메라 재연결 하라는 오류 문구
        return 0  # 종료
    width = capture.get(3) #현재 영상의 너비
    height = capture.get(4) #현재 영상의 높이
    fps = capture.get(5) #현재 영상의 fps

    #각 프레임 초기화
    _, frame = capture.read()

    def classify_image(image): # 이미지를 입력
        # print(input_details[0]['shape'][1]) #모델 인풋 크기 224*224
        # print(input_details[0]['shape'][2])
        print(image.shape)
        # 이미지 전처리: 리사이즈 및 정규화
        # TODO: resize 전에 정사각형으로 crop 해야함

        image = image[80:560, 0:480] #이미지 crop(640*480 -> 480*480)
        image = cv2.resize(image, (input_details[0]['shape'][1], input_details[0]['shape'][2]))
        cv2.imshow("frame", image)
        image = image / 255.0  # 0~255 범위의 값을 0~1 범위로 정규화

        image = tf.convert_to_tensor(image, dtype=tf.float32)
        image = tf.expand_dims(image, axis=0)  # 배치 차원 추가

        # 입력 텐서에 데이터 로드
        interpreter.set_tensor(input_details[0]['index'], image)

        # 모델 추론 실행
        interpreter.invoke()

        # 출력 텐서에서 결과 가져오기
        output_data = interpreter.get_tensor(output_details[0]['index'])

        # 결과 처리 - 가장 높은 확률을 가진 클래스 인덱스 가져오기
        predicted_class_index = tf.argmax(output_data, axis=1)[0]
        return predicted_class_index.numpy()

    while capture.isOpened():
        if cv2.waitKey(1) > 0: break #esc 누르면 종료
        _, frame = capture.read()
        # cv2.imshow("frame", frame)
        class_index = classify_image(frame)
        print(class_index)
        # print(labels[class_index.numpy()])
        print(labels[class_index])

        if cv2.waitKey(1) > 0: break  # esc 누르면 종료

get_image()
