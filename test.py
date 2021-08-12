import requests 
from bs4 import BeautifulSoup 
from PIL import Image, ImageDraw
import pycurl
from urllib.parse import urlencode

start_url = "http://www.proveyourworth.net/level3/start"
activate_url = "http://www.proveyourworth.net/level3/activate?statefulhash"
payload_url = "http://www.proveyourworth.net/level3/payload"

session = requests.Session()

def start_session(start_url):
    session.get(start_url)

def get_hash(start_url):
    request = session.get(start_url)
    soup = BeautifulSoup(request.text, 'html.parser')
    return soup.find("input",{"name":"statefulhash"})['value']

def activate(activate_url,get_hash):
    get_hash = get_hash(start_url)
    session.get("{}={}".format(activate_url,get_hash))
  
def get_image_to_sign(url_image):
    request = session.get(url_image,stream=True)
    image = request.raw
    return image

def write_image(image):
    image = Image.open(image)
    draw = ImageDraw.Draw(image)
    draw.text((20,70), "Alejandro Aparicio Guerra, \n Hash:{} \n dlaparicio87@gmail.com \n Backend Developer".format(get_hash(start_url)), fill=(50,168,82))
    image.save("image.jpg","JPEG")

def upload_pycurl(payload):
    pay = session.get(payload)
    post_url = "{}".format(pay.headers['X-Post-Back-To'])

    data = {
        "email":"dlaparicio87@gmail.com",
        "name":"Alejandro Aparicio Guerra",
        "aboutme": "I'm backend developer in Python, Javascript and PHP and with knowledges of fronted libraries as React.js."
    }
    
    c = pycurl.Curl()
    c.setopt(c.URL, post_url)

    # Form data must be provided already urlencoded.
    postfields = urlencode(data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)

    c.setopt(c.UPLOAD, 1)
    code = open("test.py","rb")
    resume = open( "cv.pdf","rb")
    image = open("image.jpg","rb")

    c.setopt(c.READDATA, code)
    c.setopt(c.READDATA, resume)
    c.setopt(c.READDATA, image)

    c.perform()
    c.close()
    code.close()
    resume.close()
    image.close()


if __name__ == '__main__':
    print('Start Session')
    start_session(start_url)
    print('End Session')
    print('Start Activation')
    activate(activate_url,get_hash)
    print('End Activation')
    print('Start Write Image')
    write_image(get_image_to_sign(payload_url))
    print('End Write Image')
    print('Start Upload Files')
    upload_pycurl(payload_url)
    print('End Upload Files')
    