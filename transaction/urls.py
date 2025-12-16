
from django.contrib import admin
from django.urls import path
from transaction import views
urlpatterns = [
    path('send_statement/<int:id>/',views.Send_bank_Statement.as_view()),
    path('view_statement/<int:id>/',views.View_transaction.as_view()),
    path('view_statement/<int:id>/transc_id/<int:t_id>/',views.view_transaction_id.as_view())
]
