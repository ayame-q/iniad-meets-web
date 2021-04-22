from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404, FileResponse
from django.urls import reverse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, ValidationError
from django.utils import html, timezone
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.exceptions import ValidationError as DRFValidationError
import json, re, csv, datetime
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Entry, Circle, UserRole, ChatLog, Status, QuestionResponse
from .serializers import CircleSerializer, CircleEntrySerializer, UserSerializer
from . import forms
import os


# Create your views here.
class CircleListAPIView(ListAPIView):
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer


class CircleInfoAPIView(RetrieveAPIView):
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer


class CircleEntryAPIView(CreateAPIView):
    queryset = Entry.objects.all()
    serializer_class = CircleEntrySerializer

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except ValidationError as e:
            print(e.message)
            raise DRFValidationError(e.message)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class CircleJoinView(CreateView):
    model = Circle
    form_class = forms.CircleJoinForm
    template_name = "meets/circle/join.html"

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        return super(CircleJoinView, self).post(request=request, *args, **kwargs)

    def form_valid(self, form):
        data = form.save()
        data.admin_users.add(self.request.user.role)
        data.staff_users.add(self.request.user.role)
        print(redirect("circle_admin", pk=data.pk))
        return redirect("circle_admin", pk=data.pk)


class CircleListView(ListView):
    model = Circle
    template_name = "meets/circle/list.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.GET.get("pass") == os.environ.get("CIRCLE_LIST_PASSWORD"):
            raise PermissionDenied
        return super(CircleListView, self).dispatch(request=request, *args, **kwargs)


class UserAdminCirclesMixin(LoginRequiredMixin):
    model = Circle
    def get_context_data(self, **kwargs):
        context = super(UserAdminCirclesMixin, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context["admin_circles"] = Circle.objects.all()
        elif self.request.user.role.admin_circles.count():
            context["admin_circles"] = self.request.user.role.admin_circles.all()
        return context


class CircleAdminSinglePageMixin(UserAdminCirclesMixin):
    model = Circle

    def get_queryset(self):
        return self.request.user.role.admin_circles.all()


class CircleAdminListPageMixin(UserAdminCirclesMixin):
    model = Circle

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Circle.objects.all()
        return self.request.user.role.admin_circles.all()
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role.admin_circles.count() <= 0:
                return redirect("circle_join")
            if request.user.role.admin_circles.count() == 1:
                return redirect("./" + str(request.user.role.admin_circles.get().uuid))
        return super(CircleAdminListPageMixin, self).dispatch(request=request, *args, *kwargs)


class CircleAdminGenericListView(CircleAdminListPageMixin, ListView):
    template_name = "meets/circle/admin/list.html"


class CircleAdminMenuView(CircleAdminSinglePageMixin, DetailView):
    template_name = "meets/circle/admin/menu.html"
    extra_context = {
        "movie_form_url": os.environ.get("MOVIE_FORM_URL"),
        "logo_form_url": os.environ.get("LOGO_FORM_URL"),
        "slack_join_url": os.environ.get("SLACK_JOIN_URL")
    }

    def get_context_data(self, **kwargs):
        context = super(CircleAdminMenuView, self).get_context_data(**kwargs)
        if self.request.user.slack_id:
            context["slack"] = True
        else:
            context["slack"] = bool(self.request.user.get_slack_info())
        return context


class CircleAdminInfoView(CircleAdminSinglePageMixin, UpdateView):
    form_class = forms.CircleInfoForm
    template_name = "meets/circle/admin/info.html"

    def get_success_url(self):
        return reverse("circle_admin", kwargs={"pk": self.object.pk})


class CircleAdminMembersView(CircleAdminSinglePageMixin, DetailView):
    template_name = "meets/circle/admin/member.html"

    def post(self, request, *args, **kwargs):
        circle = self.get_object()
        method = request.POST.get("method")

        if method == "add_admin" or method == "add_staff":
            add_emails = re.split("\r?\n", request.POST.get("add_email"))
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
                    self.extra_context["errors"].append(add_email + "は正常なINIADメールアドレスではありません。")

        if method == "remove_admin" or method == "remove_staff":
            remove_pk = request.POST.get("remove_pk")
            if method == "remove_admin":
                target_model = circle.admin_users
            else:
                target_model = circle.staff_users
            target_model.remove(UserRole.objects.get(pk=remove_pk))

        return redirect("circle_admin_members", pk=circle.pk)


class MovieUploadedAPI(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, pk):
        uuid = pk
        try:
            circle = Circle.objects.get(uuid=uuid)
        except Circle.DoesNotExist:
            raise ObjectDoesNotExist
        return Response({"movie_uploaded_at": circle.movie_uploaded_at})

    def post(self, request, pk):
        uuid = pk
        password = request.data.get("password")
        if not password == os.environ.get("MOVIE_UPLOADED_API_PASSWORD"):
            return Response({"error": True})
        try:
            circle = Circle.objects.get(uuid=uuid)
        except Circle.DoesNotExist:
            return Response({"error": True})
        circle.movie_uploaded_at = datetime.datetime.now()
        circle.save()
        return Response({"error": False})


class LogoUploadedAPI(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self, request, pk):
        uuid = pk
        try:
            circle = Circle.objects.get(uuid=uuid)
        except Circle.DoesNotExist:
            raise ObjectDoesNotExist
        return Response({"logo_uploaded_at": circle.logo_uploaded_at})

    def post(self, request, pk):
        uuid = pk
        password = request.data.get("password")
        url = request.data.get("url")
        if not password == os.environ.get("LOGO_UPLOADED_API_PASSWORD"):
            return Response({"error": True})
        try:
            circle = Circle.objects.get(uuid=uuid)
        except Circle.DoesNotExist:
            return Response({"error": True})
        circle.logo_uploaded_at = datetime.datetime.now()
        circle.logo_url = url
        circle.save()
        return Response({"error": False})


class UserIsAuthenticatedAPI(APIView):
    def get(self, request):
        return Response({"is_authenticated": self.request.user.is_authenticated})


class IsSlackJoinedAPI(APIView):
    def get(self, request):
        is_slack_joined = bool(self.request.user.slack_id)
        return Response({"is_slack_joined": is_slack_joined})


class SlackEventAPI(APIView):
    permission_classes = ()
    authentication_classes = ()
    def post(self, request):
        type = request.data.get("type")
        if type == "url_verification":
            challenge = request.data.get("challenge")
            return Response({"challenge": challenge})
        if type == "team_join":
            email = request.data["user"]["profile"]["email"]
            try:
                user = User.objects.get(email=email)
                user.get_slack_info()
            except User.DoesNotExist:
                pass
            return Response({"request": "ok"})


def sns_share_image(request, uuid):
    user = get_object_or_404(User, uuid=uuid)

    question_count = QuestionResponse.objects.filter(user=user, selection__question__type=1).count()
    correct_count = QuestionResponse.objects.filter(user=user, selection__question__type=1, selection__is_correct=True).count()

    from .shareimage import make_share_image
    img = make_share_image(correct_count, question_count)
    response = HttpResponse(content_type="image/jpeg")
    img.save(response, "JPEG")
    return response


# Old views
def app(request):
    if datetime.datetime.now() < datetime.datetime.fromtimestamp(1590397200) and not request.user.is_superuser:
        return render(request, "meets/pre.html")
    if not request.user.is_authenticated:
        return render(request, "meets/top.html")
    circles = Circle.objects.order_by("id")
    my_entries = Entry.objects.filter(user=request.user).order_by("id")
    my_questions = ChatLog.objects.filter(send_user=request.user, receiver_circle__isnull=False).order_by("id")

    if request.user.role:
        staff_circles = Circle.objects.filter(staff_users=request.user.role).order_by("id")
    else:
        staff_circles = None

    if request.user.is_superuser or request.user.role and request.user.role.admin_circles.count():
        has_admin_circle = True
    else:
        has_admin_circle = False

    result = {"circles": circles, "my_entries": my_entries, "staff_circles": staff_circles, "has_admin_circle": has_admin_circle, "my_questions": my_questions}
    status = Status.objects.get(pk=1)
    if status.status == 2:
        return render(request, "meets/after.html", result)
    return render(request, "meets/app.html", result)

def is_url(s, allowed_blank=False):
    if allowed_blank:
        return not s or bool(re.match("https?://[\w/:%#$&?()~.=+\-]+", str(s)))
    return bool(re.match("https?://[\w/:%#$&?()~.=+\-]+", str(s)))


def circle_admin_list(request):
    if not request.user.is_authenticated:
        return redirect("/auth/google/login/?next=/circle_admin")
    if request.user.is_superuser:
        admin_circles = Circle.objects.order_by("id")
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
        admin_circles = Circle.objects.order_by("id")
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
        if method == "edit_info":
            circle.is_using_entry_form = bool(request.POST.get("is_using_entry_form"))
            circle.entry_form_url = request.POST.get("entry_form_url")
            circle.panflet_url = request.POST.get("panflet_url")
            circle.website_url = request.POST.get("website_url")
            circle.twitter_sn = html.escape(request.POST.get("twitter_sn"))
            circle_comment = html.escape(request.POST.get("circle_comment"))
            if not(len(circle_comment) <= 120 and len(circle_comment.splitlines()) <= 3):
                result["errors"].append("一言説明は改行3回以内で、120文字以内でお願いします。")
            elif not (is_url(circle.entry_form_url, True) and is_url(circle.panflet_url, True) and is_url(circle.website_url, True)):
                result["errors"].append("URLがおかしいです")
            elif not circle.is_using_entry_form and not is_url(circle.entry_form_url):
                result["errors"].append("内部エントリーフォームを利用しない場合は外部フォームへのURLを指定してください")
            else:
                circle.comment = circle_comment
                circle.save()

        if method == "add_admin" or method == "add_staff":
            add_emails = re.split("\r?\n", request.POST.get("add_email"))
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


def circle_admin_entry_csv(request, pk):
    try:
        if request.user.is_superuser:
            circle = Circle.objects.get(pk=pk)
        else:
            circle = Circle.objects.filter(admin_users=request.user.role).get(pk=pk)
    except Circle.DoesNotExist:
        raise PermissionDenied
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="circle-entry.csv"'

    writer = csv.writer(response)
    writer.writerow(["学籍番号", "名前", "メールアドレス", "申込日時"])
    for entry in circle.entries.all():
        writer.writerow([entry.user.student_id, entry.user.name, entry.user.email, "{0:%Y-%m-%d %H:%M:%S}".format(entry.created_at)])

    return response


def system_admin(request):
    if request.user.is_superuser:
        return render(request, "meets/system-admin.html")
    raise PermissionDenied


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
    new_name = html.escape(request.POST.get("name"))
    request.user.name = new_name
    request.user.save()
    result = {"success": True, "error": None, "name": request.user.name}
    return JsonResponse(result)


def api_user_display_name_update(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "No data"})
    new_name = html.escape(request.POST.get("name"))
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
        if not circle.is_using_entry_form:
            return JsonResponse({"success": False, "error": "そのサークルはエントリーフォームを利用していません"})
        if Entry.objects.filter(user=request.user, circle=circle).count() == 0:
            new_entry = Entry(user=request.user, circle=circle)
            new_entry.save()
        else:
            return JsonResponse({"success": False, "error": circle.name + "には、すでに入会申込済みです"})
        my_entries = Entry.objects.filter(user=request.user)
        entry_circles = [{"id": entry.circle.id, "name": entry.circle.name} for entry in my_entries]
        result = {"success": True, "error": None, "entered_circle_name": circle.name ,"entry_circles": entry_circles}
        return JsonResponse(result)
    except Circle.DoesNotExist:
        return JsonResponse({"success": False, "error": "サークルが見つかりません"})


def api_get_my_questions(request):
    get_questions = ChatLog.objects.filter(send_user=request.user, receiver_circle__isnull=False).order_by("created_at")
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
                "sender_circle_pk": reply.sender_circle.pk,
                "sender_circle_name": reply.sender_circle.name,
                "created_at": "{0:%Y-%m-%d %H:%M:%S}".format(reply.created_at),
            } for reply in question.replies.all()],
            "send_user": {"display_name": question.send_user.display_name, "class": question.send_user.get_class()} if not question.is_anonymous else {"display_name": "匿名", "class": question.send_user.get_class()}
        }
        for question in get_questions
    ]
    return JsonResponse({"success": True, "error": None, "questions": result})


def api_get_staff_questions(request):
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


def get_status():
    circles = Circle.objects.all()
    status = Status.objects.get(pk=1)
    event_start_time = status.planning_start_time if status.status == 0 else status.started_time
    circle_list = {}
    for circle in circles:
        circle_list[circle.id] = {
            "id": circle.id,
            "name": circle.name,
            "is_using_entry_form": circle.is_using_entry_form,
            "start_time_str": "{0:%H:%M}".format(timezone.localtime(event_start_time + datetime.timedelta(seconds=circle.start_time_sec))) if circle.start_time_sec else None,
            "start_time_ts": int((event_start_time + datetime.timedelta(seconds=circle.start_time_sec)).timestamp() * 1000) if circle.start_time_sec else None,
            "video_time_sec": circle.start_time_sec if circle.start_time_sec else None,
            "entry_form_url": circle.entry_form_url,
            "panflet_url": circle.panflet_url,
            "website_url": circle.website_url,
            "twitter_sn": circle.twitter_sn,
            "comment": circle.comment,
        }
    result = {
        "status": status.status,
        "circle_list": circle_list
    }
    return result


def api_get_status(request):
    return JsonResponse(get_status())
