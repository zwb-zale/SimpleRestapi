from flask import current_app
from flask_babel import gettext as _
def health_get():
    """
    服务健康检查
    """
    try:
        data = {}
        return data, 200, {"content-type": "application/json;charset=utf8"}
    except Exception as e:
        current_app.logger.error(str(e),exc_info=True)
        return {"error": _(str(e))}, 422, {"content-type": "application/json;charset=utf8"}
