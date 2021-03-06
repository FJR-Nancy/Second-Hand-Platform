# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse

from json_api.models import Account_Info, Goods_Info, Log_Info, Message_Info, Comment_Info, Wish_List

import json
import time
from django.forms.models import model_to_dict
from django.db.models import Q

import helper
from PIL import Image
#import ContentFile
#import StringIO
    
error = {
    'success': 0,
    'error_type': 0, #Unknown Error
}
success = {
    'success': 1,
}
def getSuccessJson(models):
    data = {
              'total':len(models),
              'rows': [model_to_dict(item) for item in models ]
            }

    success = {
        'success': 1,
        'data': data,
    }

    json_data = json.dumps(success)
    return json_data

def index(request):
	return HttpResponse('Hello World')

def add_account(request):
    try:
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST.get('phone')
        bank_card = request.POST.get('bank_card')

        if phone == None:
            phone = ''
        if bank_card == None:
            bank_card = ''

        if Account_Info.objects.filter(email = email).exists():
            error['error_type'] = -2
            return HttpResponse(json.dumps(error))

        Account_Info.objects.create(
            name = name,
            email = email,
            password = password,
            phone = phone,
            sell_exp = 0,
            buy_exp = 0,
            )
        return HttpResponse(json.dumps(success))

    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))

def add_photo(request):
    try:
        photo = request.FILES['photo']
        photo.name = str(int(time.time())) + photo.name[-4:] 
        print photo
        account = Account_Info.objects.get(id = 1)
        #photo_content = ContentFile(photo.read())
        account.photo = photo
        account.save()

        return HttpResponse(json.dumps(success))
    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass
def get_photo(request):
    try:
        photo = Account_Info.objects.get(id = 1).photo
        #context = "<img src='%s' />" % photo.url
        photo_content = photo.open(mode='rb')
        return HttpResponse(photo_content)
    except Exception, e:
        print e
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass
def get_account_id(request):
    try:
        email = request.POST['email']
        password = request.POST['password']

        account_id = Account_Info.validate_email(email = email, password = password)
        if account_id == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))
        else:
            success['id'] = account_id
            return HttpResponse(json.dumps(success))
    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))

def get_account_info(request):
    try:
        account_id = request.POST['account_id']
        password = request.POST['password']

        #super user
        if password == '123':
            account_info_array = Account_Info.objects.filter(id = account_id)
            return HttpResponse(getSuccessJson(account_info_array))

        if Account_Info.validate_id(id = account_id, password = password) == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))
        else:
            account_info_array = Account_Info.objects.filter(id = account_id)
            return HttpResponse(getSuccessJson(account_info_array))
    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))

def edit_account_info(request):
    try:
        account_id = request.POST['account_id']
        password = request.POST['password']
        
        phone = request.POST.get('phone')
        new_password = request.POST.get('new_password')
        name = request.POST.get('name')
        bank_card = request.POST.get('bank_card')

        if Account_Info.validate_id(id = account_id, password = password) == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))
        
        else:
            account_info = Account_Info.objects.get(id = account_id)
            if phone != None:
                account_info.phone = phone
            if new_password != None:
                account_info.password = new_password
            if name != None:
                account_info.name = name
            if bank_card != None:
                account_info.bank_card = bank_card

            account_info.save()
            return HttpResponse(json.dumps(success))
    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))

def add_goods(request):
    try:
        seller_id =  request.POST['seller_id']
        password = request.POST['password']
        name = request.POST['name']
        pure_price = request.POST['pure_price']

        description = request.POST.get('description')
        if description == None:
            description = ""
        #photo

        if Account_Info.validate_id(id = seller_id, password = password) == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))

        goods = Goods_Info.objects.create(
            name = name,
            description = description,
            seller_id = Account_Info.objects.get(id = seller_id),
            state = 'I',
            pure_price = pure_price,
            #buyer_id = 0,
            )
        
        log = Log_Info.objects.create(
            goods_id = goods,
            time = int(time.time()),
            type = 'I',
            )
        
        success['goods_id'] = goods.id
        
        return HttpResponse(json.dumps(success))

    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass

def get_goods_info(request):
    try:
        #seller_id =  request.POST['seller_id']
        #password = request.POST['password']
        goods_id = request.POST['goods_id']

        '''
        if Account_Info.validate_id(id = seller_id, password = password) == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))
        '''

        goods_array = Goods_Info.objects.filter(id = goods_id)
        return HttpResponse(getSuccessJson(goods_array))

    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass

def get_my_goods_array(request):
    try:
        account_id =  request.POST['account_id']
        password = request.POST['password']
        account_type = request.POST['account_type']
        goods_num = request.POST.get('goods_num')

        print goods_num
        if Account_Info.validate_id(id = account_id, password = password) == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))

        if account_type == '0':
            goods_array = Goods_Info.objects.filter(seller_id = account_id)
        elif account_type == '1':
            goods_array = Goods_Info.objects.all()

        if goods_num != None:
            goods_array = goods_array.order_by('-id')[:goods_num]
        
        return HttpResponse(getSuccessJson(goods_array))
    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass

def get_goods_array(request):
    try:
        goods_num = request.POST.get('goods_num')
        state = request.POST.get('state')

        goods_array = Goods_Info.objects.all().order_by('-id')
        if goods_num != None:
            goods_array = goods_array[:goods_num]
        
        if state != None:
            goods_array = goods_array.filter(state = state)
        
        return HttpResponse(getSuccessJson(goods_array))
    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass

def edit_goods_info(request):
    try:
        seller_id =  request.POST['seller_id']
        password = request.POST['password']
        goods_id = request.POST['goods_id']

        name = request.POST.get('name')
        description = request.POST.get('description')
        pure_price = request.POST.get('pure_price')
        #photo

        #super user
        if password!='123' and Account_Info.validate_id(id = seller_id, password = password) == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))

        goods = Goods_Info.objects.filter(id = goods_id, seller_id = seller_id)
        if goods.exists() == False:
            error['error_type'] = -4
            return HttpResponse(json.dumps(error))

        goods = Goods_Info.objects.get(id = goods_id)
        if pure_price != None and goods.state != 'I':
            error['error_type'] = -4
            return HttpResponse(json.dumps(error))

        if pure_price != None:
            goods.pure_price = pure_price
        if description != None:
            goods.description = description
        if name != None:
            goods.name = name
        goods.save()

        log = Log_Info.objects.create(
            goods_id = Goods_Info.objects.get(id = goods.id),
            time = int(time.time()),
            type = 'U',
            )

        return HttpResponse(json.dumps(success))
    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass

def transact_goods(request):
    try:
        account_id =  request.POST['account_id']
        password = request.POST['password']
        account_type = request.POST['account_type']
        goods_id = request.POST['goods_id']
        type = request.POST['type']

        #super user
        if password != '123' and Account_Info.validate_id(id = account_id, password = password) == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))

        if account_type == '0':#seller
            goods = Goods_Info.objects.filter(id = goods_id, seller_id = account_id)
        
            if goods.exists() == False:
                error['error_type'] = -4
                return HttpResponse(json.dumps(error))

            goods = goods[0]
            if (type == 'O' or type == 'C') and goods.state == 'I':
                goods.state = type
                goods.save()
                log = Log_Info.objects.create(
                    goods_id = goods,
                    time = int(time.time()),
                    type = type,
                    )
                return HttpResponse(json.dumps(success))
            error['error_type'] = -4
            return HttpResponse(json.dumps(error))
        elif account_type == '1':#buyer
            goods = Goods_Info.objects.filter(id = goods_id)
        
            if goods.exists() == False:
                error['error_type'] = -3
                return HttpResponse(json.dumps(error))

            goods = goods[0]
            if (type == 'B') and goods.state == 'O':
                goods.state = type
                goods.buyer_id = Account_Info.objects.get(id = account_id)
                goods.save()
                log = Log_Info.objects.create(
                    goods_id = goods,
                    time = int(time.time()),
                    type = type,
                    )
                return HttpResponse(json.dumps(success))
            error['error_type'] = -4
            return HttpResponse(json.dumps(error))
        else:
            error['error_type'] = -4
            return HttpResponse(json.dumps(error)) 
    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass

def get_transaction_array(request):
    try:
        account_id =  request.POST['account_id']
        password = request.POST['password']
        account_type = request.POST.get('account_type')

        if account_type == None:
            account_type = '2'

        if Account_Info.validate_id(id = account_id, password = password) == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))

        
        if account_type == '0':#seller
            
            raw_sql = 'select * from json_api_log_info where goods_id_id in'
            raw_sql = raw_sql+'(select id from json_api_goods_info where seller_id_id=%s)'%account_id
            
            print raw_sql
            log_array = Log_Info.objects.raw(raw_sql)
            
            #无法直接使用getSuccessJson()
            total = 0
            for log in log_array:
                total = total + 1
            
            data = {
              'total':total,
              'rows': [model_to_dict(item) for item in log_array]
            }
            success['data'] = data
            json_data = json.dumps(success)

            #print type(log_array)
            return HttpResponse(json_data)
        elif account_type == '1':#buyer
            raw_sql = 'select * from json_api_log_info where goods_id_id in'
            raw_sql = raw_sql+'(select id from json_api_goods_info where buyer_id_id = %s)'%account_id
            
            log_array = Log_Info.objects.raw(raw_sql)
            
            #无法直接使用getSuccessJson()
            total = 0
            for log in log_array:
                total = total + 1
            
            data = {
              'total':total,
              'rows': [model_to_dict(item) for item in log_array]
            }
            success['data'] = data
            json_data = json.dumps(success)

            #print type(log_array)
            return HttpResponse(json_data)
        elif account_type == '2':#同时返回
            raw_sql = 'select * from json_api_log_info where goods_id_id in'
            raw_sql = raw_sql+'(select id from json_api_goods_info where buyer_id_id = %s or seller_id_id = %s)' % (account_id,account_id)
            
            log_array = Log_Info.objects.raw(raw_sql)
            
            #无法直接使用getSuccessJson()
            total = 0
            for log in log_array:
                total = total + 1
            
            data = {
              'total':total,
              'rows': [model_to_dict(item) for item in log_array]
            }
            success['data'] = data
            json_data = json.dumps(success)

            #print type(log_array)
            return HttpResponse(json_data)
            
        else:
            error['error_type'] = -4
            return HttpResponse(error)
        
    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass

def add_comment(request):
    try:
        account_id =  request.POST['account_id']
        password = request.POST['password']
        goods_id = request.POST['goods_id']
        content = request.POST['content']

        if Account_Info.validate_id(id = account_id, password = password) == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))

        if Goods_Info.objects.filter(id = goods_id).exists() == False:
            error['error_type'] = -3
            return HttpResponse(json.dumps(error))

        Comment_Info.objects.create(
            account_id = Account_Info.objects.get(id = account_id),
            goods_id = Goods_Info.objects.get(id = goods_id),
            time = int(time.time()),
            content = content,
            )

        return HttpResponse(json.dumps(success))
    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass

def get_comment_array(request):
    try:
        #account_id =  request.POST['account_id']
        #password = request.POST['password']
        goods_id = request.POST['goods_id']
        
        '''
        if Account_Info.validate_id(id = account_id, password = password) == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))
        '''
        
        if Goods_Info.objects.filter(id = goods_id).exists() == False:
            error['error_type'] = -3
            return HttpResponse(json.dumps(error))

        comment_array = Comment_Info.objects.filter(goods_id = goods_id)
        return HttpResponse(getSuccessJson(comment_array))
    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass

def add_wishlist(request):
    try:
        buyer_id =  request.POST['buyer_id']
        password = request.POST['password']
        goods_id = request.POST['goods_id']
        #option

        if Account_Info.validate_id(id = buyer_id, password = password) == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))

        if Goods_Info.objects.filter(id = goods_id).exists() == False:
            error['error_type'] = -3
            return HttpResponse(json.dumps(error))

        if Wish_List.objects.filter(goods_id = goods_id, account_id = buyer_id).exists():
            error['error_type'] = -5
            return HttpResponse(json.dumps(error))

        Wish_List.objects.create(
            account_id = Account_Info.objects.get(id = buyer_id),
            goods_id = Goods_Info.objects.get(id = goods_id)    ,
            time = int(time.time()),
            payed = 0,
            )

        return HttpResponse(json.dumps(success))

    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass

def get_wishlist(request):
    try:
        buyer_id =  request.POST['buyer_id']
        password = request.POST['password']
        #option

        if Account_Info.validate_id(id = buyer_id, password = password) == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))

        wish_list_array = Wish_List.objects.filter(account_id = buyer_id)
        return HttpResponse(getSuccessJson(wish_list_array))

    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass

def delete_wishlist(request):
    try:
        buyer_id =  request.POST['buyer_id']
        password = request.POST['password']
        goods_id = request.POST['goods_id']
        #option

        if Account_Info.validate_id(id = buyer_id, password = password) == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))

        if Goods_Info.objects.filter(id = goods_id).exists() == False:
            error['error_type'] = -3
            return HttpResponse(json.dumps(error))

        wish_list = Wish_List.objects.filter(goods_id = goods_id, account_id = buyer_id)
        if wish_list.exists() == False:
            error['error_type'] = -6
            return HttpResponse(json.dumps(error))

        wish_list.delete()

        return HttpResponse(json.dumps(success))

    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass

def send_message(request):
    try:
        account_id =  request.POST['account_id']
        password = request.POST['password']
        recv_account_id = request.POST['recv_account_id']
        subject = request.POST['subject']
        content = request.POST['content']

        if Account_Info.validate_id(id = account_id, password = password) == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))

        if Account_Info.objects.filter(id = recv_account_id).exists() == False:
            error['error_type'] = -7
            return HttpResponse(json.dumps(error))

        Message_Info.objects.create(
            send_account_id = account_id,
            recv_account_id = Account_Info.objects.get(id = recv_account_id),
            time = int(time.time()),
            subject = subject,
            content = content,
            state = 0,
            )
        
        return HttpResponse(json.dumps(success))

    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass

def get_message_array(request):
    try:
        account_id =  request.POST['account_id']
        password = request.POST['password']
        
        if Account_Info.validate_id(id = account_id, password = password) == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))

        message_array = Message_Info.objects.filter(recv_account_id = account_id)
        return HttpResponse(getSuccessJson(message_array))
    except Exception, e:
        print e
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass

def get_message(request):
    try:
        account_id =  request.POST['account_id']
        password = request.POST['password']
        message_id = request.POST['message_id']

        if Account_Info.validate_id(id = account_id, password = password) == False:
            error['error_type'] = -1
            return HttpResponse(json.dumps(error))

        message = Message_Info.objects.filter(message_id = message_id)
        if message_id.exists() == False:
            error['error_type'] = -8
            return HttpResponse(json.dumps(error))

        return HttpResponse(getSuccessJson(message))
    except Exception, e:
        print e
        error['error_type'] = 0
        return HttpResponse(json.dumps(error))
    else:
        pass
    finally:
        pass
def test(request):
    
    '''goods = Goods_Info.objects.create(
        name = '苹果手机',
        description = '半新品',
        seller_id = 1,
        state = 'I',
        pure_price = 8000,
        )
    '''
    option = request.GET['option']
    if request.GET['option'] == '1':
        return HttpResponse("hello")
    elif request.GET['option'] == '2':
        tmp = Wish_List.objects.select_related().filter(id = 1)
        
        total = 0
        for log in tmp:
            total = total + 1
            
        data = {
          'total': total,
          'rows': [model_to_dict(item) for item in tmp]
        }

        for d in data['rows']:
            account_dict = model_to_dict(Account_Info.objects.get(id = d['account_id']))
            del account_dict['id']
            d.update(account_dict)
            #d.insert()
        
        success['data'] = data
        json_data = json.dumps(success)

        #print type(log_array)
        return HttpResponse(json_data)
        return HttpResponse(json.dumps(getSuccessJson(tmp)))
    
    return HttpResponse("None")
def test2(request):
    tmp = Wish_List.objects.select_related('Account_Info')
    return HttpResponse(json.dumps(getSuccessJson(tmp)))
