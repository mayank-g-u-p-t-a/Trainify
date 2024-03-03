import cv2
from deepface import DeepFace
from twilio.rest import Client
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
dic={}
sr="The Report of your children is here - \n"

if not video.isOpened():
    raise IOError("Cannot open webcam")

while video.isOpened():
    kaam_ka_nhi_hai, frame = video.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for x, y, w, h in faces:
        face_roi = frame[y:y+h, x:x+w]  

        try:
            analyze = DeepFace.analyze(face_roi, actions=['emotion'])
            dominant_emotion = analyze[0]['dominant_emotion']
            if dominant_emotion in dic:
                dic[dominant_emotion]+=1
            else:
                dic[dominant_emotion]=1
            print(f"Face detected, emotion: {dominant_emotion}")
            cv2.putText(frame, f'Emotion: {dominant_emotion}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (224, 77, 176), 2)
        except Exception as e:
            
            # print(f"Error during emotion analysis: {str(e)}")
            print('No face detected')

        image = cv2.rectangle(frame, (x, y), (x+w, y+h), (89, 2, 236), 1)

    cv2.imshow('video', frame)

    key = cv2.waitKey(100)

    if key == ord('q'):
        print(dic)
        s=0
        for i in dic:
            s=s+dic[i]
        for i in dic:
            sr += f"{i} - {((dic[i] / s) * 100):.2f}%\n"

            print(i,(dic[i]/s)*100,"%")
        

# Twilio credentials
        account_sid = 'AC52814435216607f6f3461780ec3556b8'
        auth_token = '97f07a825b3a49f8b355b7241669baf5'
        twilio_phone_number = '+19404458689'
        recipient_phone_number = '+917355357077'

    # Create a Twilio client
        client = Client(account_sid, auth_token)

# Send a message
        message = client.messages.create(
            body=sr,
            from_=twilio_phone_number,
            to=recipient_phone_number
)

        print(f'Message sent with SID: {message.sid}')

        break

video.release()
cv2.destroyAllWindows()