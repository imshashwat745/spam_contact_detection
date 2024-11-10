from django.urls import path
from app import views
from app.views.register_user_view import register_user
from app.views.login_user_view import login_user
from app.views.mark_spam_view import mark_spam
from app.views.search_info_by_name import search_info_by_name
from app.views.search_info_by_contact import search_info_by_contact

urlpatterns = [
    path("register/", register_user),
    path("login/", login_user),
    path("mark_spam/", mark_spam),
    path("search_by_name/", search_info_by_name),
    path("search_by_contact/", search_info_by_contact),
]
