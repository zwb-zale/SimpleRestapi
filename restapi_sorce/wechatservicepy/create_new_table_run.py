def create_dev_db():
    from app import create_app_swagger, db
    app_sw = create_app_swagger('default')
    app = app_sw.app
    app_context = app.app_context()
    app_context.push()
    db.create_all()
if __name__ == '__main__':
    create_dev_db()
