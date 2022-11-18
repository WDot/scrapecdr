from routes import create_app
from waitress import serve

app = create_app()

if __name__ == "__main__":

    #app.run(host='0.0.0.0',port=443,threaded=True,ssl_context=('localhost+2.pem','localhost+2-key.pem'))
    serve(app, host="0.0.0.0",port=80)