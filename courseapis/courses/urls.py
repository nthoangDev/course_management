# Import hàm path và include để định nghĩa các URL patterns
from django.urls import path, include
# Import views từ cùng thư mục (nơi chứa CategoryViewSet)
from . import views
# Import DefaultRouter từ Django REST Framework để tự động tạo route cho viewsets
from rest_framework.routers import DefaultRouter

# Tạo một router mặc định (cung cấp sẵn các URL cho viewsets như list, create, retrieve, update, delete)
router = DefaultRouter()

# Đăng ký route cho viewset CategoryViewSet với prefix là 'categories'
# Ví dụ: /categories/ → list, /categories/1/ → retrieve
router.register('categories', views.CategoryViewSet, basename='category')
router.register('courses', views.CourseViewSet, basename='course')
router.register('lessons', views.LessonViewSet, basename='lesson')
router.register('users', views.UserViewSet, basename='user')

# Cấu hình URL chính, bao gồm tất cả các URL mà router đã tạo ra
urlpatterns = [
    path('', include(router.urls))  # Tự động sinh các đường dẫn từ router
]
