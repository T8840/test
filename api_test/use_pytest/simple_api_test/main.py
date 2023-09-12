import json
import requests
from utils import Excel,MyPymysqlPool


# 获得接口数据流
er = Excel(file_name="./API.xlsx", mode='r')
excel_apis = er.read2dict(sheet_name='接口库')
excel_variables = er.read2dict(sheet_name='公共变量')


def sqlRariable():
    # 数据库变量返回
    with MyPymysqlPool("TestMysql") as db:
        combine_inquiry_sql = f"select inquiry_number from iffm_combine_inquiry where inquiry_name = '接口自动化-测试' ORDER BY id DESC limit 1"
        if db.getOne(combine_inquiry_sql):
            # 获取联运询价号
            get_combine_inquiry_number = db.getOne(combine_inquiry_sql)["inquiry_number"]

            # 查询陆运id与陆运询价号
            land_inquiry_sql = f"select * from iffm_land_inquiry where combine_inquiry_number = '{get_combine_inquiry_number}' ORDER BY id DESC limit 1"
            get_land_inquiry_id = db.getOne(land_inquiry_sql)["id"]
            get_land_inquiry_number = db.getOne(land_inquiry_sql)["inquiry_number"]


            # 查询空运联运询价号-陆运报价id与陆运询价号
            air_inquiry_sql = f"select * from iffm_air_inquiry where combine_inquiry_number = '{get_combine_inquiry_number}' ORDER BY id DESC limit 1"
            get_air_inquiry_id = db.getOne(air_inquiry_sql)["id"]
            get_air_inquiry_number = db.getOne(air_inquiry_sql)["inquiry_number"]

            # 查询空运报价方案id
            air_quotation_sql = f"select * from iffm_air_quotation where inquiry_number = '{get_air_inquiry_number}' ORDER BY id DESC limit 1"
            if db.getOne(air_quotation_sql):
                get_air_quotation_id = db.getOne(air_quotation_sql)["id"]

            # 查询陆运报价方案id
            land_quotation_sql = f"select * from iffm_land_price_scheme where inquiry_id = '{get_land_inquiry_id}' ORDER BY id DESC limit 1"
            if db.getOne(land_quotation_sql):
                get_land_quotation_id = db.getOne(land_quotation_sql)["id"]

            if db.getOne(air_quotation_sql) and db.getOne(land_quotation_sql):

                sql_variables = {
                    "联运询价号":get_combine_inquiry_number,
                    "陆运询价id":str(get_land_inquiry_id),
                    "陆运询价号":get_land_inquiry_number,
                    "空运id":str(get_air_inquiry_id),
                    "空运询价号":get_air_inquiry_number,
                    "空运报价id":str(get_air_quotation_id),
                    "陆运报价id":str(get_land_quotation_id)
                }
                # print(sql_variables)
                return sql_variables
            else:
                sql_variables = {
                    "联运询价号": get_combine_inquiry_number,
                    "陆运询价id": str(get_land_inquiry_id),
                    "陆运询价号": get_land_inquiry_number,
                    "空运id": str(get_air_inquiry_id),
                    "空运询价号": get_air_inquiry_number
                }
                # print(sql_variables)
                return sql_variables

# 处理层
def beforeRequest(excel_api):
    """在请求前 对请求数据做处理
        1.格式转换
        2.变量处理
    """
    # 变量替换
    if excel_variables:

        for excel_variable in excel_variables:
            if excel_variable["flag"] != "Y":
                continue

            # values中包含"数据库变量-"字段会截取后面的去调用sqlReRariable函数
            if "数据库变量-" in excel_variable["values"]:
                if sqlRariable():
                    excel_variable["values"] = sqlRariable()[excel_variable["values"].split("-")[1]]

            # url中变量替换
            if excel_variable["location"] == "url":
                excel_api["url"] = excel_api["url"].replace(excel_variable['key'],excel_variable['values'])

            # headers中变量替换
            if excel_variable["location"] == "headers":
                excel_api["headers"] = excel_api["headers"].replace(excel_variable['key'],excel_variable['values'])

            # data中变量替换
            if excel_variable["location"] == "data":
                excel_api["data"] = excel_api["data"].replace(excel_variable['key'],excel_variable['values'])



    excel_api["url"] = excel_api["host"] + excel_api["url"]
    excel_api["headers"] = eval(excel_api["headers"])
    excel_api["data"] = json.dumps(json.loads(excel_api["data"]))

    # 整合待发送的数据
    send_request_data = {
        'url': excel_api["url"],
        'headers': excel_api["headers"],
        'method': excel_api["method"],
        'data': excel_api["data"]
    }
    # print(send_request_data)
    return send_request_data



# 执行层
def runRequest(send_request_data):
    response = requests.request(**send_request_data).text
    response = json.loads(response)
    print(response)


if __name__ == "__main__":
    for excel_api in excel_apis:
        if excel_api["flag"] != "Y":
            continue
        send_request_data = beforeRequest(excel_api)
        print("调用接口%s返回:" % send_request_data["url"])
        runRequest(send_request_data)