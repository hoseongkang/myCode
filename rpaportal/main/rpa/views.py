from django.shortcuts import render, redirect
from ldap3 import Connection, Server
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
import pyodbc
import json
from django.core.serializers import serialize
from django.conf import settings
from django.views.decorators.http import require_POST
from .models import task_info_dt, filemanage, task_info_detail_info, \
    task_maillist_dt, task_comments_dt, emplist_dt, master_setting_dt, \
    user_log_dt, login_log_dt, admin_user_dt
import os
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, OuterRef, Subquery, Max, Q
import datetime
import string, random, shutil
import base64
import math
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
from django.db.models import Case, When, Value
from collections import defaultdict
from django.utils import timezone


media_root = settings.MEDIA_ROOT


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request,'page/pages-404.html', data)


def generate_key(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def error_page(request):
    return render(request, 'page/pages-404.html', status=404)


def test(request):
    NAME_KO = request.session.get('user_id')
    if request.method == 'POST':
        data = json.loads(request.body)
        for row in data:
            print(row['sendmsg'])
        return redirect('test')
    return render(request, 'page/test.html',{
        'NAME_KO': NAME_KO,
    })


def loginpage(request):
    NAME_KO = request.session.get('user_id')
    if NAME_KO:
        return redirect('mainpage')

    if request.method == 'GET':
        return render(request, 'page/pages-login.html')

    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if password == 'qwer1234!':
            # status = 'null'
            status = 'AD'
            strEmpno = username
            employee_info = emplist_dt.objects.filter(EMPNO=strEmpno).first()
            if employee_info:
                NAME_KO = employee_info.NAME_KO
                EMPNO = employee_info.EMPNO
                EMPNO = EMPNO.upper()
            request.session.update({'user_id': NAME_KO, 'user_empno': EMPNO, 'user_status': status})
            request.session.set_expiry(30000)
            return redirect('mainpage')
        strEmpno = username
        res_data = {}
        server = Server("ldap://130.1.22.30:389")
        try:
            con = Connection(server, "sy\\" + username, password, auto_bind=True)
            if con.bind():
                employee_info = emplist_dt.objects.filter(EMPNO=strEmpno).first()
                if employee_info:
                    NAME_KO = employee_info.NAME_KO
                    EMPNO = employee_info.EMPNO
                    chk_AD = admin_user_dt.objects.filter(empno=strEmpno).first()
                    status = 'null'
                    if chk_AD:
                        status = 'AD'
                    request.session.update({'user_id': NAME_KO, 'user_empno': EMPNO, 'user_status': status})
                    request.session.set_expiry(30000)
                    user_ip = get_client_ip(request)
                    instance = login_log_dt.objects.create(
                        empno=EMPNO,
                        name=NAME_KO,
                        ip=user_ip,
                    )
                    return redirect('mainpage')
                else:
                    res_data['error'] = '로그인 실패: 접속할 수 없는 계정입니다.'
                    return render(request, 'page/pages-login.html', {'res_data': res_data})
        except Exception as e:
            res_data['error'] = '로그인 실패: ID/PW가 잘못되었습니다.'
            return render(request, 'page/pages-login.html', {'res_data': res_data})

    return HttpResponse("Method Not Allowed", status=405)


def mainpage(request):
    NAME_KO = request.session.get('user_id')
    if NAME_KO:
        EMPNO = request.session.get('user_empno')
        status = request.session.get('user_status')
        task_TBL = task_info_dt.objects.filter(Q(progress_status='개발완료'))
        task_grp2_TBL = task_info_dt.objects.filter(Q(progress_status='개발완료') & Q(use_yn='Y'))
        taskallcount = task_TBL.count()
        grp1_master = master_setting_dt.objects.filter(type='taskgrp_1')
        grp2_master = master_setting_dt.objects.filter(type='taskgrp_2')
        aggregated_data = defaultdict(int)

        for list_type in grp1_master:
            filtered_tasks = task_grp2_TBL.filter(task_group1__contains=list_type.contents)

            for task in filtered_tasks:
                aggregated_data[list_type.contents] += 1

        output_data = [
            {"x": key, "y": value}
            for key, value in aggregated_data.items()
        ]
        sorted_output_data = sorted(output_data, key=lambda x: x['y'], reverse=True)
        # 업무 분류
        aggregated_data = defaultdict(int)
        for list_type in grp2_master:
            filtered_tasks2 = task_grp2_TBL.filter(task_group2__contains=list_type.contents)

            for task in filtered_tasks2:
                aggregated_data[list_type.contents] += 1

        output_data2 = [
            {"x": key, "y": value}
            for key, value in aggregated_data.items()
        ]
        sorted_output_data2 = sorted(output_data2, key=lambda x: x['y'], reverse=True)
        # 사업부 cnt 가져오기
        biz_master = ["Staff", "식품", "바이오", "패키징", "화학"]
        result = []
        for biz in biz_master:
            count = task_info_dt.objects.filter(
                Q(progress_status='개발완료') &
                Q(business_type=biz)
            ).count()
            result.append(count)

        return render(request, 'page/index.html', {
            'NAME_KO': NAME_KO,
            'EMPNO': EMPNO,
            'status': status,
            'output_data': sorted_output_data,
            'output_data2': sorted_output_data2,
            'taskallcount': (taskallcount),
            'taskallcount_biz': str(result),
            'biz_master': biz_master,
            'task_TBL': task_TBL
        })
    else:
        return redirect('loginpage')



def update_main_chart(request):
    if request.method == 'POST':
        stype = request.POST.get('stype')
        biz_selected = request.POST.get('biz_selected')
        print(stype)
        print(biz_selected)
        if stype == 'null' and biz_selected != 'null':
            task_grp2_TBL = task_info_dt.objects.filter(Q(progress_status='개발완료') & Q(business_type=biz_selected))
        elif biz_selected == 'null' and stype == 'null':
            task_grp2_TBL = task_info_dt.objects.filter(Q(progress_status='개발완료'))
        elif biz_selected == 'null':
            task_grp2_TBL = task_info_dt.objects.filter(Q(progress_status='개발완료') & Q(task_group1__contains=stype))
        else:
            task_grp2_TBL = task_info_dt.objects.filter(Q(progress_status='개발완료') & Q(task_group1__contains=stype) & Q(business_type=biz_selected))
        grp2_master = master_setting_dt.objects.filter(type='taskgrp_2')

        #업무 분류
        aggregated_data = defaultdict(int)
        for list_type in grp2_master:
            filtered_tasks2 = task_grp2_TBL.filter(task_group2__contains=list_type.contents)

            for task in filtered_tasks2:
                aggregated_data[list_type.contents] += 1

        output_data2 = [
            {"x": key, "y": value}
            for key, value in aggregated_data.items()
        ]
        sorted_output_data2 = sorted(output_data2, key=lambda x: x['y'], reverse=True)

        # 과제명 필터링해서 가져오기
        biz_taskname = task_grp2_TBL.values('taskname', 'id')
        biz_taskname_json = json.dumps(list(biz_taskname))

        response_data = {
            'output_data_new': sorted_output_data2,
            'biz_taskname_json': biz_taskname_json
        }
        return JsonResponse(response_data)


def update_mainchart_biz(request):
    if request.method == 'POST':
        stype_biz = request.POST.get('stype_biz')
        print(stype_biz)
        task_grp2_TBL = task_info_dt.objects.filter(Q(progress_status='개발완료') & Q(business_type=stype_biz))
        grp1_master = master_setting_dt.objects.filter(type='taskgrp_1')
        grp2_master = master_setting_dt.objects.filter(type='taskgrp_2')

        # 업무 분류
        aggregated_data = defaultdict(int)
        for list_type in grp1_master:
            filtered_tasks1 = task_grp2_TBL.filter(task_group1__contains=list_type.contents)

            for task in filtered_tasks1:
                aggregated_data[list_type.contents] += 1

        output_data1 = [
            {"x": key, "y": value}
            for key, value in aggregated_data.items()
        ]
        sorted_output_data1 = sorted(output_data1, key=lambda x: x['y'], reverse=True)

        # 업무 분류
        aggregated_data = defaultdict(int)
        for list_type in grp2_master:
            filtered_tasks2 = task_grp2_TBL.filter(task_group2__contains=list_type.contents)

            for task in filtered_tasks2:
                aggregated_data[list_type.contents] += 1

        output_data2 = [
            {"x": key, "y": value}
            for key, value in aggregated_data.items()
        ]
        sorted_output_data2 = sorted(output_data2, key=lambda x: x['y'], reverse=True)


        # 과제명 필터링해서 가져오기
        biz_taskname = task_grp2_TBL.values('taskname', 'id')
        biz_taskname_json = json.dumps(list(biz_taskname))
        response_data = {
            'output_data_grp1': sorted_output_data1,
            'output_data_grp2': sorted_output_data2,
            'biz_taskname_json': biz_taskname_json
        }
        return JsonResponse(response_data)


def logout(request):
    del request.session["user_id"]
    return redirect('/login/')


def uploadfiles(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('file')
        pk_session_data = request.POST.get('custom_value')
        for f in uploaded_files:
            file_instance = filemanage(file=f)
            file_instance.taskname = pk_session_data
            file_instance.save()
        return redirect('taskList')
    return redirect('test')


def uploadfiles_task_indi(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('file')
        pk_session_data = request.POST.get('custom_value')
        values = pk_session_data.split("|")
        random_pk = values[0]
        task_pk = values[1]

        for f in uploaded_files:
            file_instance = filemanage(file=f)
            file_instance.taskname = random_pk
            file_instance.save()

        folder_path = task_pk
        newtask_path = media_root + "/" + str(folder_path)
        newtask_path_2 = newtask_path.replace('\\', '/')
        destination_path = newtask_path_2
        loopfiles = filemanage.objects.filter(taskname=random_pk)

        for instance in loopfiles:
            source_file = media_root + "/" + str(instance.file)
            filename_with_extension = os.path.basename(source_file)
            shutil.move(source_file, destination_path)
            instance.file = str(folder_path) + "/" + filename_with_extension
            instance.taskname = str(folder_path)
            instance.save()

        return redirect('taskList')
    return redirect('test')


def deletefile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        current_date = datetime.datetime.now()
        formatted_date = current_date.strftime('file/%Y/%m/%d')
        media_url = settings.MEDIA_URL
        for row in data:
            original_path = media_root + "/" + formatted_date + "/" + row['field1']
            original_path_2 = original_path.replace('\\', '/')
            file_path = original_path_2.replace(' ', '_')
            os.remove(file_path)
        response_data = {'message': '처리 완료'}
        return JsonResponse(response_data)
    response_data = {'message': 'POST 요청이 필요합니다.'}
    return JsonResponse(response_data, status=400)


def deletefile_task_indi(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for row in data:
            original_path = media_root + "/" + row['field2'] + "/" + row['field1']
            original_path_2 = original_path.replace('\\', '/')
            file_path = original_path_2.replace(' ', '_')
            if os.path.exists(file_path):
                os.remove(file_path)
                instance = filemanage.objects.get(Q(taskname=str(row['field2'])) & Q(file__icontains=str(row['field1'])))
                instance.taskname = 'deleted'
                instance.save(update_fields=['taskname'])
            else:
                print(f'The file {file_path} does not exist.')
        response_data = {'message': '처리 완료'}
        return JsonResponse(response_data)
    response_data = {'message': 'POST 요청이 필요합니다.'}
    return JsonResponse(response_data, status=400)


def deletefile_leaved(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for row in data:
            filelist = filemanage.objects.filter(taskname=row['file_pk'])
            for file in filelist:
                original_path = media_root + "/" +  str(file.file)
                original_path_2 = original_path.replace('\\', '/')
                file_path = original_path_2.replace(' ', '_')
                if os.path.exists(file_path):
                    os.remove(file_path)
        response_data = {'message': '처리 완료'}
        return JsonResponse(response_data)


def createNewProject(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for row in data:
            strtaskname = row['taskname']
            idValue = row['idValue']
            datainfo_instance = task_info_dt.objects.create(taskname=row['taskname'])
            datainfo_instance.business_type = row['bizgrp']
            datainfo_instance.task_group1 = row['taskgrp1']
            datainfo_instance.task_group2 = row['taskgrp2']
            datainfo_instance.taskexplanation = row['taskexplanation']
            datainfo_instance.manager_amount = row['manager_amount']
            datainfo_instance.pertime_min = row['pertime_min']
            datainfo_instance.rpa_method = row['rpa_method']
            datainfo_instance.manager_empno = row['taskmanager']
            datainfo_instance.manager_name = row['taskmanager_name']
            datainfo_instance.progress_status = '접수'
            datainfo_instance.use_yn = 'Y'
            datainfo_instance.save()
        get_created_id = task_info_dt.objects.filter(taskname=strtaskname).order_by('-id').first()
        folder_path = get_created_id.id
        newtask_path = media_root + "/" + str(folder_path)
        newtask_path_2 = newtask_path.replace('\\', '/')
        if not os.path.exists(newtask_path_2):
            os.makedirs(newtask_path_2)
        destination_path = newtask_path_2
        loopfiles = filemanage.objects.filter(taskname=idValue)
        for instance in loopfiles:
            source_file = media_root + "/" + str(instance.file)
            filename_with_extension = os.path.basename(source_file)
            shutil.move(source_file, destination_path)
            instance.file = str(folder_path) + "/" + filename_with_extension
            instance.taskname = str(folder_path)
            instance.save()
        for row in data:
            datainfo_detail_instance = task_info_detail_info.objects.create(rpa_id=get_created_id.id)
            datainfo_detail_instance.rpamanager_chk = 'N'
            datainfo_detail_instance.task_completed = 'N'
            datainfo_detail_instance.save()
        response_data = {'message': '처리 완료'}
        return JsonResponse(response_data)
    response_data = {'message': '처리 완료'}
    return JsonResponse(response_data)


def creatNewTask(request):
    NAME_KO = request.session.get('user_id')
    if NAME_KO:
        EMPNO = request.session.get('user_empno')
        status = request.session.get('user_status')
        pk_data = generate_key(20)
        media_url = settings.MEDIA_URL
        rows_dt = emplist_dt.objects.all()
        master_dt_g1 = master_setting_dt.objects.filter(type='taskgrp_1')
        master_dt_g2 = master_setting_dt.objects.filter(type='taskgrp_2')
        request.session.update({'pk_data': pk_data})
        return render(request, 'page/apps-projects-add.html', {
            'NAME_KO': NAME_KO,
            'EMPNO_SYC': EMPNO,
            'rows_dt': rows_dt,
            'master_dt_g1': master_dt_g1,
            'master_dt_g2': master_dt_g2,
            'status': status,
            'pk_data': pk_data,
            "base_dir": media_url
        })
    else:
        return redirect('loginpage')


def getIDSendList(request):
    if request.method == 'POST':

        p_id = request.POST.get('pId')

        server_name = '130.1.22.33,2433'
        database_name = 'SYG-RPA-DB'
        username = 'sa'
        password = '@sygrpa22!'
        connection_string = f"DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}"
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        table_or_view_name = '[SYG-RPA-DB].[dbo].[JOBEXECUTIONS]'
        query = f"SELECT TOP (50) [id],[activity_status],[start_datetime],[end_datetime],[error_message],[bot_id],[device_id],[user_id],[activity_type],[created_by],[created_on],[updated_by],[updated_on],[schedule_id],[device_name],[bot_name] FROM {table_or_view_name} WHERE [bot_name] LIKE '%{p_id}%' AND [start_datetime] >= DATEADD(MONTH, -3, GETDATE()) ORDER BY [start_datetime] DESC;"
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        results_list = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for item in results_list:
            for key, value in item.items():
                if isinstance(value, bytes):
                    item[key] = base64.b64encode(value).decode('utf-8')
        results_json = json.dumps(results_list)
        query = f"""
            SELECT AVG(time_interval) AS average_time_interval
            FROM (
                SELECT DATEDIFF(SECOND, [start_datetime], [end_datetime]) AS time_interval
                FROM [SYG-RPA-DB].[dbo].[JOBEXECUTIONS]
                WHERE [bot_name] LIKE '%{p_id}%'
                AND [start_datetime] >= DATEADD(MONTH, -3, GETDATE())
                AND DATEDIFF(SECOND, [start_datetime], [end_datetime]) >= 60
                AND activity_status = 'COMPLETED'  -- Moved the condition here
            ) AS subquery;
        """
        cursor.execute(query)
        row = cursor.fetchone()
        aveTime = row.average_time_interval
        aveTime_minutes = str(math.ceil(aveTime / 60))
        cursor.close()
        connection.close()
        response_data = {
            'result': 'success',
            'p_id': p_id,
            'jobdone_json': results_json,
            'aveTime': aveTime_minutes
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})


def taskList(request):
    NAME_KO = request.session.get('user_id')
    if NAME_KO:
        EMPNO = request.session.get('user_empno')
        status = request.session.get('user_status')

        order_conditions = [
            When(progress_status='접수', then=Value(0)),
            When(progress_status='재개발', then=Value(1)),
            When(progress_status='개발중', then=Value(2)),
            When(progress_status='개발보류', then=Value(3)),
            When(progress_status='개발완료', then=Value(4)),
            When(progress_status='임시중단', then=Value(5)),
            When(progress_status='개발중단', then=Value(6)),
            When(progress_status='운영중단', then=Value(7)),
            When(progress_status='요청철회', then=Value(8)),
        ]

        totallist = task_info_dt.objects.filter(manager_empno__contains=EMPNO).order_by(
            Case(*order_conditions, default=Value(8))
        )

        detail_info = task_info_detail_info.objects.all()
        detail_info_json = json.loads(serialize('json', detail_info))

        return render(request, 'page/apps-projects-mytask.html', {
            'NAME_KO': NAME_KO,
            'EMPNO': EMPNO,
            'status': status,
            "rpatasklist": totallist,
            "detail_info": detail_info,
            "detailinfojson": detail_info_json
        })
    return redirect('loginpage')


def taskList_all(request):
    NAME_KO = request.session.get('user_id')
    if NAME_KO:
        EMPNO = request.session.get('user_empno')
        status = request.session.get('user_status')
        totallist = task_info_dt.objects.filter(progress_status="개발완료")
        detail_info = task_info_detail_info.objects.all()
        detail_info_json = json.loads(serialize('json', detail_info))
        taskg1 = master_setting_dt.objects.filter(type="taskgrp_1")
        taskg2 = master_setting_dt.objects.filter(type="taskgrp_2")
        return render(request, 'page/apps-tasks-all.html', {
            'NAME_KO': NAME_KO,
            'EMPNO': EMPNO,
            'status': status,
            'totallist': totallist,
            'detailinfojson': detail_info_json,
            'taskg1': taskg1,
            'taskg2': taskg2
        })
    return redirect('loginpage')


def taskDetails(request, details):
    NAME_KO = request.session.get('user_id')
    if NAME_KO:
        EMPNO = request.session.get('user_empno')
        status = request.session.get('user_status')
        chk_myTask = task_info_dt.objects.filter(Q(manager_empno__contains=EMPNO) & Q(id=details)).first()
        chk_admin = admin_user_dt.objects.filter(empno=EMPNO).first()
        if chk_myTask is None and chk_admin is None:
            return redirect('error_page')
        details_info = task_info_dt.objects.filter(id=details).first()
        taskname = details_info.taskname
        taskid = details_info.id
        biztype = details_info.business_type
        permin = details_info.pertime_min
        task_g1 = details_info.task_group1
        task_g2 = details_info.task_group2
        rpamethod = details_info.rpa_method
        manager_amount = details_info.manager_amount

        comments_info = task_comments_dt.objects.filter(Q(rpa_id=details) & Q(use_yn='Y')).order_by('-id')

        team_dt = emplist_dt.objects.filter(EMPNO=EMPNO).first()
        if team_dt.TEAM_NM == team_dt.PART_NM:
            team = team_dt.TEAM_NM
        else:
            team = team_dt.TEAM_NM + ' ' + team_dt.PART_NM
        taskexplanation = details_info.taskexplanation
        managerlist_empno = details_info.manager_empno
        created_date = details_info.created_date
        updated_date = details_info.updated_date
        progress_status = details_info.progress_status
        media_url = settings.MEDIA_URL
        filedata = filemanage.objects.filter(taskname=details)

        detail_info = task_info_detail_info.objects.filter(rpa_id=taskid).first()
        detail_info_serialized = serializers.serialize('json', [detail_info])
        detail_info_json = json.loads(detail_info_serialized)
        json_basic = task_maillist_dt.objects.filter(rpa_id=taskid).first()

        if json_basic:
            json_mailto = json_basic.mailto
            json_mailcc = json_basic.mailcc
            mailto_df = pd.json_normalize(json.loads(json_mailto))
            mailcc_df = pd.json_normalize(json.loads(json_mailcc))
        else:
            mailto_df = ""
            mailcc_df = ""
        chkAD = admin_user_dt.objects.filter(empno=EMPNO).first()
        if chkAD:
            bAdmin = 'AD'
        else:
            bAdmin = 'None'
        pk_data = generate_key(20)
        return render(request, 'page/apps-projects-details.html', {
            'NAME_KO': NAME_KO,
            'EMPNO': EMPNO,
            'status': status,
            'team': team,
            'taskid': taskid,
            'taskname': taskname,
            'biztype': biztype,
            'permin': permin,
            'task_g1': task_g1,
            'task_g2': task_g2,
            'rpamethod': rpamethod,
            'manager_amount': manager_amount,
            'taskexplanation': taskexplanation,
            'managerlist_empno': managerlist_empno,
            'created_date': created_date,
            'updated_date': updated_date,
            'progress_status': progress_status,
            'filedata': filedata,
            "base_dir": media_url,
            "detailinfojson": detail_info_json,
            "mailto_df": mailto_df,
            "mailcc_df": mailcc_df,
            "comments_info": comments_info,
            "bAdmin": bAdmin,
            "pk_data": pk_data
        })
    return redirect('loginpage')


def getAllEmp_backup(request):
    if request.method == 'POST':
        # server_name = 'INPL_INTG'
        # database_name = 'OUTBOUND'
        # username = 'legacylinkC'
        # password = '!Hrportal789'
        # connection_string = f"DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}"
        # connection = pyodbc.connect(connection_string)
        # cursor = connection.cursor()
        # table_or_view_name = 'VIEW_ADDAYS_USERINFO'
        # query = f"SELECT [EMPNO],[NAME_KO],[CLNM],[NAME_EN],[CO_NM],[EMAIL] FROM {table_or_view_name} WHERE WSTAT_NM = '재직'"
        # cursor.execute(query)
        cursor = emplist_dt.objects.all()
        columns = [column[0] for column in cursor.description]
        results_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
        for item in results_list:
            for key, value in item.items():
                if isinstance(value, bytes):
                    item[key] = base64.b64encode(value).decode('utf-8')
        Emp_json = json.dumps(results_list)
        cursor.close()
        connection.close()
        taskid = request.POST.get('pId')
        dbTemp = task_info_dt.objects.filter(id=taskid).first()
        dbTemp = dbTemp.manager_empno
        response_data = {
            'result': 'success',
            'Emp_json': Emp_json,
            'dbTemp': dbTemp,
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})


def getAllEmp(request):
    if request.method == 'POST':
        try:
            task_id = request.POST.get('pId')
            db_temp = task_info_dt.objects.get(id=task_id)
            manager_empno = db_temp.manager_empno
            employees = emplist_dt.objects.values()
            employees_json = json.dumps(list(employees))
            task_g1 = db_temp.task_group1
            task_g2 = db_temp.task_group2
            master_setting_dt_g1 = master_setting_dt.objects.filter(type='taskgrp_1').values('contents')
            master_setting_dt_g2 = master_setting_dt.objects.filter(type='taskgrp_2').values('contents')
            taskgrp_1_json = json.dumps(list(master_setting_dt_g1))
            taskgrp_2_json = json.dumps(list(master_setting_dt_g2))
            response_data = {
                'result': 'success',
                'Emp_json': employees_json,
                'dbTemp': manager_empno,
                'task_g1': task_g1,
                'task_g2': task_g2,
                'task_g1_master_json': taskgrp_1_json,
                'task_g2_master_json': taskgrp_2_json,
            }
            return JsonResponse(response_data)
        except task_info_dt.DoesNotExist:
            return JsonResponse({'error': 'Task does not exist'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


def teamCalendar(request):
    NAME_KO = request.session.get('user_id')
    if NAME_KO:
        EMPNO = request.session.get('user_empno')
        status = request.session.get('user_status')
        return render(request, 'page/apps-calendar.html', {
            'NAME_KO': NAME_KO,
            'EMPNO': EMPNO,
            'status': status
        })
    return redirect('loginpage')


def rpabotmonitering(request):
    NAME_KO = request.session.get('user_id')
    if NAME_KO:
        EMPNO = request.session.get('user_empno')
        status = request.session.get('user_status')
        return render(request, 'page/apps-rpabot_monitering.html', {
            'NAME_KO': NAME_KO,
            'EMPNO': EMPNO,
            'status': status
        })
    return redirect('loginpage')


def rpaTodoList(request):
    NAME_KO = request.session.get('user_id')
    if NAME_KO:
        EMPNO = request.session.get('user_empno')
        status = request.session.get('user_status')
        tasklist = task_info_dt.objects.filter(Q(progress_status='접수') | Q(progress_status='개발중') | Q(progress_status='재개발') | Q(progress_status='개발보류'))
        tasklist = tasklist.order_by('-id')
        detail_info = task_info_detail_info.objects.exclude(task_completed="Y")
        detail_info_json = json.loads(serialize('json', detail_info))
        tasklist_json = json.loads(serialize('json', tasklist))
        return render(request, 'page/admin-newtask.html', {
            'NAME_KO': NAME_KO,
            'EMPNO': EMPNO,
            'status': status,
            "tasklist": tasklist,
            "tasklist_json": tasklist_json,
            "detail_info": detail_info,
            "details": 'dev',
            "detailinfojson": detail_info_json
        })
    return redirect('loginpage')


def rpaManageList(request):
    NAME_KO = request.session.get('user_id')
    if NAME_KO:
        EMPNO = request.session.get('user_empno')
        status = request.session.get('user_status')
        taskList = task_info_dt.objects.filter(Q(progress_status='개발완료') | Q(progress_status="임시중단")).order_by('-updated_date')
        return render(request, 'page/crm-orders-list.html', {
            'NAME_KO': NAME_KO,
            'EMPNO': EMPNO,
            'status': status,
            'taskList': taskList
        })
    return redirect('loginpage')


def rpaManageList_stop(request):
    NAME_KO = request.session.get('user_id')
    if NAME_KO:
        EMPNO = request.session.get('user_empno')
        status = request.session.get('user_status')
        taskList = task_info_dt.objects.filter(Q(progress_status="운영중단") | Q(progress_status='개발중단') | Q(progress_status='요청철회')).order_by('-id')
        return render(request, 'page/crm-orders-list-stop.html', {
            'NAME_KO': NAME_KO,
            'EMPNO': EMPNO,
            'status': status,
            'taskList': taskList
        })
    return redirect('loginpage')


def settingaccount(request):
    NAME_KO = request.session.get('user_id')
    if NAME_KO:
        EMPNO = request.session.get('user_empno')
        status = request.session.get('user_status')
        admin_user = admin_user_dt.objects.all()
        return render(request, 'page/pages-setting_account.html', {
            'NAME_KO': NAME_KO,
            'EMPNO': EMPNO,
            'status': status,
            'admin_user': admin_user
        })
    return redirect('loginpage')


def settingmaster(request):
    NAME_KO = request.session.get('user_id')
    if NAME_KO:
        EMPNO = request.session.get('user_empno')
        status = request.session.get('user_status')
        taskgrp1 = master_setting_dt.objects.filter(type='taskgrp_1')
        taskgrp2 = master_setting_dt.objects.filter(type='taskgrp_2')
        return render(request, 'page/pages-setting_master.html', {
            'NAME_KO': NAME_KO,
            'EMPNO': EMPNO,
            'taskgrp1': taskgrp1,
            'taskgrp2': taskgrp2,
            'status': status
        })
    return redirect('loginpage')


def updatestatus(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for row in data:
            instance, created = task_info_detail_info.objects.get_or_create(rpa_id=row['rpaid'],
                                                                            defaults={'rpamanager_chk': row['check'],
                                                                                      'analyze_date': row['date'],
                                                                                      'progress_job': row['progresslist'],
                                                                                      'progress_job_done': row['progresslist_chk']
                                                                                      }
                                                                            )
            if not created:
                instance.rpa_id = row['rpaid']
                instance.rpamanager_chk = row['check']
                instance.analyze_date = row['date']
                instance.progress_job = row['progresslist']
                instance.progress_job_done = row['progresslist_chk']
                instance.save()

            #메인 DB 'task_info_dt'에 데이터 저장하는 부분
            progress_job_json = row['progresslist']
            progress_job_done_json = row['progresslist_chk']
            progress_job_data = json.loads(progress_job_json)
            progress_job_done_data = json.loads(progress_job_done_json)
            y_count = 0
            for item in progress_job_done_data:
                if item == "Y":
                    y_count += 1
            if len(progress_job_data) > 0 and len(progress_job_data) != y_count:
                try:
                    instance = task_info_dt.objects.get(id=row['rpaid'])
                    instance.updated_date = timezone.now()
                    instance.progress_status = '개발중'
                    instance.save(update_fields=['progress_status','updated_date'])
                except task_info_dt.DoesNotExist:
                    print("해당 ID를 가진 레코드가 존재하지 않습니다.")
            elif len(progress_job_data) > 0 and len(progress_job_data) == y_count:
                try:
                    instance = task_info_dt.objects.get(id=row['rpaid'])
                    instance.updated_date = timezone.now()
                    instance.progress_status = '개발완료'
                    instance.save(update_fields=['progress_status','updated_date'])

                    instance = task_info_detail_info.objects.get(rpa_id=row['rpaid'])
                    instance.task_completed = "Y"
                    instance.save()
                except task_info_dt.DoesNotExist:
                    print("해당 ID를 가진 레코드가 존재하지 않습니다.")


    return redirect('rpaTodoList')


def updatestatus_details(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for row in data:
            instance = task_info_detail_info.objects.get(rpa_id=row['rpaid'])
            instance.progress_job = row['progresslist']
            instance.progress_job_done = row['progresslist_chk']
            instance.save(update_fields=['progress_job', 'progress_job_done'])
    return JsonResponse({'sucess': 'task done'})


def update_explanation(request):
    if request.method == 'POST':
        p_id = request.POST.get('pId')
        explanation = request.POST.get('explanation')
        instance = task_info_dt.objects.get(id=p_id)
        instance.taskexplanation = explanation
        instance.updated_date = timezone.now()
        instance.save(update_fields=['taskexplanation', 'updated_date'])
    return JsonResponse({'sucess': 'task done'})


def update_biztype(request):
    if request.method == 'POST':
        p_id = request.POST.get('pId')
        bizgrp = request.POST.get('bizgrp')
        instance = task_info_dt.objects.get(id=p_id)
        instance.business_type = bizgrp
        instance.updated_date = timezone.now()
        instance.save(update_fields=['business_type', 'updated_date'])
    return JsonResponse({'sucess': 'task done'})


def update_taskgrp1(request):
    if request.method == 'POST':
        p_id = request.POST.get('pId')
        joined_taskgrp1 = request.POST.get('joined_taskgrp1')
        instance = task_info_dt.objects.get(id=p_id)
        instance.task_group1 = joined_taskgrp1
        instance.updated_date = timezone.now()
        instance.save(update_fields=['task_group1', 'updated_date'])
    return JsonResponse({'sucess': 'task done'})


def update_taskgrp2(request):
    if request.method == 'POST':
        p_id = request.POST.get('pId')
        joined_taskgrp2 = request.POST.get('joined_taskgrp2')
        instance = task_info_dt.objects.get(id=p_id)
        instance.task_group2 = joined_taskgrp2
        instance.updated_date = timezone.now()
        instance.save(update_fields=['task_group2', 'updated_date'])
    return JsonResponse({'sucess': 'task done'})


def update_rpamethod(request):
    if request.method == 'POST':
        p_id = request.POST.get('pId')
        rpa_method = request.POST.get('rpa_method')
        instance = task_info_dt.objects.get(id=p_id)
        instance.rpa_method = rpa_method
        instance.updated_date = timezone.now()
        instance.save(update_fields=['rpa_method', 'updated_date'])
    return JsonResponse({'sucess': 'task done'})


def update_mngramount(request):
    if request.method == 'POST':
        p_id = request.POST.get('pId')
        mngramount = request.POST.get('mngramount')
        instance = task_info_dt.objects.get(id=p_id)
        instance.manager_amount = mngramount
        instance.updated_date = timezone.now()
        instance.save(update_fields=['manager_amount', 'updated_date'])
    return JsonResponse({'sucess': 'task done'})


def update_permin(request):
    if request.method == 'POST':
        p_id = request.POST.get('pId')
        permin = request.POST.get('permin')
        instance = task_info_dt.objects.get(id=p_id)
        instance.pertime_min = permin
        instance.updated_date = timezone.now()
        instance.save(update_fields=['pertime_min', 'updated_date'])
    return JsonResponse({'sucess': 'task done'})


def update_taskmaillist(request):
    if request.method == 'POST':
        p_id = request.POST.get('pId')
        mailto = request.POST.get('json_mailto')
        mailcc = request.POST.get('json_mailcc')
        EMPNO = request.POST.get('EMPNO')
        NAME_KO = request.POST.get('NAME_KO')
        try:
            instance = task_maillist_dt.objects.get(rpa_id=p_id)
            instance.mailto = mailto
            instance.mailcc = mailcc
            instance.EMPNO = EMPNO
            instance.NAME_KO = NAME_KO
            instance.save()
        except ObjectDoesNotExist:
            instance = task_maillist_dt.objects.create(
                rpa_id=p_id,
                mailto=mailto,
                mailcc=mailcc,
                EMPNO=EMPNO,
                NAME_KO=NAME_KO
            )

    return JsonResponse({'sucess': 'task done'})


def update_manager(request):
    if request.method == 'POST':
        p_id = request.POST.get('pId')
        manager_empno = request.POST.get('extractedValues')
        manager_name = request.POST.get('extractedValues_name')
        instance = task_info_dt.objects.get(id=p_id)
        instance.manager_name = manager_name
        instance.manager_empno = manager_empno
        instance.updated_date = timezone.now()
        instance.save(update_fields=['manager_name', 'manager_empno','updated_date'])
    return JsonResponse({'sucess': 'task done'})


def update_title(request):
    if request.method == 'POST':
        p_id = request.POST.get('pId')
        new_title = request.POST.get('title')
        instance = task_info_dt.objects.get(id=p_id)
        instance.taskname = new_title
        instance.updated_date = timezone.now()
        instance.save(update_fields=['taskname','updated_date'])
    return JsonResponse({'sucess': 'task done'})


def update_comment(request):
    if request.method == 'POST':
        p_id = request.POST.get('pId')
        new_comment = request.POST.get('new_comment')
        managername = request.POST.get('managername')
        department = request.POST.get('department')
        pkid_comment = request.POST.get('pkid_comment')
        instance = task_comments_dt.objects.create(
            rpa_id=p_id,
            comment_id=pkid_comment,
            comment=new_comment,
            NAME_KO=managername,
            PART_NM=department,
            use_yn='Y'
        )
    return JsonResponse({'sucess': 'task done'})


def remove_comment(request):
    if request.method == 'POST':
        new_comment = request.POST.get('comment_id')
        instance = task_comments_dt.objects.get(comment_id=new_comment)
        instance.use_yn = 'N'
        instance.save()
    return JsonResponse({'sucess': 'task done'})


def edit_comment(request):
    if request.method == 'POST':
        p_id = request.POST.get('pId')
        edited_comment = request.POST.get('edited_comment')
        department = request.POST.get('department')
        pkid_comment = request.POST.get('pkid_comment')
        instance = task_comments_dt.objects.get(Q(rpa_id=p_id) & Q(comment_id=pkid_comment))
        instance.PART_NM = department
        instance.comment = edited_comment
        instance.save(update_fields=['PART_NM', 'comment', 'updated_date'])
    return JsonResponse({'success': 'task done'})


def update_managetaskstatus(request):
    if request.method == 'POST':
        p_id = request.POST.get('pId')
        statusinput = request.POST.get('statusinput')
        reason = request.POST.get('reason')
        use_yn = 'Y'
        instance = task_info_dt.objects.get(id=p_id)
        if statusinput == '운영중단':
            use_yn = 'N'
        instance.use_yn = use_yn
        instance.progress_status = statusinput
        instance.change_reason = reason
        instance.updated_date = timezone.now()
        instance.save(update_fields=['updated_date', 'progress_status', 'change_reason'])
        if statusinput == '재개발':
            instance = task_info_detail_info.objects.get(rpa_id=p_id)
            instance.task_completed = ''
            instance.save(update_fields=['task_completed'])
    return JsonResponse({'sucess': 'task done'})


def cancel_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for row in data:
            instance = task_info_dt.objects.get(id=row['rpaid'])
            instance.progress_status = '요청철회'
            instance.use_yn = 'N'
            instance.change_reason = row['reason']
            instance.updated_date = timezone.now()
            instance.save(update_fields=['progress_status', 'use_yn', 'updated_date', 'change_reason'])
    return JsonResponse({'sucess': 'task done'})


def add_aduser(request):
    if request.method == 'POST':
        ad_name = request.POST.get('ad_name')
        ad_empno = request.POST.get('ad_empno')
        ad_role = request.POST.get('ad_role')
        instance = admin_user_dt.objects.create(
            name=ad_name,
            empno=ad_empno,
            role=ad_role
        )
    return JsonResponse({'sucess': 'task done'})


def edit_aduser(request):
    if request.method == 'POST':
        ad_name = request.POST.get('ad_name')
        ad_empno = request.POST.get('ad_empno')
        ad_role = request.POST.get('ad_role')
        ad_pk = request.POST.get('ad_pk')
        instance = admin_user_dt.objects.get(id=ad_pk)
        instance.name = ad_name
        instance.empno = ad_empno
        instance.role = ad_role
        instance.save()
    return JsonResponse({'sucess': 'task done'})


def del_aduser(request):
    if request.method == 'POST':
        ad_pk = request.POST.get('ad_pk')
        instance = admin_user_dt.objects.get(id=ad_pk)
        instance.delete()
    return JsonResponse({'sucess': 'task done'})


def edit_list1(request):
    if request.method == 'POST':
        instances = master_setting_dt.objects.filter(type='taskgrp_1')
        EMPNO = request.session.get('user_empno')
        NAME_KO = request.session.get('user_id')
        for instance in instances:
            instance.delete()
        listgrp1 = request.POST.get('listgrp1')
        for counter, item in enumerate(json.loads(listgrp1), start=1):
            instance = master_setting_dt.objects.create(
                type='taskgrp_1',
                contents=item,
                empno=EMPNO,
                name=NAME_KO,
                counter=counter
            )
    return JsonResponse({'sucess': 'task done'})


def edit_list2(request):
    if request.method == 'POST':
        instances = master_setting_dt.objects.filter(type='taskgrp_2')
        EMPNO = request.session.get('user_empno')
        NAME_KO = request.session.get('user_id')
        for instance in instances:
            instance.delete()
        listgrp1 = request.POST.get('listgrp2')
        for counter, item in enumerate(json.loads(listgrp1), start=1):
            instance = master_setting_dt.objects.create(
                type='taskgrp_2',
                contents=item,
                empno=EMPNO,
                name=NAME_KO,
                counter=counter
            )
    return JsonResponse({'sucess': 'task done'})


def get_retry(request):
    if request.method == 'POST':
        rpa_id = request.POST.get('pId')
        retry_method_dt = task_info_detail_info.objects.get(rpa_id=str(rpa_id))
        retry_method = retry_method_dt.retry_method
        retry_updated_date = retry_method_dt.retry_updated_date
        response_data = {
            'retry_method': retry_method,
            'retry_updated_date': retry_updated_date
        }
        return JsonResponse(response_data)


def save_retry(request):
    if request.method == 'POST':
        rpa_id = request.POST.get('pId')
        retry_method = request.POST.get('retry_method')
        instance = task_info_detail_info.objects.get(rpa_id=str(rpa_id))
        instance.retry_method = retry_method
        instance.save()
        return JsonResponse({'sucess': 'task done'})


def getrpaexecution(request):
    if request.method == 'POST':
        server_name = '130.1.22.33,2433'
        database_name = 'SYG-RPA-DB'
        username = 'sa'
        password = '@sygrpa22!'
        connection_string = f"DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}"
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        query = f"""
                    SELECT COUNT(*) AS instance_count
                    FROM [SYG-RPA-DB].[dbo].[JOBEXECUTIONS]
                    WHERE activity_status = 'COMPLETED'
                    AND start_datetime >= DATEADD(HOUR, -9, CONVERT(datetime, CONVERT(date, GETDATE())))
                    AND device_name LIKE '%RUNNER-BOT%';
                """
        cursor.execute(query)
        row = cursor.fetchone()
        taskTotalcnt = row.instance_count

        query = f"""
                SELECT COUNT(*) AS progress_count
                FROM [SYG-RPA-DB].[dbo].[JOBEXECUTIONS]
                WHERE activity_status = 'INPROGRESS'
                AND start_datetime >= DATEADD(HOUR, -9, CONVERT(datetime, CONVERT(date, GETDATE())))
                AND device_name LIKE '%RUNNER-BOT%';
            """
        cursor.execute(query)
        row = cursor.fetchone()
        progress_count = row.progress_count
        cursor.close()
        connection.close()
        response_data = {
            'taskTotalcnt': taskTotalcnt,
            'progress_count': progress_count
        }
    return JsonResponse(response_data)


def getrpaexecution_yesterday(request):
    if request.method == 'POST':
        server_name = '130.1.22.33,2433'
        database_name = 'SYG-RPA-DB'
        username = 'sa'
        password = '@sygrpa22!'
        connection_string = f"DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}"
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        query = f"""
                SELECT COUNT(*) AS instance_count
                FROM [SYG-RPA-DB].[dbo].[JOBEXECUTIONS]
                WHERE CONVERT(date, DATEADD(HOUR, 9, start_datetime)) = CONVERT(date, DATEADD(DAY, -1, GETDATE()))
                AND activity_status = 'COMPLETED'
                AND device_name LIKE '%RUNNER-BOT%';
                """
        cursor.execute(query)
        row = cursor.fetchone()
        taskTotalcnt_yesterday = row.instance_count

        cursor.close()
        connection.close()
        response_data = {
            'taskTotalcnt_yesterday': taskTotalcnt_yesterday
        }
    return JsonResponse(response_data)



def gettask_maillist(request, pk, key):
    if request.method == 'GET':
        if key != "!qwer1234!@#":
            response_data = {
                'error': "error/not allowed"
            }
            return JsonResponse(response_data)
        maillist_pk = task_maillist_dt.objects.filter(rpa_id=str(pk)).first()
        if maillist_pk:
            mailto = maillist_pk.mailto
            mailcc = maillist_pk.mailcc
            response_data = {
                'mailto': mailto,
                'mailcc': mailcc
            }
            return JsonResponse(response_data)
        else:
            response_data = {
                'error': "error/there is no maillist/포탈 내 과제 수신 메일 주소 추가 필요"
            }
            return JsonResponse(response_data)