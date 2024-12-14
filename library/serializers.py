from rest_framework import serializers
from .models import Book, BorrowRequest, BorrowHistory

# Book Serializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


# Borrow Request Serializer
class BorrowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRequest
        fields = '__all__'


# Borrow History Serializer
class BorrowHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowHistory
        fields = '__all__'
