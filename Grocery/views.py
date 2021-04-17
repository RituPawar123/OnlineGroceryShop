from __future__ import unicode_literals
from django.shortcuts import render,redirect
from collections import defaultdict
from GroceryShop import settings
from django.http.response import JsonResponse
from django.core.mail import send_mail

from .import models
import random


from datetime import datetime

curl = settings.CURRENT_URL

def home(request):
    if 'email' in request.COOKIES :
        return redirect('http://localhost:8000/groceryUser/')
    elif 'adminId' in request.COOKIES:
        return redirect('http://localhost:8000/groceryAdmin/')
    else:
        query = "select catimg , catnm, catdesc ,catid from catagory"
        models.cursor.execute(query)
        catagories = list(models.cursor.fetchall())
        for i in range(len(catagories)):
            query = "select varietyName ,varietyImg,varietyId from variety where catId = '%s'"%(catagories[i][3])
            models.cursor.execute(query)
            catagories[i] = list(catagories[i])
            catagories[i].append(models.cursor.fetchall())
        return render(request, 'home.html',{'catagories': catagories})

def about(request):
    if 'email' in request.COOKIES :
        return redirect('http://localhost:8000/groceryUser/about')
    else:
        return render(request, 'about.html')

def contact(request):
    if 'email' in request.COOKIES :
        return redirect('http://localhost:8000/groceryUser/contact')
    else:
        if request.method=="GET":
           return render(request, 'contact.html')
        else:
            name = request.POST.get('name')
            email = request.POST.get('email')
            mobile = requeest.POST.get('mobile')
            message = request.POST.get('message')
            subject="contact details"
            msg =""" name: """ +str(name)+""" email: """ +str(email)+"""mobile: """ +int(mobile)+"""message: """+str(message)
            to = ['pawarritu1998@gmail.com','akankshaingle786@gmail.com']
            send_mail(subject,msg, settings.EMAIL_HOST_USER, to)
            return redirect(request, 'contact.html', {output:1})

def feedback(request):
    if request.method=='GET':
        return render(request,'feedback.html',{})
    else:
        userId=request.POST.get('user_Id')
        city=request.POST.get('city')
        feedbackMsg=request.POST.get('message')
        print(userId,city,feedbackMsg)
        query="insert into feedbacks values('%s','%s','%s')"%(userId,city,feedbackMsg)

        models.cursor.execute(query)
        models.db.commit()
        # return redirect('http://localhost:8000/')
        return render(request,'feedback.html',{})

#user feedback


def login(request):
    if request.method=="GET":
        return render(request, 'login.html')
    else:
        email = request.POST.get('uname')
        password = request.POST.get('psw')
        print("email,psw",email,password)
        query = "select userId from customers where email ='%s' and password = '%s' "%(email,password)
        models.cursor.execute(query)
        userID =  models.cursor.fetchall()
        print("UserID  ",userID)
        if userID:
            response = redirect('http://localhost:8000/groceryUser/')
            response.set_cookie('email',email)
            print("Login Done")
            return response 
        else:
            print("Login generate Error")
            return render(request,'register.html',{'output':'User Not Exist'})

def adminLogin(request):
    if request.method=="GET":
        return render(request, 'adminlogin.html', {'output':1})
    else:
        uname = request.POST.get('uname')
        psw = request.POST.get('psw')
        query = "select * from admins where adminEmail ='%s' and adminPassword = '%s' "%(uname,psw)
        models.cursor.execute(query)
        adminExist =  models.cursor.fetchall()
        if adminExist :
            response = redirect('http://localhost:8000/groceryAdmin/')
            response.set_cookie('adminId',adminExist[0][0])
            return response
        else:
            print("Login generate Error")
            return render(request,'adminLogin.html',{'output':0})

def sendOtp(email,subject):
    try:
        otp = random.randint(1000, 9999)
        msg = """ Please use this Otp for register in Grocery\nOTP : """ \
            + str(otp) + """\n Don't shear this Otp with anyone"""
        to = email
        send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
        return otp
    except:
        return  0

class Register:
    def __init__(self):
        self.user = dict()
    def register(self,request):
        if request.method=="GET":
            return render(request, 'register.html',{})
        else:
            now = datetime.now()
            self.user['registerTime'] = now.strftime("%d/%m/%Y %H:%M:%S")
            self.user['name'] = request.POST.get("name")
            self.user['email'] = self.email = username = request.POST.get("uname")
            self.user['password'] = request.POST.get("psw")
            self.user['city'] = request.POST.get("city")
            self.user['contact_no'] = request.POST.get("contact_no")
            self.user['address'] = request.POST.get("address")
            self.user['userId'] = username.split('@')[0]
            self.otp = sendOtp(self.email,"Mail for Registration")
            if self.otp :
                response=redirect('http://localhost:8000/checkOtp/')
                response.set_cookie("email",self.email)
                return response
            else:
                return render(request, 'register.html',{})

    # def adminRegister(self, request):
    #     if request.method == "GET":
    #         return render(request, 'adminRegister.html', {})
    #     else:
    #         now = datetime.now()
    #         self.user['name'] = request.POST.get("name")
    #         self.user['email'] = self.email = username = request.POST.get("uname")
    #         self.user['password'] = request.POST.get("psw")
    #
    #         self.user['contact_no'] = request.POST.get("contact_no")
    #         self.user['address'] = request.POST.get("address")
    #         self.user['userId'] = username.split('@')[0]
    #
    #         self.otp = sendOtp(self.email, "Mail for Registration")
    #
    #         if self.otp:
    #             response = redirect('http://localhost:8000/checkOtp/')
    #             response.set_cookie("email", self.email)
    #             return response
    #         else:
    #             return render(request, 'adminRegister.html', {})

    def resendOtp(self,request):
        email = request.POST.get('email')
        print("REder mm : ",email)
        self.otp = sendOtp(email,"Mail for Registration OTP resent")
        print(self.otp)
        otpStatus = 0
        if self.otp:
            otpStatus = 1
        return JsonResponse({'otp':otpStatus})

    def checkOtp(self,request):
        if request.method=="GET":
            return render(request,'checkOtp.html',{'email':request.COOKIES['email']})
        else:
            userOtp =  request.POST.get('userOtp')
            if int(userOtp)!=self.otp:
                return render(request,'checkOtp.html',{'email':request.COOKIES['email']})
            else:
                query = "insert into customers (userId,name,email,mobile,city, password,address,status,registerDate) values('%s','%s','%s','%s','%s','%s','%s','%d','%s')"%(self.user['userId'],self.user['name'],self.user['email'],self.user['contact_no'],self.user['city'],self.user['password'],self.user['address'],1,self.user['registerTime'])
                models.cursor.execute(query)
                models.db.commit()
                return redirect('http://localhost:8000/login/')            
    def alreadyReg(self,request):
        username = request.POST.get('username')
        query = "select * from customers where email = '%s' "%(username)
        models.cursor.execute(query)
        userData = models.cursor.fetchall()
        if userData :
            return JsonResponse({'isRegistered':1})
        else:
            return JsonResponse({'isRegistered':0})
    # ................................
    # ................................
def temp(request):
    otp = sendOtp('akaushal451@gmail.com',"For temporary Use")
    print("OTP : ",otp)
    return render(request,'temp.html',{'otp':otp})

def product(request):
    # query= 'select * from catagory'
    # models.cursor.execute(query)
    # item=models.cursor.fetchall()
    # print(item)
    # queryForCatagory = "select * from catagory"
    # models.cursor.execute(queryForCatagory)
    # catagoryData = models.cursor.fetchall()

    # queryForItems = "select * from subvariety"
    # models.cursor.execute(queryForItems)
    # varietyData = [list(i) for i in models.cursor.fetchall()]
    # varietyData = list(varietyData)
    # globalData = [
    # ]
    # tempDict= defaultdict(list)
    # print(varietyData)
    # for i in varietyData:
    #     try:
    #         if tempDict[i[1]]:
    #             temp = list(i)
    #             temp[5] ='image/'+temp[5]
    #             tempDict[i[1]].append(temp)
    #     except:
    #         temp = list(i)
    #         temp[5] ='image/'+temp[5]
    #         tempDict[i[1]] = [temp,]
    # for i in range(len(catagoryData)):
    #     globalData.append([catagoryData[i][1],'image/'+catagoryData[i][2],catagoryData[i][3],tempDict[catagoryData[i][0]]])
    # print("Product Page")

    varietyId = request.GET.get('varietyId')
    print("VAriety : ",varietyId)
    query = 'select * from subvariety'
    if varietyId:
        query = "select * from subvariety where varietyId = '%s'"%(varietyId)
    models.cursor.execute(query)
    subvarietyData = models.cursor.fetchall()
    print(subvarietyData)
    return render(request, 'product.html', {'items': subvarietyData})
    # return render(request, 'product.html',{'items':varietyData})
    # return render('',{'catagories':globalData})




