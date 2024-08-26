from django.views.static import serve
from django.urls import path, include, re_path
from . import views
from django.shortcuts import render
from django.conf import settings

handler404 = 'rpa.views.error_404_view'

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('requestnewtask/', views.creatNewTask),
    path('taskList/', views.taskList, name='taskList'),
    path('taskList/<str:details>/', views.taskDetails, name='task_details'),
    path('teamCalendar/', views.teamCalendar),
    path('rpabotmonitering/', views.rpabotmonitering),
    path('rpaTodoList/', views.rpaTodoList, name='rpaTodoList'),
    path('rpaManageList/', views.rpaManageList),
    path('rpaManageList_stop/', views.rpaManageList_stop),
    path('login/', views.loginpage, name='loginpage'),
    path('logout/', views.logout, name='logout'),
    path('test/', views.test, name='test'),
    path('settingaccount/', views.settingaccount, name='settingaccount'),
    path('settingmaster/', views.settingmaster, name='settingmaster'),
    path('uploadfiles/', views.uploadfiles, name='uploadfiles'),
    path('uploadfiles_task_indi/', views.uploadfiles_task_indi, name='uploadfiles_task_indi'),
    path('deletefile_task_indi/', views.deletefile_task_indi, name='deletefile_task_indi'),
    path('deletefile/', views.deletefile, name='deletefile'),
    path('deletefileleaved/', views.deletefile_leaved, name='deletefile_leaved'),
    path('mainList_all/', views.taskList_all, name='taskList_all'),
    path('updatestatus/', views.updatestatus, name='updatestatus'),
    path('updatestatus_details/', views.updatestatus_details, name='updatestatus_details'),
    path('updateexplanation/', views.update_explanation, name='update_explanation'),
    path('updatemaillist/', views.update_taskmaillist, name='update_taskmaillist'),
    path('error_page/', views.error_page, name='error_page'),
    path('createNewProject/', views.createNewProject, name='createNewProject'),
    path('getIDSendList/', views.getIDSendList, name='getIDSendList'),
    path('getAllEmp/', views.getAllEmp, name='getAllEmp'),
    path('updatemanager/', views.update_manager, name='update_manager'),
    path('updatetitle/', views.update_title, name='update_title'),
    path('updatecomment/', views.update_comment, name='update_comment'),
    path('updatebiztype/', views.update_biztype, name='update_biztype'),
    path('updatetaskgrp1/', views.update_taskgrp1, name='update_taskgrp1'),
    path('updatetaskgrp2/', views.update_taskgrp2, name='update_taskgrp2'),
    path('updaterpamethod/', views.update_rpamethod, name='update_rpamethod'),
    path('updatemngramount/', views.update_mngramount, name='update_mngramount'),
    path('updatepermin/', views.update_permin, name='update_permin'),
    path('cancelrequest/', views.cancel_request, name='cancel_request'),
    path('editcomment/', views.edit_comment, name='edit_comment'),
    path('removecomment/', views.remove_comment, name='remove_comment'),
    path('addaduser/', views.add_aduser, name='add_aduser'),
    path('editaduser/', views.edit_aduser, name='edit_aduser'),
    path('deladuser/', views.del_aduser, name='del_aduser'),
    path('editlist1/', views.edit_list1, name='edit_list1'),
    path('editlist2/', views.edit_list2, name='edit_list2'),
    path('getretry/', views.get_retry, name='get_retry'),
    path('saveretry/', views.save_retry, name='save_retry'),
    path('updatemainchart/', views.update_main_chart, name='update_main_chart'),
    path('updatemainchart_biz/', views.update_mainchart_biz, name='update_mainchart_biz'),
    path('getrpaexecution/', views.getrpaexecution, name='getrpaexecution'),
    path('getrpaexecution_yesterday/', views.getrpaexecution_yesterday, name='getrpaexecution_yesterday'),
    path('updatemanagetaskstatus/', views.update_managetaskstatus, name='update_managetaskstatus'),
    path('gettask_maillist/<str:pk>/<str:key>/', views.gettask_maillist, name='gettask_maillist'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]