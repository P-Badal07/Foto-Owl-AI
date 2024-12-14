from django.urls import path
from .views import *

urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('login/', LoginView.as_view(), name='login'),
    path('books/', ListBooksView.as_view(), name='list-books'),
    path('borrow-request/', BorrowRequestView.as_view(), name='borrow-request'),
    path('approve-request/<int:request_id>/', ApproveBorrowRequestView.as_view(), name='approve-request'),
    path('all-borrow-requests/', ListAllBorrowRequestsView.as_view(), name='all-borrow-requests'),
    path('borrow-history/', PersonalBorrowHistoryView.as_view(), name='personal-borrow-history'),
    path('borrow-history/csv/', DownloadBorrowHistoryCSVView.as_view(), name='borrow-history-csv'),
]
