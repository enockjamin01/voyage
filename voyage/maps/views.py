from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
import re
from firebase_admin import auth,db
import json

# Create your views here.
class Home(View):

    def get(self,request):
        if "uid" in request.session and len(request.session['uid']) != 0:
                try:
                    db_ref=db.reference("/users")
                    db_child=db_ref.child(request.session['uid'])
                    db_child_trips=db_child.child("trips")
                    if(db_child_trips.get() == None):
                        name=db_child.get()['name']
                        return render(request,'maps/index.html',{
                        "name":name,
                        "trips":None
                    })
                    else:
                        name=db_child.get()['name']
                        trips=db_child.get()['trips']
                        print(type(trips[0]))
                        return render(request,'maps/index.html',{
                            "name":name,
                            "trips":trips
                        })
                except Exception:
                    print("Failed to fetch data")
                    request.session['uid']=""
                    return HttpResponseRedirect('/login')
        else:
            request.session['uid']=""
            return HttpResponseRedirect('/login')
        
    def post(self,request):
        trip_name=request.POST['tripname']
        coordinates=json.loads(request.POST['coordinates'])
        new_trip={"name":trip_name,"coordinates":coordinates}
        db_ref=db.reference("/users")
        db_child=db_ref.child(request.session['uid'])
        db_child_trip=db_child.child("trips")
        if(db_child_trip.get() == None):
            db_child_trip.set([new_trip])
        else:
            existing_trip=db_child_trip.get()
            trips=[]
            for trip in existing_trip:
                trips.append(trip)
            trips.append(new_trip)
            db_child_trip.set(trips)
        return HttpResponseRedirect('/')


class SignUp(View):

    def get(self,request):
            if "uid" not in request.session or len(request.session['uid']) == 0:
                return render(request,'maps/signup.html')
            else:
               return HttpResponseRedirect('/')

    def post(self,request):
        email_pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        request.session['uid']=""
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        if len(name) >= 5 and len(email) >= 7 and len(password) >= 8:
            if re.match(email_pattern,email):
                try:
                    user=auth.get_user_by_email(email)
                    print("User with this email already exist with ID: ",user.uid," (Email: ",email,")")
                    return HttpResponseRedirect("/signup")
                except Exception:
                    try:
                        user=auth.create_user(
                            email=email,
                            password=password,
                            display_name=name
                        )
                        request.session['uid']=user.uid
                        db_ref=db.reference("/users")
                        db_child=db_ref.child(user.uid)
                        user_data={
                                "name":name,
                                "email":email,
                                "password":password,
                                "uid":user.uid,
                                "trips":[]
                            }
                        db_child.set(user_data)
                        return HttpResponseRedirect("/")
                    except Exception:
                        print("Error while creating user")
                        return HttpResponseRedirect("/signup")
            else:
                print("Invalid Email")
                return HttpResponseRedirect("/signup")
        else:
            print("Invalid Data")
            return HttpResponseRedirect("/signup")

class LogIn(View):
    def get(self,request):
        if "uid" not in request.session or len(request.session['uid']) == 0:
            return render(request,'maps/login.html')
        else:
            return HttpResponseRedirect('/')

    def post(self,request):
        email_pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        request.session['uid']=""
        email=request.POST['email']
        password=request.POST['password']
        if len(email) >= 7 and len(password) >= 8:
            if re.match(email_pattern,email):
                try:
                    user=auth.get_user_by_email(email)
                    request.session['uid']=user.uid
                    return HttpResponseRedirect("/")
                except Exception:
                    print("Error while logging in")
                    return HttpResponseRedirect("/login")
            else:
                print("Invalid Email")
                return HttpResponseRedirect("/login")
        else:
            print("Invalid Data")
            return HttpResponseRedirect("/login")

class Logout(View):
    def get(self,request):
        if "uid" in request.session and len(request.session['uid']) != 0:
            del request.session['uid']
            request.session.modified=True
            return render(request,"maps/logout.html")
        else:
            return HttpResponseRedirect("/signup")
