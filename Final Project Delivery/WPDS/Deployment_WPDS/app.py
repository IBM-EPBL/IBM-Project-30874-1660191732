import flask
from flask import request,render_template
from flask_cors import CORS
import joblib
from urllib.parse import urlparse,urlencode
import ipaddress
import re
import socket
import sklearn

app=flask.Flask(__name__,static_url_path='')
CORS(app)

@app.route('/',methods=['GET'])
def SendIndexPage():
    return render_template('index.html')

@app.route('/result',methods=['POST'])
def predictResult():
    url=request.form['URL']
    a=getDomain(url)
    b=havingIP(url)
    c=haveAtSign(url)
    d=getLength(url)
    e=getDepth(url)
    f=redirection(url)
    g=httpDomain(url)
    h=tinyURL(url)
    i=prefixSuffix(url)
    x=[[b,c,d,e,f,g,h,i]]
    model=joblib.load('Selected_Model.pkl')
    res=model.predict(x)[0]
    if(res==1):
      res1="Phished Website"
    elif(res==0):
      res1="Legitimate Website"
    return render_template('result.html',predict=res1)

# Getting the domain of the URL (Domain)
def getDomain(url):  
  domain = urlparse(url).netloc
  return domain

# Checking the IP address for URL (Have_IP)
def havingIP(url):
  try:
    ip_address = socket.gethostbyname(Domain)
    ip = 1
  except:
    ip = 0
  return ip

# Checking the presence of @ in URL (Have_At)
def haveAtSign(url):
  if "@" in url:
    at = 1    
  else:
    at = 0    
  return at

# Finding the length of URL (URL_Length)
def getLength(url):
  if len(url) < 54:
    length = 0            
  else:
    length = 1            
  return length

# Finding the number of '/' in URL (URL_Depth)
def getDepth(url):
  s = urlparse(url).path.split('/')
  depth = 0
  for j in range(len(s)):
    if len(s[j]) != 0:
      depth = depth+1
  return depth

# Checking for redirection '//' in the URL (Redirection)
def redirection(url):
  pos = url.rfind('//')
  if pos > 6:
    if pos > 7:
      return 1
    else:
      return 0
  else:
    return 0

# checking for presence of “HTTPS” in the Domain of the URL (https_Domain)
def httpDomain(url):
  if 'https' in url:
    return 1
  else:
    return 0

# Checking for Shortening Services in URL (Tiny_URL)
def tinyURL(url):
    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|"\
                          r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                          r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                          r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                          r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                          r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                          r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                           r"tr\.im|link\.zip\.net"
    match=re.search(shortening_services,url)
    if match:
        return 1
    else:
        return 0

# Checking for Prefix or Suffix Separated by (-) in the Domain (Prefix/Suffix)
def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1
    else:
        return 0 

if __name__=='__main__':
    app.run()