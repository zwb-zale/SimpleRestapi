from sqlalchemy import or_, and_, desc
from app.models import *
from flask import current_app
from flask_babel import gettext as _
from app.utils import set_timezone,todatetime
import time
def wechatphones_get(phone = None,finish_state = None):
    """
    :param page:
    :type page: integer
    :rtype:Wechatphone
    :param per_page:
    :type per_page: integer
    :rtype:Wechatphone
    """
    datap = Wechatphone.query
    header = {"content-type": "application/json;charset=utf8"}
    if phone:
        datap = datap.filter(Wechatphone.phone == phone)
    if finish_state is not None:
        datap = datap.filter(Wechatphone.finish_state == finish_state)
    datas = datap.order_by(desc(Wechatphone.id)).all()
    result = []
    for data in datas:
        temp_d = set_timezone(data.to_json())
        if temp_d["deviceid"] == "":
            temp_d["status_str"] = "未分配"
        else:
            if temp_d["finish_state"] == 0:
                tm = data.bind_timestamp
                if tm:
                    now_tm = int(time.time())
                    if (now_tm - tm) < 10*60:
                        temp_d["status_str"] = "被分配"
                    else:
                        temp_d["status_str"] = "可分配"
                else:
                    temp_d["status_str"] = "未分配"
            elif temp_d["finish_state"] == 1:
                temp_d["status_str"] = "操作成功！"
            elif temp_d["finish_state"] == 2:
                temp_d["status_str"] = "操作失败！"
        result.append(temp_d)
    return result ,200 ,header
def wechatphones_post(body):
    """
    :param body:
    :type body: object
    :rtype:Wechatphone
    """
    try:
        body["finish_state"] = 0
        body["finish_deviceid"] = ""
        body["deviceid"] = ""
        body["bind_timestamp"] = 0
        temp_data = Wechatphone.query.filter(Wechatphone.phone == body["phone"]).first()
        if temp_data is None:
            data = Wechatphone(**{k: v for k, v in body.items() if k in Wechatphone.__table__.columns.keys()})
            db.session.add(data)
            db.session.commit()
        else:
            Wechatphone.query.filter(Wechatphone.id == temp_data.id).update(body)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(str(e),exc_info=True)
        return {"error": _(str(e))}, 422, {"content-type": "application/json;charset=utf8"}
    return "ok", 201, {"content-type": "application/json;charset=utf8"}
def wechatphones_id_put(id,body):
    """
    :param id:
    :type id: integer
    :rtype:Wechatphone
    :param body:
    :type body: object
    :rtype:Wechatphone
    """
    return "", 201, {"content-type": "application/json;charset=utf8"}
    # try:
    #     body = todatetime({k: v for k, v in body.items() if k in Wechatphone.__table__.columns.keys()},[])
    #     Wechatphone.query.filter(Wechatphone.id == id).update(body)
    # except Exception as e:
    #     db.session.rollback()
    #     current_app.logger.error(str(e),exc_info=True)
    #     return {"error": _(str(e))}, 422, {"content-type": "application/json;charset=utf8"}
    # data = Wechatphone.query.filter_by(id=id).first_or_404()
    # return set_timezone(data.to_json()), 201, {"content-type": "application/json;charset=utf8"}
def set_device_for_data(deviceid):
    all_free_datas = Wechatphone.query\
        .filter(Wechatphone.finish_state == 0)\
        .order_by(desc(Wechatphone.id))\
        .all()
    for all_free_data in all_free_datas:
        if all_free_data.deviceid:
            tm = all_free_data.bind_timestamp
            if tm:
                now_tm = int(time.time())
                if (now_tm - tm) < 10*60:
                    continue
        all_free_data.deviceid = deviceid
        all_free_data.bind_timestamp = int(time.time())
        body = todatetime(
            {k: v for k, v in set_timezone(all_free_data.to_json()).items() if
             k in Wechatphone.__table__.columns.keys()}, [])
        Wechatphone.query.filter(Wechatphone.id == body["id"]).update(body)
        db.session.commit()
        return set_timezone(all_free_data.to_json())
    return {}
def fenpei_datat(deviceid):
    result = {}
    data = Wechatphone.query.filter(Wechatphone.deviceid == deviceid).first()
    if data is None:
        result = set_device_for_data(deviceid)
    else:
        if data.finish_deviceid == "" or data.finish_deviceid is None:
            data.bind_timestamp = int(time.time())
            result = set_timezone(data.to_json())
            Wechatphone.query.filter(Wechatphone.id == result["id"]).update(result)
            db.session.commit()
    return result
def belonguserdatas_get(deviceid):
    """
    获取分配给用户的资料
    :param deviceid:
    :type deviceid: string
    :rtype:Wechatphone
    """
    try:
        return fenpei_datat(deviceid), 200, {"content-type": "application/json;charset=utf8"}
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(str(e),exc_info=True)
        return {"error": _(str(e))}, 422, {"content-type": "application/json;charset=utf8"}
def finishwork_callback_post(body):
    """
    :param body:
    :type body: object
    :rtype:
    """
    try:
        new_body = {
            "finish_deviceid": body["deviceid"],
            "finish_state":body["finish_state"]
        }
        Wechatphone.query.filter(Wechatphone.phone == body["phone"]).update(new_body)
        db.session.commit()
        return "ok", 201, {"content-type": "application/json;charset=utf8"}
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(str(e), exc_info=True)
        return {"error": _(str(e))}, 422, {"content-type": "application/json;charset=utf8"}
def bulkadd_post(body):
    """
    批量新增
    :param body:
    :type body: object
    :rtype:
    """
    try:
        create_datas = []
        for sorce_data in body["datas"]:
            temp_data = Wechatphone.query.filter(Wechatphone.phone == sorce_data["phone"]).first()
            if temp_data is None:
                create_datas.append(sorce_data)
            else:
                Wechatphone.query.filter(Wechatphone.id == temp_data.id).update(sorce_data)
                db.session.commit()
        create_datas.reverse()
        db.session.bulk_insert_mappings(
            Wechatphone,
            create_datas
        )
        return '成功新增'+str(len(create_datas))+'笔，更新'+str(len(body["datas"])-len(create_datas))+'笔', 201, {"content-type": "application/json;charset=utf8"}
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(str(e),exc_info=True)
        return {"error": _(str(e))}, 422, {"content-type": "application/json;charset=utf8"}
def remove_datas_delete():
    """
    """
    try:
        db.session.execute("truncate table wechatphone")
        return "", 204
    except Exception as e:
        current_app.logger.error(str(e),exc_info=True)
        return {"error": _(str(e))}, 422, {"content-type": "application/json;charset=utf8"}
def reallocatephone_get(phone,deviceid):
    """
    废弃当前号码，重新分配新号码
    :param phone:
    :type phone: string
    :rtype:
    :param deviceid:
    :type deviceid: string
    :rtype:
    """
    try:
        data = Wechatphone.query.filter(Wechatphone.phone == phone).first()
        if data is not None:
            data.deviceid = "000000000000"
            data.finish_state = 2
            data.finish_deviceid = "000000000000"
            data.bind_timestamp = 0
            data.ppd = ""
            body = todatetime(
                {k: v for k, v in set_timezone(data.to_json()).items() if
                 k in Wechatphone.__table__.columns.keys()}, [])
            Wechatphone.query.filter(Wechatphone.id == data.id).update(body)
            db.session.commit()
        return fenpei_datat(deviceid), 200, {"content-type": "application/json;charset=utf8"}
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(str(e), exc_info=True)
        return {"error": _(str(e))}, 422, {"content-type": "application/json;charset=utf8"}
def ppd_post(phone,deviceid,ppd):
    """
    :param phone:
    :type phone: string
    :rtype:
    :param deviceid:
    :type deviceid: string
    :rtype:
    :param ppd:
    :type ppd: string
    :rtype:
    """
    try:
        datas = Wechatphone.query.filter(and_(Wechatphone.phone == phone,Wechatphone.deviceid == deviceid)).all()
        for data in datas:
            data.ppd = ppd
            result = set_timezone(data.to_json())
            Wechatphone.query.filter(Wechatphone.id == result["id"]).update(result)
        db.session.commit()
        return "ok", 201, {"content-type": "application/json;charset=utf8"}
    except Exception as e:
        current_app.logger.error(str(e),exc_info=True)
        return {"error": _(str(e))}, 422, {"content-type": "application/json;charset=utf8"}
