# Import các model Category, Lesson, Course từ file models.py của app courses
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from courses.models import Category, Lesson, Course, User
# Import file serializers.py trong app courses (chứa các class để chuyển đổi dữ liệu model)
from courses import serializers, paginators, permis
from rest_framework import viewsets, generics, parsers, permissions

# Định nghĩa một class CategoryViewSet để xử lý API hiển thị danh sách Category
class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    # Chỉ định tập dữ liệu sẽ được truy xuất: lọc các Category có trường active=True
    queryset = Category.objects.filter(active=True)

    # Chỉ định serializer dùng để biến đổi dữ liệu Category sang JSON và ngược lại
    serializer_class = serializers.CategorySerializer

class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializer
    # Chỉ định lớp phân trang cho API này (tùy chỉnh phân trang cho khóa học)
    pagination_class = paginators.CoursePaginator

    # Hàm trả về queryset với các điều kiện lọc (search filter)
    def get_queryset(self):
        query = self.queryset  # Lấy queryset ban đầu (tất cả các khóa học)

        # Lọc theo từ khóa 'q' trong URL (tìm kiếm trong môn học)
        q = self.request.query_params.get('q')
        if q:
            # Nếu có 'q', lọc các khóa học có môn học chứa từ khóa tìm kiếm
            query = query.filter(subject__icontains=q)

        # Lọc theo category (danh mục) nếu tham số 'category' có trong URL
        cate_id = self.request.query_params.get('category')
        if cate_id:
            # Nếu có 'category', lọc các khóa học theo id của danh mục
            query = query.filter(category_id=cate_id)

        # Trả về queryset đã được lọc theo các điều kiện
        return query

    # Định nghĩa một custom action trong ViewSet (thường dùng với Django REST Framework).
    @action(methods=['get'], url_path='lessons', detail=True)
    # Định nghĩa hàm xử lý khi client gửi yêu cầu GET đến endpoint `/.../<pk>/lessons/`
    def get_lesson(self, request, pk):
        # Lấy object chính từ ViewSet theo khóa chính (pk), sau đó truy cập đến liên kết các bài học (lesson_set)
        # và lọc những bài học có trường active=True
        lessons = self.get_object().lesson_set.filter(active=True)

        # Sử dụng serializer để chuyển danh sách lesson sang dạng JSON (có many=True vì là danh sách),
        # sau đó trả về Response (dữ liệu JSON) cho client
        return Response(serializers.LessonSerializer(lessons, many=True).data)

# ViewSet chỉ hỗ trợ xem chi tiết 1 bài học (GET /lessons/<id>/)
class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    # Lấy các bài học đang hoạt động và load trước tags (tối ưu truy vấn)
    # Sử dụng prefetch_related để tối ưu việc truy vấn các tag liên quan (mối quan hệ many-to-many)
    queryset = Lesson.objects.prefetch_related('tags').filter(active=True)
    # Dùng serializer có thêm nội dung và tags
    serializer_class = serializers.LessonDetailSerializer

    # Tạo endpoint phụ: GET /lessons/<id>/comments/
    @action(methods=['get'], url_path='comments', detail=True)
    def get_comment(self, request, pk):
        # select_related('user') giúp tối ưu truy vấn khi lấy thông tin user của mỗi bình luận.
        comments = self.get_object().comment_set.select_related('user').filter(active=True)
        return Response(serializers.CommentSerializer(comments, many=True).data)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    # Cho phép xử lý dữ liệu dạng multipart (ví dụ: upload file, hình ảnh)
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            # Áp dụng quyền kiểm tra chủ sở hữu (chỉ cho phép nếu là chủ object)
            return [permis.OwnerPerms()]

        # Ngược lại (ví dụ: GET, POST...), cho phép truy cập tự do không cần xác thực
        return [permissions.AllowAny()]

    # API trả về thông tin người dùng đang đăng nhập (yêu cầu xác thực) - endpoint GET /.../current_user/
    @action(methods=['get'], url_path='current_user', detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_current_user(self, request):
        return Response(serializers.UserSerializer(request.user).data)


