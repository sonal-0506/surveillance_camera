import RPi.GPIO as GPIO
import time
import picamera
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

GPIO.setwarnings(False)
GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
TRIG = 4
ECHO = 18

GREEN = 17
YELLOW = 27
RED = 22

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.setup(GREEN,GPIO.OUT)
GPIO.setup(YELLOW,GPIO.OUT)
GPIO.setup(RED,GPIO.OUT)

def no_lights():
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(YELLOW, GPIO.LOW)
    GPIO.output(RED, GPIO.LOW)

def green_light():
    GPIO.output(GREEN, GPIO.HIGH)
    GPIO.output(YELLOW, GPIO.LOW)
    GPIO.output(RED, GPIO.LOW)

def yellow_light():
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(YELLOW, GPIO.HIGH)
    GPIO.output(RED, GPIO.LOW)

def red_light(flag):
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(YELLOW, GPIO.LOW)
    GPIO.output(RED, GPIO.HIGH)
    if flag == 1:    
        flag = click_picture(flag)
    return flag

def click_picture(flag):
    camera = picamera.PiCamera()
    #camera.vflip = True
    camera.start_recording('chor.h264')
    time.sleep(5)
    camera.stop_recording()
    flag = 0
    fromaddr = 'raspberrypitest7@gmail.com'
    toaddr = 'raspberrypitest7@gmail.com'
    
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    
    msg['Subject'] = 'SECURITY ALERT!'
    
    body = 'Intruder alert! Video Attached.'
    msg.attach(MIMEText(body, 'plain'))
    
    filename = 'chor.h264'
    attachment = open('/home/pi/Desktop/project/chor.h264', 'rb')
    
    p = MIMEBase('application', 'octet-stream')
    
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    
    p.add_header('Content-Disposition', 'attachment; filename = %s' % filename)
    msg.attach(p)
    
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, 'test12345!')
    
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
    
    return flag

def get_distance():

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == False:
        start = time.time()

    while GPIO.input(ECHO) == True:
        end = time.time()

    sig_time = end-start
    
    distance = sig_time / 0.000058
    return distance

flag = 1

while True:
    distance = get_distance()
    time.sleep(0.05)
    print(distance)
    
    
    if distance >= 200:
        no_lights()
    elif 200 > distance >= 30:
        green_light()
    elif 30 > distance > 10:
        yellow_light()
    elif distance <= 10:
        flag = red_light(flag)
