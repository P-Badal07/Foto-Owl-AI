from django.contrib import admin
from .models import Book, BorrowRequest, BorrowHistory

# Customize Book Admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'isbn', 'available')  # Columns displayed
    search_fields = ('title', 'author', 'isbn')  # Searchable fields
    list_filter = ('available',)  # Filters
    ordering = ('id',)


# Customize BorrowRequest Admin
@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'start_date', 'end_date', 'status')  # Columns displayed
    list_filter = ('status', 'start_date', 'end_date')  # Filters
    search_fields = ('user__username', 'book__title')  # Searchable fields
    ordering = ('id',)
    list_editable = ('status',)  # Allow inline editing of status


# Customize BorrowHistory Admin
@admin.register(BorrowHistory)
class BorrowHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'borrowed_on', 'returned_on')  # Columns displayed
    search_fields = ('user__username', 'book__title')  # Searchable fields
    list_filter = ('borrowed_on', 'returned_on')  # Filters
    ordering = ('id',)
