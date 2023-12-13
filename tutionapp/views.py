from django.shortcuts import render,redirect
from django.contrib.auth import  authenticate, login as a_login
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import CustomUser,teacher,student,course,departmenttable,assigntable,passtable,assignment,assignmenttable,notification
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from .models import attendancetable,teacherattendancetable,attendancereport,teachernotification
from .models import CustomUser, notification, teacher, passtable
import random, datetime, os
from datetime import datetime
from django.urls import reverse


@login_required(login_url='login1')
def adminhome(request):
    notifications = notification.objects.filter(status=1)
    notification_count = notifications.count()
    
    context = {
        'notifications': notifications,
        'notification_count': notification_count,
    }
    return render(request, 'adminhome.html', context)

@login_required(login_url='login1')
def studenthome(request):
    return render(request,'studenthome.html')
@login_required(login_url='login1')
def teacherhome(request):
    current=request.user.id
    data=teachernotification.objects.all()
    c=0
    for i in data:
        if i.userid.id == current:
            c=c+1
    return render(request,'teacherhome.html',{'data':data,'co':c,'current':current})
@login_required(login_url='login1')
def addcourse(request):
    notifications = notification.objects.filter(status=1)
    notification_count = notifications.count()
    
    context = {
        'notifications': notifications,
        'notification_count': notification_count,
    }
    return render(request,'addcourse.html',context)
@login_required(login_url='login1')
def doaddcourse(request):
    if request.method == 'POST':
        coursename = request.POST['course']
        coursefee = request.POST['fee']
        syllabus = request.POST['syllabus']  # Retrieve syllabus data from textarea
        dura = request.POST['START_DATE']
        data_exists = course.objects.filter(course_name=coursename).exists()
        if data_exists:
            messages.info(request, 'Course already exists')
            return redirect('addcourse')
        
        data = course(course_name=coursename, Course_fee=coursefee, syllabus=syllabus, course_duration=dura)
        data.save()
        return redirect('adminhome')

@login_required(login_url='login1')
def department(request):
    notifications = notification.objects.filter(status=1)
    notification_count = notifications.count()
    
    context = {
        'notifications': notifications,
        'notification_count': notification_count,
    }
    return render(request,'department.html',context)

def sregistration(request):
    return render(request,'sregistration.html')

def login1(request):
    return render(request,'login.html')

def doRegistration(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email_id = request.POST['email']
        age = request.POST['age']
        contact = request.POST['contact']
        image = request.FILES.get('image')
        password = str(random.randint(100000, 999999))

        if not (email_id and age and image and first_name and last_name):
            messages.info(request, 'Please provide all the details.')
            return redirect('sregistration')

        is_user_exists = CustomUser.objects.filter(email=email_id).exists()
        if is_user_exists:
            messages.info(request, 'This email id already exists.')
            return redirect('sregistration')

        user_type = request.POST['text']
       
        user_name = first_name 
        user = CustomUser()
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.username = user_name
        user.user_type = user_type
        user.email = email_id
        user.save()

        data = notification()
        data.name = first_name
        data.age = age
        data.email = email_id
        data.usertype = user_type
        data.userid = user
        data.image = image
        data.save()

        if user_type == '3':
            user3 = student()
            user3.firstname = first_name
            user3.lastname = last_name
            user3.username = user_name
            user3.email = email_id
            user3.age = age
            user3.contact = contact
            user3.image = image
            user3.user = user
            user3.save()

            userpass = passtable()
            userpass.password = password
            userpass.userid = user
            userpass.save()

 
        subject = 'Registration Confirmation'
        message = f'Hello {first_name},\n\n' \
                  f'You have been registered for tuition. Please wait for admin approval.\n\n' \
                  f'Thank you for choosing our tuition platform!'
        from_email = settings.EMAIL_HOST_USER  # Use the configured email from settings
        recipient_list = [email_id]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        messages.info(request, 'Registration successful. Please wait for admin approval.')
        return redirect('sregistration')

    return render(request, 'sregistration.html')

def doLogin(request):
    user_name=request.GET.get('username')
    
    password1=request.GET.get('password')
    if not ( password1):
        messages.info(request,'Required fields must be filled in.')
        return redirect('login1')
    user=auth.authenticate(username=user_name, password=password1)
    if not user:
        messages.info(request,'Login failed. Please check your username and password and try again.')
        return redirect('login1')
    a_login(request,user)
    if user.user_type == CustomUser.STUDENT:
        messages.info(request,f'welcome, '+str(user_name))
        return redirect('studenthome')
    elif user.user_type == CustomUser.STAFF:
        messages.info(request,f'welcome, '+str(user_name))
        return redirect('teacherhome')
    elif user.user_type == CustomUser.HOD:
        messages.info(request,'welcome, '+str(user_name))
        return redirect('adminhome')
    return redirect('login1')
@login_required(login_url='login1')
def managecourse(request):
    data=course.objects.all()
    return render(request,'managecourse.html',{'key':data}) 
def adddepartment(request):
    if request.method =='POST':
        dep=request.POST['dep']
        data=departmenttable(department=dep)
        data.save()
        messages.info(request,'New Department added')
        return redirect('department')



@login_required(login_url='login1')
def tableassign(request):
    data=assigntable.objects.all()
    return render(request,'assigntable.html',{'key':data})
@login_required(login_url='login1')
def studentprofile(request):
    current=request.user.id
    data=student.objects.get(user_id=current)
    return render(request,'studentprofile.html',{'data':data})



@login_required(login_url='login1')
def teacherprofile(request):
    current=request.user.id
    data1=teacher.objects.get(user=current)
    return render(request,'teacherprofile.html',{'data':data1})

@login_required(login_url='login1')
def adminstudentattendance(request):
    value=course.objects.all()
    return render(request,'adminstudentattendance.html',{'data':value})
@login_required(login_url='login1')
def adminstudentatendancedata(requsest):
    if requsest.method =='POST':
        value=requsest.POST['course']
        date=requsest.POST['date']
        data=attendancereport.objects.filter(courseid=value,date=date)
        return render(requsest,'adminviewstudentattendance.html',{'data':data})
    return redirect('adminstudentattendance') 

@login_required(login_url='login1') 
def studentatendance(request):
    current=request.user.id
    teacherdata=teacher.objects.get(user=current)
    value=student.objects.filter(courseid=teacherdata.courseid)
    return render(request,'studentatendance.html',{'data':value})
@login_required(login_url='login1')
def studentatendancedata(request):
    if request.method =='POST':
        value=request.POST['course']
        value1=course.objects.get(id=value)
        data=attendancetable.objects.all()
        return render(request,'attendancetable.html',{'data':data,'data2':value1})
    return redirect('studentatendance')


def present(request):
    if request.method =='POST':
        a=request.POST['username']
        b=request.POST['date']
        c=request.POST['attendance']
        user=CustomUser.objects.get(id=a)
        if a =='' and b =='' and c =='':
            messages.info(request,'fill all the fileds')
            return redirect('studentatendancedata')
        try:
            if attendancereport.objects.get(userid=user,date=b):
                messages.info(request,'ATTENDANCE ALREADY TAKEN FOR THE student FOR THE SAME DATE')
                return redirect('studentatendancedata')
        except:
           
            studentdata=student.objects.get(user=user)
            cid=studentdata.courseid.id
            coursedata=course.objects.get(id=cid)
            data=attendancereport(userid=user,date=b,status=c,courseid=coursedata)
            data.save()
            messages.info(request,'ATTENDANCE MARKED')
            return redirect('studentatendancedata')
    return redirect('studentatendancedata')

@login_required(login_url='login1')
def teacherviewstudentatten(request):
    if request.method == 'POST':
        current=request.user.id
        date=request.POST['date']
        stdata=teacher.objects.get(user=current)
        courseid=stdata.courseid.id
        data=attendancereport.objects.filter(courseid=courseid,date=date)
        return render(request,'teacherpageforstatten.html',{'data':data})



    

@login_required(login_url='login1')
def teachertableassign(request):
    return render(request,'teacherassigntable.html')
  

@login_required(login_url='login1')
def assignmentst(request):
    current_user = request.user  
    if current_user.user_type == CustomUser.STAFF: 
        teacher_courses = course.objects.filter(teacher__user=current_user)

        return render(request, 'assignment.html', {'teacher_courses': teacher_courses})
    else:

        pass
def doassignment(request):
    if request.method=='POST':
        a=request.POST['assignment']
        b=request.POST['sdate']
        c=request.POST['edate']
        d=request.POST['course']
        co=course.objects.get(id=d)
        current=request.user.id
        user=CustomUser.objects.get(id=current)
        data=assignment()
        data.userid=user
        data.assignment_name=a
        data.start_date=b
        data.end_date=c
        data.courseid=co
        data.save()
        messages.info(request,'New Assignment added')
        return redirect('assignmentst')   


@login_required(login_url='login1')       
def studentpage(request):
    current = request.user.id
    user = student.objects.get(user=current)
    data1 = assignment.objects.filter(courseid=user.courseid)
    if data1.exists():
        return render(request, 'studentpageassignment.html', {'data': data1})
    else:
        messages.error(request, "No assignment available.")
        return redirect('studenthome')
    
    
@login_required(login_url='login1')
def teacherdetails(request):
    data=teacher.objects.all()
    return render(request,'teacherdetails.html',{'data':data})    
@login_required(login_url='login1')
def teacherdetails1(request):
    data=teacher.objects.all()
    return render(request,'teacherdetails1.html',{'data':data}) 
def delteacher(request,pk):
    data1=teacher.objects.get(user=pk)
    data1.delete()
    data=CustomUser.objects.get(id=pk)
    data.delete()
    return redirect('teacherdetails')
def delstudent(request,pk):
    data=student.objects.get(user=pk)
    data.delete()
    data1=CustomUser.objects.get(id=pk)
    data1.delete()
    return redirect('studentdetails')
    
@login_required(login_url='login1')
def logout(request):
    auth.logout(request)
    return redirect('login1')
@login_required(login_url='login1')
def studentdetails(request):
    data=student.objects.all()
    return render(request,'studentdetails.html',{'data':data})
@login_required(login_url='login1')
def studentdetails1(request):
    data=student.objects.all()
    return render(request,'studentdetails1.html',{'data':data})
def viewuser(request):
    data=notification.objects.all()
    return render(request,'approve.html',{'data':data})

def approve(request,pk):
    data=notification.objects.get(userid=pk)
    
    if data.usertype == 2:
        data.status='2'
        data.save()
        password=passtable.objects.get(userid=pk)
        userdata=teacher.objects.get(user=pk)
        userpassword=password.password
        username=userdata.username
        email=userdata.email
        atn=teacherattendancetable()
        atn.userid=CustomUser.objects.get(id=pk)
        atn.date=datetime.now()
        atn.save()
        subject="ADMIN APPROVED"
        message="username: "+str(username)+"\n"+"password: "+str(userpassword)+"\n"+"email: "+str(email)
        send_mail(subject,message,settings.EMAIL_HOST_USER,[data.email])
        messages.info(request,'USER APPROVED')   
        return redirect('viewuser')
    if data.usertype == 3:
        data.status='2'
        data.save()
        password=passtable.objects.get(userid=pk)
        userdata=student.objects.get(user=pk)
        userpassword=password.password
        username=userdata.username
        email=userdata.email
        subject="ADMIN APPROVED"
        message="username: "+str(username)+"\n"+"password: "+str(userpassword)+"\n"+"email: "+str(email)
        send_mail(subject,message,settings.EMAIL_HOST_USER,[data.email])
        messages.info(request,'USER APPROVED')   
        return redirect('viewuser')
    return redirect('viewuser')  
def disapprove(request,pk):
    data=notification.objects.get(userid=pk)
    if data.usertype == 2:
        data.status='0'
        data.save()
        userdata=teacher.objects.get(user=pk)
        userdata.delete()
        password=passtable.objects.get(userid=pk)
        password.delete()
        user=notification.objects.get(userid=pk)
        user.delete()
        user1=CustomUser.objects.get(id=pk)
        user1.delete()
        messages.info(request,'User Disapproved')   
        return redirect('viewuser')
    if data.usertype == 3:
        data.status='0'
        data.save()
        userdata=student.objects.get(user=pk)    
        userdata.delete()
        password=passtable.objects.get(userid=pk)
        password.delete()
        user=notification.objects.get(userid=pk)
        user.delete()
        user1=CustomUser.objects.get(id=pk)
        user1.delete
        messages.info(request,'User Disapproved')   
        return redirect('viewuser')
    return redirect('viewuser')


def stattendanceview(request):
    Current=request.user.id
    data=attendancereport.objects.all()
    return render(request,'stviewattendance.html',{'data':data,'current':Current})
def teacherattendanceview(request):
    data=teacherattendancetable.objects.all()
    return render(request,'teacherattendance.html',{'data':data})
def teviewattendance(request):
    current=request.user.id
    data=attendancereport.objects.all()
    return render(request,'teviewattendance.html',{'data':data,'current':current})




def present1(request):
    if request.method =='POST':
        a=request.POST['username']
        b=request.POST['date']
        c=request.POST['attendance']
        user=CustomUser.objects.get(id=a)
        try:
            if attendancereport.objects.get(userid=a,date=b):
                messages.info(request,'ATTENDANCE ALREADY TAKEN FOR THE TEACHER FOR THE SAME DATE')
                return redirect('teacherattendanceview')
        except:
           
            data=attendancereport(userid=user,date=b,status=c)
            data.save()
            messages.info(request,'ATTENDANCE MARKED')
            return redirect('teacherattendanceview')
    return redirect('teacherattendanceview')
def absent1(request,pk):
    data=teacherattendancetable.objects.get(id=pk)
    data.date=datetime.datetime.now()
    data.attendance=0
    data.save()
    user=data.userid.id
    user1=CustomUser.objects.get(id=user)
    x=datetime.datetime.now()
    data2=attendancereport(userid=user1,status=data.attendance,date=x)
    data2.save()
    return redirect('teacherattendanceview')

def pushassignment(request, pk):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file') 
        current=request.user.id
        asii=assignment.objects.get(id=pk)
        user=CustomUser.objects.get(id=current)
        course1=student.objects.get(user=user)
        date=datetime.now()
        data=assignmenttable()
        data.userid=user
        data.submit_date=date
        data.username=user.username
        data.assignment_name=asii.assignment_name
        data.pdf_file=pdf_file
        data.courseid=course1.courseid
        data.save()
        return redirect('studentpage')


def viewassignment(request):
    data=assignmenttable.objects.all()
    return render(request,'viewassignment.html',{'data':data}) 
def editteacher(request):
    current=request.user.id
    data=CustomUser.objects.get(id=current)
    data2=teacher.objects.get(user=data)
    return render(request,'editteacher.html',{'data':data,'data2':data2}) 
def editstudent(request):
    current=request.user.id
    data=CustomUser.objects.get(id=current)
    data2=student.objects.get(user=data)
    return render(request,'editstudent.html',{'data':data,'data2':data2}) 
def studentupdate(request):
    if request.method == 'POST':
        pk=request.user.id
        username=request.POST['username']
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        email_id=request.POST['email']
        age=request.POST['age']
        contact=request.POST['contact']
        image = request.FILES.get('image')

        data=CustomUser.objects.get(id=pk)
        data.first_name = first_name
        data.last_name = last_name
        data.email = email_id
        data.username = username
        data.save()
        udata = student.objects.get(user=data)
        udata.firstname = first_name
        udata.lastname = last_name
        udata.email = email_id
        udata.age = age
        udata.contact = contact
        udata.username = username

        if image:
            if udata.image:
                udata.image.delete()
            udata.image = image

        udata.save()
        return redirect('studentprofile')
    return redirect('studentprofile')         
def teacherupdate(request):
      if request.method == 'POST':
        pk=request.user.id
        username=request.POST['username']
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        email_id=request.POST['email']
        age=request.POST['age']
        contact=request.POST['contact']
        image = request.FILES.get('image')
        data=CustomUser.objects.get(id=pk)
        data.first_name=first_name
        data.last_name=last_name
        data.email=email_id
        data.username=username
        data.save()
        udata = teacher.objects.get(user=data)
        udata.firstname = first_name
        udata.lastname = last_name
        udata.email = email_id
        udata.username = username
        udata.age = age
        udata.contact = contact
        if image:
            if udata.image:
                udata.image.delete()
            udata.image = image

        udata.save()
        return redirect('teacherprofile')
    
    
def resetpassword(request):
    return render(request,'passwordreset.html')
def resetpassword1(request):
    return render(request,'passwordreset1.html')

def dogeneration(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        new_password = request.POST['new_password'] 
        data = CustomUser.objects.get(username=username, email=email)
        if data.user_type == '2':
            data.set_password(new_password)
            data.save()
            subject = "PASSWORD RESET"
            message = "Your password has been reset."
            message = f"Username: {username}\nNew Password: {new_password}\nEmail: {email}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [data.email])
            return redirect('resetpassword')
        elif data.user_type == '3':
            data.set_password(new_password)
            data.save()
            subject = "PASSWORD RESET"
            message = "Your password has been reset."
            message = f"Username: {username}\nNew Password: {new_password}\nEmail: {email}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [data.email])
            return redirect('login1')

    return redirect('resetpassword1')

           
from django.contrib.auth.hashers import make_password

def dogeneration1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        try:
            data = CustomUser.objects.get(username=username, email=email)
            data.set_password(new_password)
            data.save()
            subject = "PASSWORD RESET SUCCESSFUL"
            message = f"Username: {username}\nNew Password: {new_password}\nEmail: {email}"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [data.email])
            messages.info(request, 'Password reset was successful. You can now login with your new password.')
            return redirect('login1')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User with provided username and email does not exist.')
    return redirect('resetpassword1')
            


def tregistration(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email_id = request.POST['email']
        age = request.POST['age']
        contact = request.POST['contact']
        image = request.FILES.get('image')
        password = str(random.randint(100000, 999999))

        if not (email_id and age and image and first_name and last_name):
            messages.info(request, 'Please provide all the details.')
            return redirect('sregistration')

        is_user_exists = CustomUser.objects.filter(email=email_id).exists()
        if is_user_exists:
            messages.info(request, 'This email id already exists.')
            return redirect('tregistration')

        user_type = request.POST.get('text')
       
        user_name = first_name 
        user = CustomUser()
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.username = user_name
        user.user_type = user_type
        user.email = email_id
        user.save()

        data = notification()
        data.name = first_name
        data.age = age
        data.email = email_id
        data.usertype = user_type
        data.userid = user
        data.image = image
        data.save()

        if user_type == '2':
            user2 = teacher()
            user2.firstname = first_name
            user2.lastname = last_name
            user2.username = user_name
            user2.email = email_id
            user2.age = age
            user2.contact = contact
            user2.image = image
            user2.user = user
            user2.save()

            userpass2 = passtable()
            userpass2.password = password
            userpass2.userid = user
            userpass2.save()

        # Send a registration email to the registered teacher or student
        subject = 'Registration Confirmation'
        message = f'Hello {first_name},\n\n' \
                  f'You have been registered for tuition. Please wait for admin approval.\n\n' \
                  f'Thank you for choosing our tuition platform!'
        from_email = settings.EMAIL_HOST_USER  # Use the configured email from settings
        recipient_list = [email_id]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        messages.info(request, 'Registration successful. Please wait for admin approval.')
        return redirect('tregistration')

    return render(request, 'tregistration.html')


def edit_course(request, course_id):
    course_obj = course.objects.get(id=course_id)

    if request.method == 'POST':
        course_obj.course_name = request.POST['course']
        course_obj.Course_fee = request.POST['fee']
        course_obj.course_duration = request.POST['duration']

        syllabus = request.POST.get('syllabus')
        if syllabus:
            course_obj.syllabus = syllabus

        course_obj.save()
        return redirect('managecourse')

    return render(request, 'edit_course.html', {'course': course_obj})


def delete_course(request,course_id):
    data1=course.objects.get(id=course_id)
    data1.delete()

    return redirect('managecourse')


# def notification_list(request):
#     notifications = notification.objects.filter(status=1)  
#     return render(request, 'notification_list.html', {'notifications': notifications})


def notification_list(request):
    notifications = notification.objects.filter(status=1)
    notification_count = notifications.count()
    
    context = {
        'notifications': notifications,
        'notification_count': notification_count,
    }
    return render(request, 'notification_list.html', context)


def approve_notification(request, pk):
    notification_instance = notification.objects.get(pk=pk)
    notification_instance.status = 2  # Approved status
    notification_instance.save()
    return redirect('notification_list')

def disapprove_notification(request, pk):
    notification_instance = notification.objects.get(pk=pk)
    notification_instance.status = 0  # Disapproved status
    notification_instance.save()
    return redirect('notification_list')

@login_required(login_url='login1')
def student_course(request):
    current_user = request.user  # Get the logged-in user

    if current_user.user_type == CustomUser.STUDENT:  # Assuming 'STUDENT' is the user type for students
        # Retrieve the course details for the logged-in student
        student_details = student.objects.get(user=current_user)  # Get the student's details
        student_course = student_details.courseid  # Get the course assigned to the student

        return render(request, 'student_course.html', {'student_course': student_course})
    else:
        # Handle the case when the logged-in user is not a student
        # You can redirect or show an error message
        pass
@login_required(login_url='login1')
def teacher_course(request):
    current_user = request.user  # Get the logged-in user

    if current_user.user_type == CustomUser.STAFF:  # Assuming 'STUDENT' is the user type for students
        # Retrieve the course details for the logged-in student
        teacher_details = teacher.objects.get(user=current_user)  # Get the student's details
        teacher_course = teacher_details.courseid  # Get the course assigned to the student

        return render(request, 'teacher_course.html', {'teacher_course': teacher_course})
    else:
        # Handle the case when the logged-in user is not a student
        # You can redirect or show an error message
        pass


def course_details(request, course_id):
    selected_course = course.objects.get(id=course_id)
    
    # Retrieve the teachers and students for the selected course
    teachers = teacher.objects.filter(courseid=selected_course)
    students = student.objects.filter(courseid=selected_course)
    
    return render(request, 'course_details.html', {'selected_course': selected_course, 'teachers': teachers, 'students': students})

def course_details1(request, course_id):
    selected_course = course.objects.get(id=course_id)
    students = student.objects.filter(courseid=selected_course)
    
    return render(request, 'course_details1.html', {'selected_course': selected_course,  'students': students})



@login_required(login_url='login1')
def assign_teacher(request):
    c = course.objects.all()
    d = departmenttable.objects.all()

    t = teacher.objects.all()
    
    return render(request, 'assign_teacher.html', {'course': c, 'dep': d,  'teacher': t})

@login_required(login_url='login1')
def assign_student(request):
    c = course.objects.all()
    d = departmenttable.objects.all()

    st = student.objects.all()
    
    return render(request, 'assign_student.html', {'course': c, 'dep': d, 'student': st})



@login_required(login_url='login1')
def add_assign_teacher(request):
    if request.method =='POST':
        dep=request.POST['department']
        co=request.POST['course']
        tea=request.POST['teacher']
       
        dep1=departmenttable.objects.get(id=dep)
        co1=course.objects.get(id=co)
        tea1=teacher.objects.get(id=tea)
        user=tea1.user.id
        try:
            data=assigntable.objects.get(teacherid=tea1)
            if data:
                messages.info(request,'course already assigned')
                return redirect('assign')
        except:
            data=assigntable(departmentid=dep1,courseid=co1,teacherid=tea1)
            data.save()
            data3=teacher.objects.get(id=tea)
            data3.departmentid=departmenttable.objects.get(id=dep)
            data3.courseid=co1
            data3.save()
            data4=teachernotification()
            data4.userid=CustomUser.objects.get(id=user)
            y=co1.course_name  + 'course assigned for you'
            data4.messge=y
            data4.save()
            
    return redirect('adminhome')


def add_assign_student(request):
    if request.method == 'POST':
        dep = request.POST['department']

        co = request.POST['course']
        stu = request.POST['student'] 
        
        dep1 = departmenttable.objects.get(id=dep)

        co1 = course.objects.get(id=co)
        stu1 = student.objects.get(id=stu)
        userid = stu1.user.id
        user = CustomUser.objects.get(id=userid)
        
        data = assigntable(departmentid=dep1, courseid=co1, studentid=stu1)
        data.save()
        
        data2 = student.objects.get(id=stu)
        data2.courseid = course.objects.get(id=co)
        data2.save()
        
        data4 = attendancetable()
        data4.userid = user
        data4.courseid = co1
        data4.save()
        
        # Add the necessary logic for student assignment here
        
        return redirect('adminhome')

@login_required(login_url='login1')
def adminstudentattendance(request):
    value=course.objects.all()
    return render(request,'adminstudentattendance.html',{'data':value})
@login_required(login_url='login1')
def adminstudentatendancedata(requsest):
    if requsest.method =='POST':
        value=requsest.POST['course']
        date=requsest.POST['date']
        data=attendancereport.objects.filter(courseid=value,date=date)
        return render(requsest,'adminviewstudentattendance.html',{'data':data})
    return redirect('adminstudentattendance') 

    
@login_required(login_url='login1')
def teacherviewstudentatten(request):
    if request.method == 'POST':
        current=request.user.id
        date=request.POST['date']
        stdata=teacher.objects.get(user=current)
        courseid=stdata.courseid.id
        data=attendancereport.objects.filter(courseid=courseid,date=date)
        return render(request,'teacherpageforstatten.html',{'data':data})
    

@login_required(login_url='login1')
def teachertableassign(request):
    return render(request,'teacherassigntable.html')


def viewnotification(request):
    current_user = request.user
    notifications = teachernotification.objects.filter(userid=current_user)

    if notifications:
        return render(request, 'viewnotification.html', {'notifications': notifications, 'current_user': current_user})
    else:
        return redirect('teacherhome')
def markview(request,pk):
    data=teachernotification.objects.get(id=pk)
    data.delete()
    return redirect('teacherhome')