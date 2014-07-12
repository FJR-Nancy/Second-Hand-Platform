# coding=utf-8
import json
import requests

url_prefix = "http://10.180.38.137:8000/"

add_account_url = "json_api/add_account/"
add_account_data = {
    "name": u"小黄",
    "email": u"kunhuang110@gmail.com",
    "password": "123",
    "phone": "1234",
}

get_account_id_url = "json_api/get_account_id/"
get_account_id_data = {
    "email": u"kunhuang110@gmail.com",
    "password": "123",
}

get_account_info_url = "json_api/get_account_info/"
get_account_info_data = {
    "account_id": 1,
    "password": "123",
}

edit_account_info_url = "json_api/edit_account_info/"
edit_account_info_data = {
    "account_id": 1,
    "password": "123",
    "name": u"小黄",
    "phone": "1111"
}

add_goods_url = "json_api/add_goods/"
add_goods_data = {
    "seller_id": 1,
    "password": "123",
    "name": u"显示屏",
    "description": u"2013年",
    "pure_price": 400,
    #"photo"
}

get_transaction_array_url = "json_api/get_transaction_array/"
get_transaction_array_data = {
    "account_id": 1,
    "password": "123",
    "account_type": 0,
    #"photo"
}

r = requests.post(url_prefix + get_account_info_url, get_account_info_data)
print(r.content)