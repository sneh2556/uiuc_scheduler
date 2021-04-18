# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Sum, Avg, Func
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Gpa, Rating, RegularCourse, friendRequest, friendships
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .generator import *
import json
from django.core import serializers
from .forms import RegisterForm
from django.contrib import messages
from django.db import connection

class Round(Func):
    function = 'ROUND'
    arity = 2

@login_required
def view_friend_schedules(request):
    user_id = request.user.id
    cursor = connection.cursor()

    cursor.execute('SELECT MAX(schedule_id), GROUP_CONCAT(crn), MAX(term), MAX(year), Friends.first_name, Friends.last_name FROM schedule JOIN (SELECT first_name, last_name, id FROM (SELECT first_name, last_name, id FROM auth_user) as A JOIN (SELECT friend_two_id FROM friendships WHERE friend_one_id = %s) as B ON A.id = B.friend_two_id) as Friends ON Friends.id = schedule.user_id GROUP BY Friends.first_name, Friends.last_name, schedule_id;',  [user_id])
    results = set(cursor.fetchall())

    cursor.execute('SELECT MAX(schedule_id), GROUP_CONCAT(crn), MAX(term), MAX(year), Friends.first_name, Friends.last_name FROM schedule JOIN (SELECT first_name, last_name, id FROM (SELECT first_name, last_name, id FROM auth_user) as A JOIN (SELECT friend_one_id FROM friendships WHERE friend_two_id = %s) as B ON A.id = B.friend_one_id) as Friends ON Friends.id = schedule.user_id GROUP BY Friends.first_name, Friends.last_name, schedule_id;',  [user_id])
    results.update(cursor.fetchall())

    return render(request, 'view_friend_schedules.html', {'results' : list(results)})

@login_required
def follow(request):
    user_id = request.user.id
    friend_id = request.POST.get('id')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO following (follower_id, following_id) VALUES (%s, %s);', [user_id, friend_id])
    return HttpResponse('Follow Successful!')

@login_required
def unfollow(request):
    user_id = request.user.id
    friend_id = request.POST.get('id')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM following WHERE follower_id = %s AND following_id = %s;', [user_id, friend_id])
    return HttpResponse('Unfollow Successful!')

@login_required
def unsave_schedule(request):
    schedule_id = int(request.POST.get('schedule_id'))
    user_id = request.user.id
    cursor = connection.cursor()
    cursor.execute('DELETE FROM schedule WHERE user_id=%s AND schedule_id=%s;', [user_id, schedule_id])
    return redirect('/view_saved_schedules/')

@login_required
def view_saved_schedules(request):
    cursor = connection.cursor()
    user_id = request.user.id

    cursor.execute('SELECT MAX(schedule_id), GROUP_CONCAT(crn), MAX(term), MAX(year) FROM schedule WHERE user_id=%s GROUP BY schedule_id',  [user_id])
    results = cursor.fetchall()

    return render(request, 'view_saved_schedules.html', {'results' : results})

@login_required
def save_schedule(request):
    cursor = connection.cursor()
    user_id = request.user.id

    if user_id:
        cursor.execute("SELECT MAX(schedule_id) FROM schedule WHERE user_id = %s;", [user_id])
        schedule_id = cursor.fetchall()[0][0]
        new_schedule_id = 1
        if schedule_id != None:
            new_schedule_id = int(schedule_id) + 1

        combination = request.POST.get('combination')
        final = json.loads(combination)
        for section in final:
            crn = int(section['fields']['crn'])
            term = section['fields']['term']
            year = section['fields']['year']
            cursor.execute("INSERT INTO schedule(user_id, schedule_id, crn, term, year) VALUES(%s, %s, %s, %s, %s)", [user_id, new_schedule_id, crn, term, year])

        return HttpResponse('Schedule Saved!')
    else:
        return HttpResponse('Please Login First To Save Schedules!')

@login_required
def view_friends(request):
    cursor = connection.cursor()
    user_id = request.user.id

    cursor.execute("SELECT first_name, last_name, id, temp.following_id FROM auth_user JOIN (SELECT friend_two_id, following_id FROM friendships LEFT OUTER JOIN following ON follower_id = friend_one_id AND following_id = friend_two_id WHERE friend_one_id = %s) as temp ON id = temp.friend_two_id;", [user_id])
    friends = set(cursor.fetchall())
    cursor.execute("SELECT first_name, last_name, id, temp.following_id FROM auth_user JOIN (SELECT friend_one_id, following_id FROM friendships LEFT OUTER JOIN following ON follower_id = friend_two_id AND following_id = friend_one_id WHERE friend_two_id = %s) as temp ON id = temp.friend_one_id;", [user_id])
    temp = set(cursor.fetchall())
    friends.update(temp)

    cursor.execute("SELECT first_name, last_name, id FROM auth_user JOIN (SELECT receiver_id FROM friend_requests WHERE sender_id = %s) as temp ON temp.receiver_id = id;", [user_id])
    sent_requests = set(cursor.fetchall())
    cursor.execute("SELECT first_name, last_name, id FROM auth_user JOIN (SELECT sender_id FROM friend_requests WHERE receiver_id = %s) as temp ON temp.sender_id = id;", [user_id])
    received_requests = set(cursor.fetchall())

    context = {
        'friends': friends,
        'sent': sent_requests,
        'received': received_requests
    }
    
    return render(request, 'view_friends.html', context)

@login_required
def add_friend(request):
    cursor = connection.cursor()
    sender = request.user.id
    receiver = request.POST.get('id')
    cursor.execute("INSERT INTO friend_requests(sender_id, receiver_id) VALUES(%s, %s);", [sender, receiver])
    return HttpResponse('Done')

@login_required
def accept_request(request):
    cursor = connection.cursor()
    one = request.user.id
    two = request.POST.get('id')
    cursor.execute("INSERT INTO friendships(friend_one_id, friend_two_id) VALUES(%s, %s);", [one, two])
    cursor.execute("DELETE FROM friend_requests WHERE sender_id = %s AND receiver_id = %s", [two, one])
    return HttpResponse('Done')

@login_required
def unfriend(request):
    cursor = connection.cursor()
    one = request.user.id
    two = request.POST.get('id')
    cursor.execute("DELETE FROM friendships WHERE (friend_one_id = %s AND friend_two_id = %s) OR (friend_one_id = %s AND friend_two_id = %s);", [one, two, two, one])
    cursor.execute("DELETE FROM following WHERE follower_id = %s AND following_id = %s;", [one, two])
    return HttpResponse('Done')

@login_required
def cancel_request(request):
    cursor = connection.cursor()
    sender = request.user.id
    receiver = request.POST.get('id')
    cursor.execute("DELETE FROM friend_requests WHERE sender_id = %s AND receiver_id = %s", [sender, receiver])
    return HttpResponse('Done')

@login_required
def search_people(request):
    name = request.POST.get("searchName")
    names = name.split()
    length = len(names)

    cursor = connection.cursor() 
    user_id = request.user.id

    cursor.execute("SELECT friend_two_id FROM friendships WHERE friend_one_id = %s;", [user_id])
    friends = set(cursor.fetchall())
    cursor.execute("SELECT friend_one_id FROM friendships WHERE friend_two_id = %s;", [user_id])
    temp = set(cursor.fetchall())
    friends.update(temp)
    #print(friends)

    cursor.execute("SELECT receiver_id FROM friend_requests WHERE sender_id = %s;", [user_id])
    sent_requests = set(cursor.fetchall())
    cursor.execute("SELECT sender_id FROM friend_requests WHERE receiver_id = %s;", [user_id])
    received_requests = set(cursor.fetchall())

    if length == 0:
        query = "SELECT id, first_name, last_name FROM auth_user WHERE id <> %s  AND is_staff = 0;"

    elif length == 1:
        query = "SELECT id, first_name, last_name FROM auth_user WHERE id <> %s  AND is_staff = 0 AND (first_name LIKE '%%" + names[0] + "%%' OR last_name  LIKE '%%" + names[0] + "%%');"

    else:
        import string
        remove = string.punctuation
        
        for i in range(length):
            names[i] = ''.join(x for x in names[i] if x not in remove)

        #print(names)

        query = "SELECT id, first_name, last_name FROM auth_user WHERE id <> %s AND (first_name LIKE '%%" + names[0] + "%%' "

        for i in range(1, length):
            temp = "OR first_name LIKE '%%" + names[i] + "%%' "
            query += temp
        
        query += ") AND (last_name LIKE '%%" + names[0] + "%%' "

        for i in range(1, length):
            temp = "OR last_name LIKE '%%" + names[i] + "%%' "
            query += temp
            
        query += ") AND is_staff = 0;"
    
    #print(query)
    cursor.execute(query, [user_id])
    all = list(cursor.fetchall())
    results = []

    for one in all:
        if (one[0],) in friends:
            results.append([one[1], one[2], 'Unfriend', one[0]])
        elif (one[0],) in sent_requests:
            results.append([one[1], one[2], 'Cancel Request', one[0]])
        elif (one[0],) in received_requests:
            results.append([one[1], one[2], 'Accept', one[0]])
        else:
            results.append([one[1], one[2], 'Add Friend', one[0]])

    context = {
        'results': results
    }

    return render(request, "search_people_results.html", context)

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("/home")
    else:
        form = RegisterForm()
    #for f in form:
    #    print(f.help_text)
    return render(response, "registration/register.html", {"form":form})

def home_view(request):
    return render(request, "index.html", {})

def search_view(request):
    return render(request, "search.html", {})

def get_avg_gpa(request):
    #name = request.POST.get("prof_name")
    subject = request.POST.get("subjects")
    number = int(request.POST.get("number"))
    results = Gpa.objects.raw("SELECT COUNT(ID) as ID, PrimaryInstructor, CONVERT(AVG(avgGpa), DECIMAL(65,2)) as avgGPA, SUM(A) as sumA, SUM(B) as sumB, SUM(C) as sumC, SUM(D) as sumD, SUM(F) as sumF FROM gpa WHERE Subject = %s and Number = %s GROUP BY PrimaryInstructor", [subject, number])
    #results = Gpa.objects.filter(subject=subject, number=number).values('primaryinstructor').annotate(Avg('avggpa'), Sum('a'), Sum('b'), Sum('c'), Sum('d'), Sum('f'))
    context = {
        'results': results
    }

    return render(request, "display_avg_gpa.html", context)

def search_geneds(request):
    if request.method == "POST":
        year = request.POST.get('year')
        term = request.POST.get('term')
        category = '%' + request.POST.get('category') + '%'
        subcategory= '%' + request.POST.get('subcategory') + '%'
        filter1 = request.POST.get('filter-1')
        filter2 = request.POST.get('filter-2')

        cursor = connection.cursor()
    
        # default
        query = "SELECT gpa.Subject as subject, gpa.Number as number, CONVERT(AVG(gpa.avgGpa), DECIMAL(65, 2)) as avg, SUM(gpa.Total) as total FROM gpa JOIN (SELECT Subject, Number FROM regular_courses NATURAL JOIN (SELECT * FROM gen_eds WHERE DegreeAttributes LIKE %s AND DegreeAttributes LIKE %s) as one GROUP BY Subject, Number) as two ON gpa.Subject = two.Subject AND gpa.Number = two.Number GROUP BY gpa.Subject, gpa.Number ORDER BY avg DESC, total DESC;"
        
        if filter1 == 'total':
            if filter2 == 'avg':
                query = "SELECT gpa.Subject as subject, gpa.Number as number, CONVERT(AVG(gpa.avgGpa), DECIMAL(65, 2)) as avg, SUM(gpa.Total) as total FROM gpa JOIN (SELECT Subject, Number FROM regular_courses NATURAL JOIN (SELECT * FROM gen_eds WHERE DegreeAttributes LIKE %s AND DegreeAttributes LIKE %s) as one GROUP BY Subject, Number) as two ON gpa.Subject = two.Subject AND gpa.Number = two.Number GROUP BY gpa.Subject, gpa.Number ORDER BY total DESC, avg DESC;"
            else:
                query = "SELECT gpa.Subject as subject, gpa.Number as number, CONVERT(AVG(gpa.avgGpa), DECIMAL(65, 2)) as avg, SUM(gpa.Total) as total FROM gpa JOIN (SELECT Subject, Number FROM regular_courses NATURAL JOIN (SELECT * FROM gen_eds WHERE DegreeAttributes LIKE %s AND DegreeAttributes LIKE %s) as one GROUP BY Subject, Number) as two ON gpa.Subject = two.Subject AND gpa.Number = two.Number GROUP BY gpa.Subject, gpa.Number ORDER BY total DESC;"
        else:
            if filter2 == 'avg':
                query = "SELECT gpa.Subject as subject, gpa.Number as number, CONVERT(AVG(gpa.avgGpa), DECIMAL(65, 2)) as avg, SUM(gpa.Total) as total FROM gpa JOIN (SELECT Subject, Number FROM regular_courses NATURAL JOIN (SELECT * FROM gen_eds WHERE DegreeAttributes LIKE %s AND DegreeAttributes LIKE %s) as one GROUP BY Subject, Number) as two ON gpa.Subject = two.Subject AND gpa.Number = two.Number GROUP BY gpa.Subject, gpa.Number ORDER BY avg DESC;"


        cursor.execute(query, [category, subcategory])

        results = cursor.fetchall()
        return render(request, "display_geneds.html", {'results': results})

    return render(request, "search_geneds.html", {})

def add_rating_view(request):
    if request.method == "POST":
        subject = request.POST.get("subjects")
        prof_name = request.POST.get("profs")
        rating = (request.POST.get("ratng"))
        description = request.POST.get("description")

        user_id = request.user.id;

        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("INSERT INTO ratings(professor_name, subject, rating, description, writer_id) VALUES(%s, %s, %s, %s, %s)", [prof_name, subject, rating, description, user_id])

        messages.success(request, 'Rating Added Successfully!') 
        return redirect('/insert/')
    else:
        return render(request, "insert.html", {})

@login_required
def delete_my_ratings_view(request):
    user_id = request.user.id;
    ratings = Rating.objects.raw("SELECT * FROM ratings WHERE writer_id = %s", [user_id])

    #print(ratings)
    if len(list(ratings)) == 0:
        return HttpResponse("<h1> You Have Not Rated Any Professor! </h1>")

    context = {
        'ratings': ratings
    }

    return render(request, "delete_my_ratings.html", context)

@login_required
def update_my_ratings_view(request):
    user_id = request.user.id;

    ratings = Rating.objects.raw("SELECT * FROM ratings WHERE writer_id = %s", [user_id])

    context = {
        'ratings': ratings
    }

    return render(request, "update_my_ratings.html", context)

@login_required
def delete_rating(request):
    r_ids = request.POST.getlist("delete_update")
    user_id = request.user.id;

    cursor = connection.cursor()

    if len(r_ids) == 0:
        return HttpResponse("<h1> Need to Select At Least One Entry! </h1>")

    for id in r_ids:
        id = int(id)
        cursor.execute("DELETE FROM ratings WHERE writer_id = %s and id = %s", [user_id, id])

    return HttpResponse("<h1> Deleted Successfully! </h1>")

@login_required
def update_rating(request):
    r_ids = request.POST.getlist("delete_update")
    user_id = request.user.id;

    from django.db import connection
    cursor = connection.cursor()

    for id in r_ids:
        prof = request.POST.get(id+'_name')
        subject = request.POST.get(id+'_subject')
        rating = request.POST.get(id+'_rating')
        description = request.POST.get(id+'_description')
        cursor.execute("UPDATE ratings SET professor_name=%s, rating=%s, description=%s, subject=%s WHERE id = %s", [prof, rating, description, subject, id])

    return redirect('/update_my_ratings/')

def generate_schedule_select_term_view(request):
    return render(request, "generate_schedule_select_term.html", {})

def generate_schedule_view(request):
    year = request.POST.get('year')
    term = request.POST.get('sem')
    courses = RegularCourse.objects.raw("SELECT DISTINCT 1 as CRN, Subject, Number FROM regular_courses WHERE Year=%s AND Term=%s ORDER BY Number", [year, term])
    context = {
        'courses': courses,
        'year': year,
        'sem': term
    }
    return render(request, "generate_schedule.html", context)

def generate_schedule(request):
    year = request.POST.get('year')
    term = request.POST.get('sem')
    courses = request.POST.getlist('list[]')
    days = request.POST.getlist('weekday')

    results, gpas, courses, profs = schedule_generator(courses, days, year, term)

    json_results = []
    #serialized_results = serializers.serialize('json', results)
    for result in results:
        c_objects = serializers.serialize('json', result)
        json_results.append(c_objects)

    #print(json_results)
    json_gpas = []
    json_courses = []
    json_profs = []
    for g in gpas:
        g = str(round(g, 2))
        g = float(g)
        gpa = {}
        gpa = g
        json_gpas.append(gpa)
    for c in courses:
        course = {}
        course = c
        json_courses.append(course)
    for p in profs:
        prof = {}
        prof = c
        json_profs.append(prof)
    #json_gpas = json.dumps(json_gpas)
    #json_courses = json.dumps(json_courses)

    data = {'combinations': json_results, 'gpas': json_gpas, 'courses' : courses, 'profs' : profs}
    mimetype = 'application/json'

    return HttpResponse(json.dumps(data), mimetype)

def render_schedule(request):
    combination = request.POST.get('combination')
    schno = request.POST.get('schedule_number')
    #print(combination)
    if request.POST.get('saved'):
        term = request.POST.get('term')
        year = request.POST.get('year')
        result = []
        crns = combination.split(',')
        open = '%Open%'
        for crn in crns:
            section = RegularCourse.objects.raw("SELECT id, CRN, Type, Instructors, Days, StartTime, EndTime FROM regular_courses WHERE CRN=%s AND Year=%s AND Term=%s AND EnrollmentStatus LIKE %s", [crn, year, term, open])[0]
            result.append(section)
        print(result)
        c_objects = serializers.serialize('json', result)
        context = {
            'combination' : c_objects,
            'schedule_number' : schno
        }
        return render(request, "schedule.html", context)

    context = {
        'combination' : combination,
        'schedule_number' : schno
    }
    return render(request, "schedule.html", context)

def get_prof_ratings(request):
    return render(request, "get_prof_ratings.html", {})

def display_prof_ratings(request):
    subject = request.POST.get("subjects")
    prof = request.POST.get("profs")

    ratings = Rating.objects.raw("SELECT * FROM ratings WHERE subject=%s AND professor_name=%s", [subject, prof])
    info = Rating.objects.raw("SELECT COUNT(id) as id, AVG(rating) as avgR FROM ratings WHERE subject=%s AND professor_name=%s GROUP BY professor_name", [subject, prof])

    context = {
        'ratings' : ratings,
        'subject' : subject,
        'prof_name' : prof,
        'avg' : info[0].avgR,
        'total' : info[0].id
    }
    return render(request, "display_prof_ratings.html", context)

def get_profs(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        q = '%' + q + '%'
        #profs = Gpa.objects.filter(primaryinstructor__icontains=q).values('primaryinstructor').distinct()
        profs = Gpa.objects.raw("SELECT DISTINCT COUNT(ID) as ID, PrimaryInstructor from gpa WHERE PrimaryInstructor LIKE %s GROUP BY PrimaryInstructor", [q])

        results = []
        for p in profs:
            prof_json = {}
            prof_json = p.primaryinstructor
            results.append(prof_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def get_subjects(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        q = '%' + q + '%'
        #subjects = Gpa.objects.filter(subject__icontains=q).values('subject').distinct()
        subjects = Gpa.objects.raw("SELECT DISTINCT COUNT(ID) as ID, Subject from gpa WHERE Subject LIKE %s GROUP BY Subject", [q])
        results = []
        for s in subjects:
            subject_json = {}
            subject_json = s.subject
            results.append(subject_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@csrf_exempt
def get_numbers(request):
    subject = request.POST.get('subject')
    year = request.POST.get('year')
    sem = request.POST.get('sem')

    nums = RegularCourse.objects.raw("SELECT DISTINCT COUNT(id) as id, Number from regular_courses WHERE Year=%s AND Term=%s AND Subject=%s GROUP BY Number ORDER BY Number", [year, sem, subject])

    results = []
    for n in nums:
        number_json = {}
        number_json = n.number
        results.append(number_json)
    data = json.dumps(results)
    mimetype = 'application/json'

    return HttpResponse(data, mimetype)
