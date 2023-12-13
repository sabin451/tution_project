from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.login1,name='login1'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('studenthome',views.studenthome,name='studenthome'),
    path('teacherhome',views.teacherhome,name='teacherhome'),
    path('addcourse',views.addcourse,name='addcourse'),
    path('department',views.department,name='department'),
    path('sregistration',views.sregistration,name='sregistration'),
    path('doregistration',views.doRegistration,name='doregistration'),
    path('doLogin',views.doLogin,name='doLogin'),
    path('doaddcourse',views.doaddcourse,name='doaddcourse'),
    path('managecourse',views.managecourse,name='managecourse'),
    path('adddepartment',views.adddepartment,name='adddepartment'),
    path('tableassign',views.tableassign,name='tableassign'),
    path('studentprofile',views.studentprofile,name='studentprofile'),
    path('teacherprofile',views.teacherprofile,name='teacherprofile'),


  
    path('studentatendance',views.studentatendance,name='studentatendance'),
    path('studentatendancedata',views.studentatendancedata,name='studentatendancedata'),      
    path('assignmentst',views.assignmentst,name='assignmentst'),
    path('doassignment',views.doassignment,name='doassignment'),
    path('studentpage',views.studentpage,name='studentpage'),
    path('teacherdetails',views.teacherdetails,name='teacherdetails'),
    path('teacherdetails1',views.teacherdetails1,name='teacherdetails1'),
    path('delteacher/<int:pk>',views.delteacher,name='delteacher'),
    path('logout',views.logout,name='logout'),
    path('studentdetails',views.studentdetails,name='studentdetails'),
    path('studentdetails1',views.studentdetails1,name='studentdetails1'),
    path('delstudent/<int:pk>',views.delstudent,name='delstudent'),
    path('viewuser',views.viewuser,name='viewuser'),
    path('approve/<int:pk>',views.approve,name='approve'),
    path('disapprove/<int:pk>',views.disapprove,name='disapprove'),
    path('present',views.present,name='present'),
    path('stattendanceview',views.stattendanceview,name='stattendanceview'),

    path('teacherattendanceview',views.teacherattendanceview,name='teacherattendanceview'),
    path('present1',views.present1,name='present1'),
    path('absent1/<int:pk>',views.absent1,name='absent1'),
    
    path('teviewattendance',views.teviewattendance,name='teviewattendance'),

    path('pushassignment/<int:pk>/',views.pushassignment,name='pushassignment'),

    path('viewassignment',views.viewassignment,name='viewassignment'),
    path('editteacher',views.editteacher,name='editteacher'),
    path('editstudent',views.editstudent,name='editstudent'),
    path('studentupdate',views.studentupdate,name='studentupdate'),
    path('teacherupdate',views.teacherupdate,name='teacherupdate'),
    
    path('resetpassword',views.resetpassword,name='resetpassword'),
    path('resetpassword1',views.resetpassword1,name='resetpassword1'),
    path('dogeneration',views.dogeneration,name='dogeneration'),
    path('dogeneration1',views.dogeneration1,name='dogeneration1'),
    
    path('tregistration',views.tregistration,name='tregistration'),
    path('edit_course<int:course_id>', views.edit_course, name='edit_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('approve_notification/<int:pk>/', views.approve_notification, name='approve_notification'),
    path('disapprove_notification/<int:pk>/', views.disapprove_notification, name='disapprove_notification'),
    
    path('student_course', views.student_course, name='student_course'),
    path('teacher_course', views.teacher_course, name='teacher_course'),
    
    
    path('course_details/<int:course_id>/', views.course_details, name='course_details'),
    path('course_details1/<int:course_id>/', views.course_details1, name='course_details1'),

    
    
    path('assign_teacher', views.assign_teacher, name='assign_teacher'),
    path('assign_student', views.assign_student, name='assign_student'),
    path('add_assign_teacher/', views.add_assign_teacher, name='add_assign_teacher'),
    path('add_assign_student/', views.add_assign_student, name='add_assign_student'),    
    
    path('adminstudentattendance',views.adminstudentattendance,name='adminstudentattendance'),
    path('adminstudentatendancedata',views.adminstudentatendancedata,name='adminstudentatendancedata'),
    
    path('teacherviewstudentatten',views.teacherviewstudentatten,name='teacherviewstudentatten'),
    path('teachertableassign',views.teachertableassign,name='teachertableassign'),
    
    path('viewnotification',views.viewnotification,name='viewnotification'),
    path('markview/<int:pk>',views.markview,name='markview'),
]
