import pyodbc
import json
from datetime import datetime, timedelta

# Define your constants
server = '130.1.22.33'
database = 'SYG-RPA-DB'
username = 'sa'
password = '@sygrpa22!'
port = '2433'

# Define your mappings
word_to_number = {
    "FIRST": 1,
    "SECOND": 2,
    "THIRD": 3,
    "FOURTH": 4,
    "FIFTH": 5
}

month_mapping = {
    'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
    'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
}

weekday_mapping = {
    'MON': 1, 'TUE': 2, 'WED': 3, 'THU': 4, 'FRI': 5, 'SAT': 6, 'SUN': 7
}

# Helper functions
def parse_null(value):
    return value if value is not None else None

def convert_month(month):
    return month_mapping.get(month)

def convert_weekday(weekday):
    return weekday_mapping.get(weekday)

def convert_word(word):
    return word_to_number.get(word)

def get_week_number(date_string):
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    first_day_of_month = date_object.replace(day=1)
    first_day_of_month_weekday = first_day_of_month.weekday()
    
    if first_day_of_month_weekday in [3, 4, 5]:  # If Thursday, Friday, Saturday
        first_week_start = first_day_of_month
    else: 
        first_week_start = first_day_of_month - timedelta(days=first_day_of_month_weekday)
    
    week_number = ((date_object - first_week_start).days // 7) + 1
    
    return week_number

# Main function to generate schedule data
def generate_schedule_data(date_str):
    conn_str = f'DRIVER={{SQL Server}};SERVER={server},{port};DATABASE={database};UID={username};PWD={password}'
    json_str = '[]'

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("""
            WITH FilteredJobExecutions AS (
                SELECT
                    [bot_id],
                    [device_id],
                    DATEDIFF(minute, [start_datetime], [end_datetime]) AS duration_minutes,
                    ROW_NUMBER() OVER(PARTITION BY [bot_id] ORDER BY [start_datetime] DESC) AS row_num
                FROM
                    [SYG-RPA-DB].[dbo].[JOBEXECUTIONS]
                WHERE
                    [start_datetime] >= DATEADD(month, -6, GETDATE())
                    AND [activity_status] = 'COMPLETED'
            ),
            AvgDuration AS (
                SELECT
                    [bot_id],
                    AVG(CAST(duration_minutes AS FLOAT)) AS avg_duration_minutes
                FROM
                    FilteredJobExecutions
                GROUP BY
                    [bot_id]
            )
            SELECT
                ASCH.[id],
                ASCH.[name],
                ASCH.[created_on],
                ASCH.[updated_on],
                ASCH.[recurrence_type],
                ASCH.[recurrence_interval],
                ASCH.[clock_recurrence_start_time],
                ASCH.[clocktime_recurrence_end_time],
                ASCH.[clocktime_recurrence_runevery],
                ASCH.[recurrence_dates_of_month],
                ASCH.[recurrence_week_of_month],
                ASCH.[recurrence_days_of_week],
                ASCH.[recurrence_months],
                ASCH.[time_recurrence_type],
                D.[hostname],
                AD.avg_duration_minutes
            FROM
                [SYG-RPA-DB].[dbo].[AUTOMATION_SCHEDULE] AS ASCH
            LEFT JOIN
                FilteredJobExecutions AS JE ON ASCH.[task_id] = JE.[bot_id] AND JE.row_num = 1
            LEFT JOIN
                AvgDuration AS AD ON JE.[bot_id] = AD.[bot_id]
            LEFT JOIN
                [SYG-RPA-DB].[dbo].[DEVICES] AS D ON JE.[device_id] = D.id
            WHERE
                ASCH.[status] = '1';
            """)

        rows = cursor.fetchall()
        data = json.loads(json_str)

        for row in rows:
            name = row[1].split('.')[0].strip()
            if "Trigger" in name:
                continue  
            recurrence_type = row[4]
            recurrence_interval = row[5]
            clock_recurrence_start_time = row[6]
            clocktime_recurrence_end_time = row[7]
            clocktime_recurrence_runevery = row[8]
            recurrence_dates_of_month = row[9]
            recurrence_week_of_month = row[10]
            recurrence_days_of_week = row[11]
            recurrence_months = row[12]
            time_recurrence_type = row[13]
            runner = row[14] if row[14] else 'none'
            duration = str(row[15])[:5] if row[15] else "1"

            if recurrence_days_of_week:
                recurrence_days_of_week = [convert_weekday(day) for day in recurrence_days_of_week.split(',')]
            if recurrence_months:
                recurrence_months = [convert_month(month) for month in recurrence_months.split(',')]
            if recurrence_week_of_month:
                recurrence_week_of_month = [convert_word(word) for word in recurrence_week_of_month.split(',')]

            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            first_day_of_month = date_obj.replace(day=1)
            next_month = first_day_of_month.replace(month=first_day_of_month.month + 1)
            if next_month.month == 1:
                next_month = next_month.replace(year=next_month.year + 1)

            current_day = first_day_of_month
            while current_day < next_month:
                weekday_number = current_day.isoweekday()
                datePresent = current_day.strftime('%Y-%m-%d')
                month_number = current_day.month
                day_number = current_day.day
                week_number = get_week_number(datePresent)

                if recurrence_type == 'DAILY':
                    if time_recurrence_type == "ONCE":
                        new_data = {
                            "taskname": name,
                            "date": datePresent,
                            "start_time": clock_recurrence_start_time,
                            "runner" : runner,
                            "duration" : duration
                        }
                        data.append(new_data)
                    elif time_recurrence_type == "MANY":
                        start_time_str = clock_recurrence_start_time
                        end_time_str = clocktime_recurrence_end_time
                        recurrence_runevery_ms = clocktime_recurrence_runevery

                        def print_time_range(start_time_str, end_time_str, recurrence_runevery_ms):
                            start_time = datetime.strptime(start_time_str, '%H:%M')
                            end_time = datetime.strptime(end_time_str, '%H:%M')

                            recurrence_runevery_sec = recurrence_runevery_ms / 1000
                            current_time = start_time
                            while current_time <= end_time:
                                added_start_time = current_time.strftime('%H:%M')
                                new_data = {
                                    "taskname": name,
                                    "date": datePresent,
                                    "start_time": added_start_time,
                                    "runner" : runner,
                                    "duration" : duration
                                    }
                                data.append(new_data)
                                current_time += timedelta(seconds=recurrence_runevery_sec)
                        print_time_range(start_time_str, end_time_str, recurrence_runevery_ms)
                elif recurrence_type == 'WEEKLY':
                    if time_recurrence_type == "ONCE":
                        if weekday_number in recurrence_days_of_week:
                            new_data = {
                                "taskname": name,
                                "date": datePresent,
                                "start_time": clock_recurrence_start_time,
                                "runner" : runner,
                                "duration" : duration
                            }
                            data.append(new_data)
                    elif time_recurrence_type == "MANY":

                        start_time_str = clock_recurrence_start_time
                        end_time_str = clocktime_recurrence_end_time
                        recurrence_runevery_ms = clocktime_recurrence_runevery

                        def print_time_range(start_time_str, end_time_str, recurrence_runevery_ms):
                            start_time = datetime.strptime(start_time_str, '%H:%M')
                            end_time = datetime.strptime(end_time_str, '%H:%M')

                            recurrence_runevery_sec = recurrence_runevery_ms / 1000
                            current_time = start_time
                            while current_time <= end_time:
                                added_start_time = current_time.strftime('%H:%M')
                                new_data = {
                                    "taskname": name,
                                    "date": datePresent,
                                    "start_time": added_start_time,
                                    "runner" : runner,
                                    "duration" : duration
                                    }
                                data.append(new_data)
                                current_time += timedelta(seconds=recurrence_runevery_sec)
                        print_time_range(start_time_str, end_time_str, recurrence_runevery_ms)

                elif recurrence_type == 'MONTHLY':

                    if time_recurrence_type == "ONCE":

                        if month_number in recurrence_months:
                            if str(recurrence_dates_of_month) == str(day_number):
                                new_data = {
                                    "taskname": name,
                                    "date": datePresent,
                                    "start_time": clock_recurrence_start_time,
                                    "runner" : runner,
                                    "duration" : duration
                                    }
                                data.append(new_data)

                            elif str(recurrence_dates_of_month) == 'None':
                                if week_number in recurrence_week_of_month and weekday_number in recurrence_days_of_week:
                                    new_data = {
                                        "taskname": name,
                                        "date": datePresent,
                                        "start_time": clock_recurrence_start_time,
                                        "runner" : runner,
                                        "duration" : duration
                                        }
                                    data.append(new_data)

                current_day += timedelta(days=1)

    except pyodbc.Error as e:
        print(f'Database connection error: {e}')
        return None

    finally:
        if 'conn' in locals():
            conn.close()

    return json.dumps(data)

# Test the function with a date string
date_str = "2024-06-03"
updated_json_str = generate_schedule_data(date_str)
print(updated_json_str)
