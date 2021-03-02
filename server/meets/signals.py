from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added, social_account_updated, social_account_removed
from allauth.socialaccount.models import SocialAccount, SocialToken
from .models import User, UserRole
import re

@receiver(user_signed_up)
def signed_up(user, **kwargs):
    social_info = SocialAccount.objects.filter(user=user)[0]
    social_token = SocialToken.objects.filter(account=social_info)[0]
    if social_info.provider == "google":
        user.display_name = social_info.extra_data["name"]
        if social_info.extra_data["hd"] == "iniad.org":
            match = re.match(r"s1f10(([0-9]{2})[0-9]{4})[0-9]{1}@iniad\.org", social_info.extra_data["email"])
            if(match):
                user.entry_year = int(match.group(2)) + 2000
                user.is_student = True  # 学生
                user.student_id = "1F10" + match.group(1)
                try:
                    user_role = UserRole.objects.get(email=social_info.extra_data["email"])
                    user.role = user_role
                except UserRole.DoesNotExist:
                    new_user_role = UserRole(email=social_info.extra_data["email"])
                    new_user_role.save()
                    user.role = new_user_role
            else:
                user.is_student = False  # 教職員他
    print(user)
    user.save()

@receiver(social_account_added)
def account_added(request, sociallogin, **kwargs):
    user = request.user
    social_info = sociallogin.account
    social_token = sociallogin.token
    if social_info.provider == "google":
        if social_info.extra_data["hd"] == "iniad.org":
            user.email = social_info.extra_data["email"]
            user.first_name = social_info.extra_data["given_name"]
            user.last_name = social_info.extra_data["family_name"]
            user.initialized = False
            match = re.match(r"s1f10([0-9]{2})[0-9]{5}@iniad\.org", social_info.extra_data["email"])
            if(match):
                user.entry_year = int(match.group(2)) + 2000
                user.is_student = True  # 学生
                user.student_id = "1F10" + match.group(1)
            else:
                user.is_student = False  # 教職員他
            print(user)
            user.save()