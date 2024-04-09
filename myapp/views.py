# myapp/views.py
from django.shortcuts import render
from .models import Event
import sqlite3
import json
import os
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST,require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.conf import settings

@require_POST
def ajax_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username,password)
    user = User.objects.get(username=username)
    print(user.is_active)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"success": True}, content_type='application/json')
    else:
        return JsonResponse({"success": False, "message": "Invalid username or password."})


@require_POST
def create_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if User.objects.filter(username=username).exists():
        return JsonResponse({"success": False, "message": "Username already exists."})
    try:
        # 验证密码复杂度
        validate_password(password)

        # 创建用户
        user = User.objects.create_user(username, password)
        user.save()
        login(request, user)
        print("success ")
        return JsonResponse({"success": True, "message": "User created successfully."})

    except ValidationError as e:
        # 如果密码验证失败，返回错误信息
        return JsonResponse({"success": False, "message": "\n".join(e.messages)})


def show_events(request):

    db_path = os.path.join(settings.BASE_DIR, 'events.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT * FROM Events")
    events = c.fetchall()

    events_with_details = []

    for event in events:
        c.execute("SELECT * FROM ShowInfo WHERE event_uid=?", (event[0],))
        show_info_list = c.fetchall()

        # 存储当前事件的所有show详细信息
        shows_details = []

        for show_info in show_info_list:
            # 获取当前show对应的location信息
            c.execute("SELECT * FROM Locations WHERE id=?", (show_info[3],))
            location = c.fetchone()

            # 创建包含show和location详细信息的字典
            show_details = {
                'time': show_info[2],
                'onSales': show_info[4],
                'price': show_info[5],
                'endTime': show_info[6],
                'location': location[1],
                'locationName': location[2],
                'latitude': location[3],
                'longitude': location[4]
            }
            shows_details.append(show_details)

        # 创建包含事件和对应show详细信息的字典
        event_with_details = {
            'UID': event[0],
            'title': event[1],
            'category': event[2],
            'descriptionFilterHtml': event[3],
            'imageUrl': event[4],
            'webSales': event[5],
            'sourceWebPromote': event[6],
            'comment': event[7],
            'editModifyDate': event[8],
            'sourceWebName': event[9],
            'startDate': event[10],
            'endDate': event[11],
            'hitRate': event[12],
            'shows': shows_details  # 添加与当前事件相关的所有show信息
        }
        events_with_details.append(event_with_details)

    conn.close()

    return render(request, 'myapp/index.html', {'events': events_with_details})


@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def operation(request):
    if request.method == 'GET':
        query = request.GET.get('query', None)
        response = display_page_or_query_data(request , query)
        if query:
            return JsonResponse(response)
        else:
            return render(request, 'myapp/index.html', response)

    elif request.method == 'PUT':
        return update_data(request)

    elif request.method == 'POST':
        return add_or_update_data(request)

    elif request.method == 'DELETE':
        return delete_data(request)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def display_page_or_query_data(request, query):
    db_path = os.path.join(settings.BASE_DIR, 'events.db')
    get_conn = sqlite3.connect(db_path)
    #get_conn = sqlite3.connect('events.db')
    c = get_conn.cursor()
    query = request.GET.get('query', None)
    if query:
        c.execute("SELECT * FROM Events WHERE UID LIKE ?", ('%' + query + '%',))
    else:
        c.execute("SELECT * FROM Events")
    events = c.fetchall()

    events_with_details = []
    for event in events:
        # 获取当前事件的所有show信息
        c.execute("SELECT * FROM ShowInfo WHERE event_uid=?", (event[0],))
        show_info_list = c.fetchall()

        # 存储当前事件的所有show详细信息
        shows_details = []

        for show_info in show_info_list:
            # 获取当前show对应的location信息
            c.execute("SELECT * FROM Locations WHERE id=?", (show_info[3],))
            location = c.fetchone()

            # 创建包含show和location详细信息的字典
            show_details = {
                'time': show_info[2],
                'onSales': show_info[4],
                'price': show_info[5],
                'endTime': show_info[6],
                'location': location[1],
                'locationName': location[2],
                'latitude': location[3],
                'longitude': location[4]
            }
            shows_details.append(show_details)

        # 创建包含事件和对应show详细信息的字典
        event_with_details = {
            'UID': event[0],
            'title': event[1],
            'category': event[2],
            'descriptionFilterHtml': event[3],
            'imageUrl': event[4],
            'webSales': event[5],
            'sourceWebPromote': event[6],
            'comment': event[7],
            'editModifyDate': event[8],
            'sourceWebName': event[9],
            'startDate': event[10],
            'endDate': event[11],
            'hitRate': event[12],
            'shows': shows_details  # 添加与当前事件相关的所有show信息
        }
        events_with_details.append(event_with_details)

    get_conn.close()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'events': events_with_details})
    else:
        return {'events': events_with_details}


def update_data(request):
    data = json.loads(request.body)
    events = data.get('events', [])
    print(events)
    db_path = os.path.join(settings.BASE_DIR, 'events.db')
    update_conn = sqlite3.connect(db_path)
    #uptate_conn = sqlite3.connect('events.db')
    cursor = update_conn.cursor()

    for event_data in events:
        update_sql = '''
        UPDATE Events
        SET title = ?, category = ?, descriptionFilterHtml = ?, startDate = ?, endDate = ?
        WHERE UID = ?
        '''
        cursor.execute(update_sql, (
            event_data.get('title'),
            event_data.get('category'),
            event_data.get('description'),
            event_data.get('startDate'),
            event_data.get('endDate'),
            event_data['UID']
        ))

        update_conn.commit()
        update_conn.close()

    return JsonResponse({'status': 'success', 'message': 'Events updated successfully'})


def add_or_update_data(request):
    print(request)


def delete_data(request):
    data = json.loads(request.body)
    UIDs = data.get('UIDs', [])
    db_path = os.path.join(settings.BASE_DIR, 'events.db')
    delete_conn = sqlite3.connect(db_path)
    #delete_conn = sqlite3.connect('events.db')
    cursor = delete_conn.cursor()

    for uid in UIDs:
        cursor.execute("DELETE FROM ShowInfo WHERE event_uid=?", (uid,))
        cursor.execute("DELETE FROM Events WHERE UID=?", (uid,))

    delete_conn.commit()
    delete_conn.close()
    return JsonResponse({'status': 'success', 'message': 'Selected events have been deleted successfully'})