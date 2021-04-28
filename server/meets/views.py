from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404, FileResponse
from django.urls import reverse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, ValidationError
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.exceptions import ValidationError as DRFValidationError
import json, re, csv, datetime, os
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Entry, Circle, UserRole, QuestionResponse, Status
from .serializers import CircleSerializer, CircleEntrySerializer, UserSerializer
from . import forms


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

    def perform_update(self, serializer):
        data = self.request.data
        if data.get("display_name"):
            serializer.save(is_display_name_initialized=True)
        serializer.save()



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
        context["status"] = Status.objects.get()
        if self.request.user.is_superuser:
            context["admin_circles"] = Circle.objects.all()
        elif self.request.user.role.admin_circles.count():
            context["admin_circles"] = self.request.user.role.admin_circles.all()
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Circle.objects.all()
        return self.request.user.role.admin_circles.all()


class CircleAdminSinglePageMixin(UserAdminCirclesMixin):
    model = Circle


class CircleAdminListPageMixin(UserAdminCirclesMixin):
    model = Circle
    
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


class CircleAdminPamphletView(CircleAdminSinglePageMixin, UpdateView):
    form_class = forms.CirclePamphletForm
    template_name = "meets/circle/admin/pamphlet.html"

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


class CircleAdminEntriesView(CircleAdminSinglePageMixin, DetailView):
    template_name = "meets/circle/admin/entries.html"


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
        circle.movie_uploaded_at = timezone.localtime()
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
        circle.logo_uploaded_at = timezone.localtime()
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


class SnsShareView(DetailView):
    model = User
    template_name = "meets/share.html"
    extra_context = {"site_host": os.environ.get("SITE_HOST") if os.environ.get("SITE_HOST")[-1] != "/" else os.environ.get("SITE_HOST")[0:-1]}


def sns_share_image(request, uuid):
    user = get_object_or_404(User, uuid=uuid)

    from .shareimage import make_share_image
    img = make_share_image(user.get_correct_count(), user.get_question_count())
    response = HttpResponse(content_type="image/jpeg")
    img.save(response, "JPEG")
    return response


def circle_admin_entries_csv(request, pk):
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
    writer.writerow(["学籍番号", "名前", "フリガナ", "メールアドレス", "受付日時"])
    for entry in circle.entries.all():
        writer.writerow([entry.user.student_id, entry.user.get_name(), entry.user.get_name_ruby(), entry.user.email, "{0:%Y-%m-%d %H:%M:%S}".format(entry.created_at)])

    return response


class IsOpenAPIView(APIView):
    def get(self, request):
        status = Status.objects.get()
        is_open = False
        if status.status != 0 and status.opening_time < timezone.localtime():
            is_open = True
        return JsonResponse({"is_open": is_open})


class StatusAPIView(APIView):
    def get(self, request):
        status = Status.objects.get()
        return JsonResponse({
            "status": status.status,
            "movie_url": status.streaming_url if status.status != 2 else status.archive_url
        })
