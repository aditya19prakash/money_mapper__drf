from django.urls import include,path
from user import views
urlpatterns = [
     path("login/",views.User_login_page.as_view()),
     path("logout/",views.User_logout_page.as_view()),
     path("refresh_token/",views.Refersh_access_token.as_view())
]
