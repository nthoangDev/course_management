# Import các model Course, Category, Lesson từ ứng dụng courses
from courses.models import Course, Category, Lesson

# Import lớp serializers từ thư viện Django REST Framework để xây dựng serializer
from rest_framework import serializers

# Định nghĩa serializer cho model Category
class CategorySerializer(serializers.ModelSerializer):
    # Nội dung cấu hình serializer nằm trong lớp Meta
    class Meta:
        # Liên kết model Category với serializer này
        model = Category  # Sử dụng model Category làm cơ sở dữ liệu cho serializer

        # Chỉ định các trường sẽ được đưa vào trong quá trình serialize/deserialize
        fields = ['id', 'name']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'subject', 'description', 'created_date', 'category_id']