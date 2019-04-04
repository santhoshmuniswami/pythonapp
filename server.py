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

    if(page>0):
        url = WebUrl
        code = requests.get(url)
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
            if myvalue[1] ==  domain or myvalue[1] == '' or myvalue[1] == '/':
                listofpaths.append(myvalue[2])
                while '' in listofpaths:
                    listofpaths.remove('')


              #  print(listofpaths)

                finalset=set()
                finalset=set(listofpaths)
                print(finalset)

              #  print(len(listofpaths))
              #  print(len(finalset))
                count = count + 1

            # secondlist = []
            # for i in range(len(listofpaths)):
            #     splitedvalue = str(listofpaths[i]).split('/')
            #     while '' in splitedvalue:
            #         splitedvalue.remove('')
            #     if len(splitedvalue) > 0 and splitedvalue != ["b''"]:
            #
            #         secondlist.append(splitedvalue)


            # listofpaths.sort()
            # setoffinal=set(secondlist)
            # print(listofpaths)



        print(count)
        # mydict={"content":finalset}

        return list(finalset)


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

      actualURL = parsevalue[0] + "://" + parsevalue[1]

      finalset=web(1, actualURL, domain)

      return jsonify(finalset)
   else:
      my_dict = {'name': 'John', '1': [2, 4, 3]}

      return jsonify(my_dict)

if __name__ == '__main__':
   app.run(host='0.0.0.0')


