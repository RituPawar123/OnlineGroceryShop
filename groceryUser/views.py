from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.http.response import JsonResponse
from . import models
import json
from datetime import datetime

from collections import defaultdict

currentOrder = 0
# def home(request):
#     print("User Home")
#     if 'email' in request.COOKIES :
#         query = "select * from currentorders where userId = '%s' " % (request.COOKIES['email'].split('@')[0])
#         models.cursor.execute(query)
#         currentOrder = models.cursor.fetchall()
#         if currentOrder:
#             currentOrder = 1
#         else:
#             currentOrder = 0
#         return render(request,'userHome.html',{'currentOrder':currentOrder})
#     else:
#         return redirect("http://localhost:8000/")

def home(request):
    if 'email' in request.COOKIES :
        query = "select * from currentorders where userId = '%s' " % (request.COOKIES['email'].split('@')[0])
        models.cursor.execute(query)
        currentOrder = models.cursor.fetchall()
        if currentOrder:
            currentOrder = 1
        else:
            currentOrder = 0
        query = "select catimg , catnm, catdesc ,catid from catagory"
        models.cursor.execute(query)
        catagories = list(models.cursor.fetchall())

        for i in range(len(catagories)):
            query = "select varietyName ,varietyImg,varietyId from variety where catId = '%s'"%(catagories[i][3])
            models.cursor.execute(query)
            catagories[i] = list(catagories[i])
            catagories[i].append(models.cursor.fetchall())
            
        return render(request,'userHome.html',{'currentOrder':currentOrder,'catagories': catagories})
    else:
        return redirect("http://localhost:8000/")



def product(request):
    if 'email' in request.COOKIES :
        varietyId = request.GET.get('varietyId')
        print("VAriety : ",varietyId)
        query = 'select * from subvariety'
        if varietyId:
         query = "select * from subvariety where varietyId = '%s'"%(varietyId)
        models.cursor.execute(query)
        subvarietyData = models.cursor.fetchall()
        print(subvarietyData)
        return render(request, 'userSubVariety.html', {'items': subvarietyData, 'currentOrder': currentOrder})
    else:
        return redirect("http://localhost:8000/")
    # queryForCatagory = "select * from catagory"
    # models.cursor.execute(queryForCatagory)
    # catagoryData = models.cursor.fetchall()
    #
    # queryForItems = "select * from variety order by catId"
    # models.cursor.execute(queryForItems)
    # varietyData = [list(i) for i in models.cursor.fetchall()]
    # varietyData = list(varietyData)
    # globalData = [
    # ]
    # tempDict = defaultdict(list)
    # for i in varietyData:
    #     try:
    #         if tempDict[i[1]]:
    #             temp = list(i)
    #             temp[5] = 'image/' + temp[5]
    #             tempDict[i[1]].append(temp)
    #     except:
    #         temp = list(i)
    #         temp[5] = 'image/' + temp[5]
    #         tempDict[i[1]] = [temp, ]
    # for i in range(len(catagoryData)):
    #     globalData.append(
    #         [ catagoryData[i][1], 'image/' + catagoryData[i][2], catagoryData[i][3], tempDict[catagoryData[i][0]]])
    #
    # return render('', {'catagories': globalData})


def about(request):
    query = "select * from currentorders where userId = '%s' " % (request.COOKIES['email'].split('@')[0])
    models.cursor.execute(query)
    currentOrder = models.cursor.fetchall()
    if currentOrder:
        currentOrder = 1
    else:
        currentOrder = 0
    if 'email' in request.COOKIES :
        return render(request,'AboutUs.html',{'currentOrder':currentOrder})
    else:
        return redirect("http://localhost:8000/")

def contact(request):
    if 'email' in request.COOKIES :
        return render(request,'contact.html',{})
    else:
        return redirect("http://localhost:8000/")
# def product(request):
#     query = "select * from subvariety"
#     models.cursor.execute(query)
#     subvarietyData = models.cursor.fetchall()
#     return render(request,'userSubVariety.html',{'items':subvarietyData,'currentOrder':currentOrder})

def cart(request):
    if 'email' in request.COOKIES :
        if request.method=="GET":
           return render(request,'cart.html',{'currentOrder':currentOrder})
        else:
           orderItems=json.loads(request.POST.get('groceryItems'))
           print(type(orderItems))
           print(orderItems)
        address=request.POST.get('address')
        deliveryNote=request.POST.get('deliveryNote')
        cartNumber=request.POST.get('cartNumber')
        query = "select count(orderId) from orders";
        models.cursor.execute(query)
        orderId = 'ORD000'+str(models.cursor.fetchall()[0][0]+1)
        userId = request.COOKIES['email'].split('@')[0]
        print("CArt : ",userId)
        now = datetime.now()
        orderTime =now.strftime("%d/%m/%Y %H:%M:%S")
        query = "insert into orders (orderId,userId,orderTime,deliveryNote,address,orderItems) values('%s','%s','%s','%s','%s','%s')"%(orderId,userId,orderTime,deliveryNote,address,orderItems)
        models.cursor.execute(query)
        models.db.commit()
        
        query = "insert into currentorders (orderId,userId) values('%s','%s')"%(orderId,userId)
        models.cursor.execute(query)
        models.db.commit()

        return JsonResponse({'output':1})
    else:
        return redirect("http://localhost:8000/")

def AboutUs(request):
    if 'email' in request.COOKIES :
        return render(request,'AboutUs.html',{'currentOrder':currentOrder})
    else:
        return redirect("http://localhost:8000/")

def ContactUs(request):
    if 'email' in request.COOKIES :
         return render(request,'ContactUs.html',{'currentOrder':currentOrder})
    else:
        return redirect("http://localhost:8000/")

def userfeedback(request):
    if 'email' in request.COOKIES :
        return render(request, 'userfeedback.html', {'currentOrder': currentOrder})
    else:
        return redirect("http://localhost:8000/")

    #return redirect('http://localhost:8000/groceryUser/userfeedback')

# def userfeedback(request):
#     if 'email' in request.COOKIES:
#          return redirect('http://localhost:8000/groceryUser/userfeedback')
#     else:
#         return render(request, 'userfeedback.html')

def logout(request):
   if 'email' in request.COOKIES:
       response = redirect('http://localhost:8000/')
       response.delete_cookie('email')
       return response
   else:
       return redirect('http://localhost:8000/')

def trackOrder(request):
    query="select * from currentorders where userId='%s' "%(request.COOKIES['email'].split('@')[0].lower())
    models.cursor.execute(query)
    currentOrderData=models.cursor.fetchall()[0]
    print(currentOrderData)
    status=currentOrderData[2]
    orderId=currentOrderData[0]
    print("status : ",status)
    return render(request,'trackorder.html',{'status':status,'orderId':orderId})