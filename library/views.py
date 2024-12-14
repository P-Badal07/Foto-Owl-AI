from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Book, BorrowRequest, BorrowHistory
from .serializers import BookSerializer, BorrowRequestSerializer, BorrowHistorySerializer
from rest_framework.permissions import IsAuthenticated
import csv
from django.utils import timezone

# Create User View
class CreateUserView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        if username and password and email:
            User.objects.create_user(username=username, email=email, password=password)
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    """
    User login view. Returns a token for authenticated users.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if username and password are provided
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(username=username, password=password)
        if user:
            # Generate or get existing token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "message": "Login successful",
                "username": user.username
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# List All Books View
class ListBooksView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# Borrow Request View
class BorrowRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book_id = request.data.get("book_id")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        book = get_object_or_404(Book, id=book_id)
        user = request.user

        # Check for overlapping borrow requests
        if BorrowRequest.objects.filter(book=book, status='Approved', start_date__lte=end_date, end_date__gte=start_date).exists():
            return Response({"error": "Book is already borrowed for the selected dates"}, status=status.HTTP_400_BAD_REQUEST)

        # Create Borrow Request
        borrow_request = BorrowRequest.objects.create(
            user=user, book=book, start_date=start_date, end_date=end_date, status='Pending'
        )
        return Response({"message": "Borrow request submitted successfully"}, status=status.HTTP_201_CREATED)


# Approve/Deny Borrow Request View
class ApproveBorrowRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        action = request.data.get("action")  # "Approve" or "Deny"
        borrow_request = get_object_or_404(BorrowRequest, id=request_id)

        if action not in ['Approve', 'Deny']:
            return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        if action == "Approve":
            borrow_request.status = "Approved"
            borrow_request.book.available = False
            borrow_request.book.save()
        elif action == "Deny":
            borrow_request.status = "Denied"

        borrow_request.save()
        return Response({"message": f"Borrow request {action}d successfully"}, status=status.HTTP_200_OK)


# View All Borrow Requests (Admin)
class ListAllBorrowRequestsView(ListAPIView):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer


# Personal Borrow History View
class PersonalBorrowHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BorrowHistory.objects.filter(user=self.request.user)

    serializer_class = BorrowHistorySerializer


# Download Borrow History as CSV View
class DownloadBorrowHistoryCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        borrow_history = BorrowHistory.objects.filter(user=user)

        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="borrow_history.csv"'

        writer = csv.writer(response)
        writer.writerow(['Book Title', 'Borrowed On', 'Returned On'])

        for record in borrow_history:
            writer.writerow([record.book.title, record.borrowed_on, record.returned_on])

        return response
