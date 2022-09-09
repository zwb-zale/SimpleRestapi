from app import create_app_swagger

if __name__ == '__main__':
    app = create_app_swagger('default')
    app.run(host='0.0.0.0')



