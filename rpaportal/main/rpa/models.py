from django.db import models
from django.conf import settings
import os
from django.utils import timezone
media_url = settings.MEDIA_URL
media_root = settings.MEDIA_ROOT


class task_info_detail_info(models.Model):
    created_date = models.DateTimeField(auto_now=True)
    rpa_id = models.CharField(max_length=30)
    rpamanager_chk = models.CharField(max_length=2)
    analyze_date = models.CharField(max_length=10)
    task_completed = models.CharField(max_length=2)
    progress_job = models.TextField(blank=True)
    progress_job_done = models.CharField(max_length=100)
    retry_method = models.TextField(blank=True)
    retry_updated_date = models.DateTimeField(auto_now=True)

    def formatted_date(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M')



class task_info_dt(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    taskname = models.CharField(max_length=26)
    taskexplanation = models.TextField(blank=True)
    manager_name = models.TextField(blank=True)
    manager_empno = models.TextField(blank=True)
    rpa_method = models.CharField(max_length=100)
    pertime_min = models.CharField(max_length=100)
    task_group1 = models.CharField(max_length=1000)
    task_group2 = models.CharField(max_length=1000)
    progress_status = models.CharField(max_length=100)
    use_yn = models.CharField(max_length=1)
    manager_amount = models.CharField(max_length=10)
    business_type = models.CharField(max_length=10)
    change_reason = models.TextField(blank=True)

    def formatted_date(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M')


class filemanage(models.Model):
    created_date = models.DateTimeField(auto_now=True)
    taskname = models.CharField(max_length=26)
    file = models.FileField(upload_to='file/%Y/%m/%d', blank=True)

    def formatted_date(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M')
    def filename(self):
        input_string = str(self.file)
        result = input_string.split("/")[-1]
        return result
    def filesize(self):
        filename = str(self.file)
        file_path = os.path.join(media_root, filename)
        if os.path.exists(file_path):
            file_size_in_bytes = os.path.getsize(file_path)
            file_size_in_kb = file_size_in_bytes / 1024
            file_size_in_mb = file_size_in_kb / 1024
            if file_size_in_kb % 1 == 0:
                file_size_in_mb_rounded = round(file_size_in_mb, 1)
                return f"{file_size_in_mb_rounded} MB"
            else:
                return f"{int(file_size_in_kb)} KB"
        else:
            return "File not found"


class task_maillist_dt(models.Model):
    rpa_id = models.CharField(max_length=10)
    mailto = models.TextField(blank=True)
    mailcc = models.TextField(blank=True)
    EMPNO = models.CharField(max_length=10)
    NAME_KO = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now=True)

    def formatted_date(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M')


class task_comments_dt(models.Model):
    rpa_id = models.CharField(max_length=10)
    comment_id = models.CharField(max_length=21)
    comment = models.CharField(max_length=100)
    NAME_KO = models.CharField(blank=True, max_length=100)
    PART_NM = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now=True)
    use_yn = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now=True)
    empno = models.TextField(blank=True)

    def formatted_date(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M')



class emplist_dt(models.Model):
    EMPNO = models.CharField(max_length=10)
    NAME_KO = models.CharField(max_length=100)
    NAME_EN = models.CharField(max_length=100)
    CLNM = models.CharField(blank=True, max_length=100)
    CO_NM = models.CharField(max_length=100)
    TEAM_NM = models.CharField(max_length=100)
    PART_NM = models.CharField(max_length=100)
    BU_NM = models.CharField(max_length=100)
    EMAIL = models.CharField(blank=True, max_length=100)


class master_setting_dt(models.Model):
    counter = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    contents = models.CharField(max_length=20)
    updated_date = models.DateTimeField(auto_now=True)
    empno = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def formatted_date(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M')


class user_log_dt(models.Model):
    rpa_id = models.CharField(max_length=10)
    change_log = models.TextField(blank=True)
    empno = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now=True)

    def formatted_date(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M')


class login_log_dt(models.Model):
    empno = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    request_time = models.DateTimeField(auto_now=True)

    def formatted_date(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M')


class admin_user_dt(models.Model):
    empno = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now=True)

    def formatted_date(self):
        return self.created_date.strftime('%Y-%m-%d %H:%M')