from django.contrib import admin
from django.urls import path
from transaction import views



urlpatterns = [
    path('send_statement/',views.Send_bank_Statement.as_view()),
    path('view_statement/',views.View_transaction.as_view()),
    path('view_statement_id/<int:t_id>/',views.view_transaction_id.as_view())
]

