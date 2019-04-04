import requests
from bs4 import BeautifulSoup
from requests.compat import urljoin
from requests.compat import urlparse
from flask import Flask, redirect, url_for, request
from flask import jsonify
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
#app.config['CORS_HEADERS'] = 'application/json'

#CORS(app)
app.config["DEBUG"] = True


def web(page,WebUrl,domain):
    count = 0
    myjson={}
    myjson[WebUrl]={}

    listofpaths=[]
    differentdomain=[]

    if(page>0):
        url = WebUrl
        try:
            code = requests.get(url)
        except:
            print("I couldn't fetch the URL ! Please check the URL")
            errorresponse=["I couldn't fetch this URL. Please check the url!"]
            return errorresponse

        # print(code)
        plain = code.text
        # print(plain)
        s = BeautifulSoup(plain, "html.parser")
        # print(s)

        for link in s.findAll('a'):
            print("..................")
            # tet = link.get('title')
            # print(tet)
            tet_2 = link.get('href')
            # print(tet_2)
            # print(urljoin(tet_2, '.'))
            # print(urlparse(tet_2))
            myvalue=urlparse(tet_2)
            print(myvalue)
            appendwww="www."+domain
            print(appendwww)
            if myvalue[1] == domain or myvalue[1] == '' or myvalue[1] == '/' or myvalue[1] == appendwww:
                print(myvalue[2])
                listofpaths.append(myvalue[2])
            else:
                differentdomain.append(myvalue[1]+myvalue[2])


        while '' in listofpaths:
            listofpaths.remove('')

        print(listofpaths)
        finalset=set(listofpaths)
        print(finalset)

        print(len(listofpaths))
        print(len(finalset))
        count = count + 1



        print(count)
        # mydict={"content":finalset}

        listoffinalset= list(finalset)
        if(len(listoffinalset)==0):
            listoffinalset=differentdomain

        return listoffinalset


@app.route('/sitemap',methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
      print("Request received at "+str(datetime.now()))
      url = request.get_json()
      if 'url' not in url:
          raise ValueError("Please pass the URL in the payload")

          data = {"error":"Please pass the URL in the payload"}
          js = json.dumps(data)

          resp = Response(js, status=400, mimetype='application/json')
          return resp

      myurl = url['url']
      parsevalue = urlparse(myurl)
      print(parsevalue)

      domain = parsevalue[1]
      protocal = parsevalue[0]
      domainname=parsevalue[1]
      if(parsevalue[0]==''):
          protocal='http'
          domainname=parsevalue[2]
          domain=parsevalue[2]



      actualURL = protocal + "://" + domainname

      finalresponse=web(1, actualURL, domain)

      return jsonify(finalresponse)
   else:
      my_dict = {'name': 'John', '1': [2, 4, 3]}

      return jsonify(my_dict)

if __name__ == '__main__':
   app.run(host='0.0.0.0')

