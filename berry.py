import cv2
import tensorflow as tf
import numpy as np

labels = ["accept", "reject", "none"]
model_path = 'classify_plastic.tflite'

interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def classify_image(image):
    image = cv2.resize(image, (input_details[0]['shape'][1], input_details[0]['shape'][2]))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    
    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted_class_index = np.argmax(output_data, axis=1)[0]
    return predicted_class_index

def get_image():
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        print('error : Can\'t detect camera. Please connect it again.')
        return 0
    
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break
        
        class_index = classify_image(frame)
        print(labels[class_index])
        
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC 키 누르면 종료
            break
    
    capture.release()
    cv2.destroyAllWindows()

get_image()
