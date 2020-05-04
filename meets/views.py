from django.shortcuts import render, redirect
from django.http import JsonResponse
import json, re
from .models import Entry, Circle, UserRole, ChatLog

# Create your views here.
def pre(request):
    return render(request, "meets/pre.html")


def app(request):
    if not request.user.is_authenticated:
        return render(request, "meets/top.html")
    circles = Circle.objects.all()
    my_entries = Entry.objects.filter(user=request.user)
    get_questions = None
    if request.user.role:
        staff_circles = Circle.objects.filter(staff_users=request.user.role)
        if staff_circles:
            get_questions = ChatLog.objects.filter(receiver_circle__in=staff_circles).order_by("-created_at")
    else:
        staff_circles = None

    if request.user.is_superuser or request.user.role.admin_circles.count():
        has_admin_circle = True
    else:
        has_admin_circle = False

    result = {"circles": circles, "my_entries": my_entries, "staff_circles": staff_circles, "has_admin_circle": has_admin_circle, "get_questions": get_questions}
    return render(request, "meets/app.html", result)


def circle_admin_list(request):
    if request.user.is_superuser:
        admin_circles = Circle.objects.all()
    elif request.user.role.admin_circles.count():
        admin_circles = request.user.role.admin_circles.all()
    else:
        return render(request, "meets/circle-admin.html", {"is_permitted": False})
    result = {
        "is_permitted": True,
        "admin_circles": admin_circles
    }
    return render(request, "meets/circle-admin.html", result)


def circle_admin_page(request, pk):
    if request.user.is_superuser:
        admin_circles = Circle.objects.all()
    elif request.user.role.admin_circles.count():
        admin_circles = request.user.role.admin_circles.all()
    else:
        return render(request, "meets/circle-admin.html", {"is_permitted": False})
    if not request.user.is_superuser:
        if not request.user.role.admin_circles.filter(pk=pk).count():
            return render(request, "meets/circle-admin.html", {"is_permitted": False})
    circle = Circle.objects.get(pk=pk)
    result = {"errors": []}
    if request.method == "POST":
        method = request.POST.get("method")
        if method == "add_admin" or method == "add_staff":
            add_emails = request.POST.get("add_email").split("\n")
            target_model = None
            if method == "add_admin":
                target_model = circle.admin_users
            else:
                target_model = circle.staff_users
            for add_email in add_emails:
                if re.match(r"s1f10[0-9]{7}@iniad\.org", add_email):
                    user_role = None
                    try:
                        user_role = UserRole.objects.get(email=add_email)
                    except UserRole.DoesNotExist:
                        user_role = UserRole(email=add_email)
                        user_role.save()
                    target_model.add(user_role)
                else:
                    result["errors"].append(add_email + "は正常なINIADメールアドレスではありません。")

        if method == "remove_admin" or method == "remove_staff":
            remove_pk = request.POST.get("remove_pk")
            if method == "remove_admin":
                target_model = circle.admin_users
            else:
                target_model = circle.staff_users
            target_model.remove(UserRole.objects.get(pk=remove_pk))

    result.update({
        "is_permitted": True,
        "admin_circles": admin_circles,
        "circle": circle
    })
    return render(request, "meets/circle-admin.html", result)


def api_admin_users_add(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "No data"})
    data = json.loads(request.body)
    circle_pk = data["circle_pk"]
    emails = data["emails"]
    circle = Circle.objects.get(pk=circle_pk)
    if not request.user.is_superuser:
        try:
            circle.admin_users.get(pk=request.user.pk)
        except circle.admin_users.DoesNotExist:
            return JsonResponse({"success": False, "error": "No Permission"})
    for email in emails:
        user_role = None
        try:
            user_role = UserRole.objects.get(email=email)
        except UserRole.DoesNotExist:
            user_role = UserRole(email=email)
        circle.admin_users.add(user_role)
    result = {"success": True, "error": None, "circle_id": circle.id, "admin_users": circle.admin_users}
    return JsonResponse(result)


def api_staff_users_add(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "No data"})
    data = json.loads(request.body)
    circle_pk = data["circle_pk"]
    emails = data["emails"]
    circle = Circle.objects.get(pk=circle_pk)
    if not request.user.is_superuser:
        try:
            circle.admin_users.get(pk=request.user.pk)
        except circle.admin_users.DoesNotExist:
            return JsonResponse({"success": False, "error": "No Permission"})
    for email in emails:
        user_role = None
        try:
            user_role = UserRole.objects.get(email=email)
        except UserRole.DoesNotExist:
            user_role = UserRole(email=email)
        circle.staff_users.add(user_role)
    result = {"success": True, "error": None, "circle_id": circle.id, "staff_users": circle.admin_users}
    return JsonResponse(result)


def api_user_name_update(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "No data"})
    new_name = request.POST.get("name")
    request.user.name = new_name
    request.user.save()
    result = {"success": True, "error": None, "name": request.user.name}
    return JsonResponse(result)


def api_user_display_name_update(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "No data"})
    new_name = request.POST.get("name")
    request.user.display_name = new_name
    request.user.is_display_name_initialized = True
    request.user.save()
    result = {"success": True, "error": None, "name": request.user.display_name}
    return JsonResponse(result)


def api_entry(request, pk):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "No data"})
    if not request.user.name:
        return JsonResponse({"success": False, "error": "No name"})
    if not request.user.is_student:
        return JsonResponse({"success": False, "error": "No student"})

    try:
        circle = Circle.objects.get(pk=pk)
        if Entry.objects.filter(user=request.user, circle=circle).count() == 0:
            new_entry = Entry(user=request.user, circle=circle)
            new_entry.save()
        my_entries = Entry.objects.filter(user=request.user)
        entry_circles = [{"id": entry.circle.id, "name": entry.circle.name} for entry in my_entries]
        result = {"success": True, "error": None, "entry_circles": entry_circles}
        return JsonResponse(result)
    except Circle.DoesNotExist:
        return JsonResponse({"success": False, "error": "サークルが見つかりません"})

def api_get_questions(request):
    if request.user.role:
        staff_circles = Circle.objects.filter(staff_users=request.user.role)
        if staff_circles:
            get_questions = ChatLog.objects.filter(receiver_circle__in=staff_circles).order_by("created_at")
            result = [
                {
                    "id": question.id,
                    "comment": question.comment,
                    "receiver_circle_pk": question.receiver_circle.pk if question.receiver_circle else None,
                    "receiver_circle_name": question.receiver_circle.name if question.receiver_circle else None,
                    "is_anonymous": question.is_anonymous,
                    "created_at": "{0:%Y-%m-%d %H:%M:%S}".format(question.created_at),
                    "replies": [{
                        "id": reply.id,
                        "parent_pk": question.id,
                        "comment": reply.comment,
                        "send_user": {"display_name": reply.send_user.display_name, "class": reply.send_user.get_class()},
                        "created_at": "{0:%Y-%m-%d %H:%M:%S}".format(reply.created_at),
                    } for reply in question.replies.all()],
                    "send_user": {"display_name": question.send_user.display_name, "class": question.send_user.get_class()} if not question.is_anonymous else {"display_name": "匿名", "class": question.send_user.get_class()}
                }
                for question in get_questions
            ]
            return JsonResponse({"success": True, "error": None, "questions": result})
        else:
            return JsonResponse({"success": False, "error": "サークルのスタッフではありません"})
    else:
        return JsonResponse({"success": False, "error": "学生ではありません"})
