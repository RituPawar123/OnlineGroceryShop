from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.http.response import JsonResponse

from . import models
class AdminHome:
    def home(self,request):
        if 'adminId' in request.COOKIES:
            query = "select * from  currentorders"
            models.cursor.execute(query)
            currentOrders = models.cursor.fetchall()
            if currentOrders:
                print("")
            else:
                currentOrders = None
            return render(request,'adminHome.html',{'orders':currentOrders})
        else:
            return redirect('http://localhost:8000/')

    def allOrders(self, request):
        if 'adminId' in request.COOKIES:
            query = "select orderId, userId, orderTime, address, paymentMethod, orderStatus from orders"
            models.cursor.execute(query)
            allOrders = models.cursor.fetchall()
            if allOrders:
               print("")
            else:
               allOrders = None
            return render(request, 'allOrders.html', {'orders': allOrders})
        else:
            return redirect('http://localhost:8000/')

    def confirmOrder(self,request):
        if 'adminId' in request.COOKIES:
            if request.method=="POST":
             orderId = request.POST.get('orderId')
            query = "update currentorders set orderStatus = '%d' where orderId = '%s' "%(1,orderId)
            models.cursor.execute(query)
            models.db.commit()
            return JsonResponse({'output':1})
        else:
            return redirect('http://localhost:8000/groceryAdmin/')

    def prepareOrder(self,request):
        if 'adminId' in request.COOKIES:
            if request.method=="POST":
             orderId = request.POST.get('orderId')
            query = "update currentorders set orderStatus = '%d' where orderId = '%s' " %(2,orderId)
            models.cursor.execute(query)
            models.db.commit()
            return JsonResponse({'output':2})
        else:
            return redirect('http://localhost:8000/groceryAdmin/')

    def doneOrder(self,request):
        if 'adminId' in request.COOKIES:
            if request.method=="POST":
             orderId = request.POST.get('orderId')
            query = "update currentorders set orderStatus = '%d' where orderId = '%s' " %(3,orderId)
            models.cursor.execute(query)
            models.db.commit()
            return JsonResponse({'output':3})
        else:
            return redirect('http://localhost:8000/groceryAdmin/')


    def deliveryOrder(self,request):
        if 'adminId' in request.COOKIES:
            if request.method=="POST":
             sorderId = request.POST.get('orderId')

            query = "delete from currentorders where orderId = '%s' " %(orderId)
            models.cursor.execute(query)
            models.db.commit()

            query = "update orders set orderStatus = '%d' where orderId = '%s' " %(1,orderId)
            models.cursor.execute(query)
            models.db.commit()
            return JsonResponse({'output':1})
        else:
            return redirect('http://localhost:8000/groceryAdmin/')

    def deleteOrder(self,request):
        if 'adminId' in request.COOKIES:
            if request.method =="POST":
             orderId = request.POST.get('orderId')

            query = "delete from currentorders where orderId = '%s' " %(orderId)
            models.cursor.execute(query)
            models.db.commit()
            return JsonResponse({'output':1})
        else:
            return redirect('http://localhost:8000/groceryAdmin/')

       

def addCatagory(request):
    if 'adminId' in request.COOKIES:
        if 'adminId' in request.COOKIES:
            if request.method=='GET':
                return render(request,'addCatagory.html',{})
            else:
                catagoryName = request.POST.get('catagoryName')
            # catagoryImage = request.POST.get('catagoryImage')
            catagoryDesc = request.POST.get('catagoryDesc')
            catagoryImage=request.FILES['catagoryImage']
            catagoryid=''+catagoryName[:3]+catagoryName[-1:-4:-1]+str(sum(map(ord,catagoryName))%1000)
            fs=FileSystemStorage()
            filename=fs.save(catagoryImage.name,catagoryImage)
            query = "insert into catagory values('%s','%s','%s','%s')"%(catagoryid,catagoryName,filename,catagoryDesc)
            models.cursor.execute(query)
            models.db.commit()
            return render(request,'addCatagory.html',{'output':'Catagory added Successfully'})
    else:
        return redirect("http://localhost:8000/adminlogin")

def addVariety(request):
    if 'adminId' in request.COOKIES:
        query = "select * from catagory"
        models.cursor.execute(query)
        allCatagory = models.cursor.fetchall()
        if request.method=='GET':
           return render(request,'addVariety.html',{"catagory":allCatagory})
        else:
            varietyName = request.POST.get('VarietyName')
            catid = request.POST.get('catid')
            varietyDesc = request.POST.get('varietyDesc')
            varietyImage=request.FILES['varietyImage']
            varietyId =''+varietyName[:3] + varietyName[-1:-4:-1] + str(sum(map(ord, varietyName))%1000)
            fs=FileSystemStorage()
            filename=fs.save(varietyImage.name,varietyImage)
            query = "insert into variety (catid,varietyId,varietyName,varietyImg,varietyDesc) values('%s','%s','%s','%s','%s')"%(catid,varietyId,varietyName,filename,varietyDesc)
            models.cursor.execute(query)
            models.db.commit()
        return render(request,'addVariety.html',{"catagory":allCatagory,'output':'variety added Successfully'})
    else:
        return redirect("http://localhost:8000/adminlogin")

def addSubVariety(request):
    if 'adminId' in request.COOKIES:
        query = "select * from catagory"
        models.cursor.execute(query)
        allCatagory = models.cursor.fetchall()
        if request.method=='GET':
            return render(request,'addSubVariety.html',{"catagory":allCatagory})
        else:
            varietyId = request.POST.get('varietyId')
            itemName = request.POST.get('subVarietyName')
            itemprice = int(request.POST.get('subVarietyPrice'))
            itemDesc = request.POST.get('subVarietyDesc')
            itemid = '' + itemName[:3] + itemName[-1:-4:-1] + str(sum(map(ord, itemName)) % 1000)
            query = "insert into subvariety (itemId,varietyId,itemName,itemDescription,itemPrice,itemImg) values('%s','%s','%s','%s','%d','%s')"%(itemid,varietyId,itemName,itemDesc,itemprice,'')
            models.cursor.execute(query)
            models.db.commit()
    
            return render(request,'addSubVariety.html',{"catagory":allCatagory,'output':'variety added Successfully'})
    else:
        return redirect("http://localhost:8000/adminlogin")

# View to load Varieties using Ajax in AddSubVariety Template
def changeCatagory(request):
    if 'adminId' in request.COOKIES:
        catid = request.POST.get('catid')
        print(catid)
        query = "select varietyId,varietyName from variety where catid='%s'"%(catid)
        models.cursor.execute(query)
        varietyList = models.cursor.fetchall()
        print("Change : variety" ,varietyList)
        return JsonResponse({'varietyList':varietyList})
    else:    
        return redirect("http://localhost:8000/adminlogin")

def changeVariety(request):
    if 'adminId' in request.COOKIES:
        print("riunning")
        varietyId = request.POST.get('varietyId')
        print(varietyId)
        query = "select itemId,itemName from subvariety where varietyId='%s'"%(varietyId)
        models.cursor.execute(query)
        subvarietyList = models.cursor.fetchall()
        print("SubVAriety : ",subvarietyList)
        return JsonResponse({'subvarietyList':subvarietyList})
    else:    
        return redirect("http://localhost:8000/adminlogin")    

def deleteCatagory(request):
    if 'adminId' in request.COOKIES:
        query = "select * from catagory"
        models.cursor.execute(query)
        allCatagory = models.cursor.fetchall()
        if request.method == 'GET':
           return render(request, 'deleteCatagory.html', {"catagory":allCatagory})
        else:
           catid = request.POST.get('catid')
           query = "delete from catagory where catid = '%s' " % (catid)
           models.cursor.execute(query)
           models.db.commit()
        return render(request, 'deletecatagory.html', {"catagory": allCatagory, 'output': 'Delete Catagory Successfully'})
    else:
        return redirect("http://localhost:8000/adminlogin")


def deleteVariety(request):
    if 'adminId' in request.COOKIES:
        query = "select * from catagory"
        models.cursor.execute(query)
        allCatagory = models.cursor.fetchall()
        if request.method == 'GET':
           return render(request, 'deletevariety.html', {"catagory": allCatagory})
        else:
            catid = request.POST.get('catid')
            query = "delete from variety where catid = '%s' " % (catid)
            models.cursor.execute(query)
            models.db.commit()
            return render(request, 'deleteVariety.html',{"catagory": allCatagory, 'output': 'Delete Variety Successfully'})
    else:
            return redirect("http://localhost:8000/adminlogin")

        
def deleteSubVariety(request):
    if 'adminId' in request.COOKIES:

        query = "select * from catagory"
        models.cursor.execute(query)
        catagoryData = models.cursor.fetchall()
        if request.method == 'GET' :
            return render(request, 'deleteSubVariety.html', {"catagory": catagoryData})
        else:
            varietyId = request.POST.get('varietyId')
            query = "delete from subvariety where varietyId = '%s' " % (varietyId)
            models.cursor.execute(query)
            models.db.commit()
            return render(request, 'deleteSubVariety.html', {"catagory": catagoryData, 'output': 'Delete Variety Successfully'})
    else:
            return redirect("http://localhost:8000/adminlogin")

def allFeedbacks( request):
    if 'adminId' in request.COOKIES:

        query = "select user_Id, city, message from feedbacks"
        models.cursor.execute(query)
        allFeedbacks = models.cursor.fetchall()
        
        return render(request, 'allFeedbacks.html', {'feedbacks': allFeedbacks})
    else:
        return redirect("http://localhost:8000/adminlogin")

def adminLogout(request):
   if 'adminId' in request.COOKIES:
       response = redirect('http://localhost:8000/')
       response.delete_cookie('adminId')
       return response
   else:
       return redirect('http://localhost:8000/adminlogin')
