# Import các model Category, Lesson, Course từ file models.py của app courses
from courses.models import Category, Lesson, Course

# Import file serializers.py trong app courses (chứa các class để chuyển đổi dữ liệu model)
from courses import serializers

# Import viewsets và generics từ Django REST Framework để tạo API view
from rest_framework import viewsets, generics

# Định nghĩa một class CategoryViewSet để xử lý API hiển thị danh sách Category
class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    # Chỉ định tập dữ liệu sẽ được truy xuất: lọc các Category có trường active=True
    queryset = Category.objects.filter(active=True)

    # Chỉ định serializer dùng để biến đổi dữ liệu Category sang JSON và ngược lại
    serializer_class = serializers.CategorySerializer

class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializer

