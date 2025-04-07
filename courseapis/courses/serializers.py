# Import các model Course, Category, Lesson từ ứng dụng courses
from courses.models import Course, Category, Lesson, Tag, Comment, User

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


# Tạo một lớp serializer cơ bản kế thừa từ ModelSerializer để tùy chỉnh cách hiển thị dữ liệu
class BaseSerializer(serializers.ModelSerializer):

    # Ghi đè phương thức to_representation để tùy chỉnh dữ liệu trả về khi serialize
    def to_representation(self, instance):
        # Gọi phương thức to_representation gốc để lấy dữ liệu serialize mặc định dưới dạng dict
        d = super().to_representation(instance)

        # Gán giá trị 'image' bằng đường dẫn URL thật sự từ trường image của model (thay vì chỉ là tên file)
        d['image'] = instance.image.url

        # Trả về dict đã được chỉnh sửa — bao gồm cả các trường mặc định và đường dẫn ảnh
        return d


class CourseSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = ['id', 'subject', 'description', 'created_date', 'image','category_id']

class LessonSerializer(BaseSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'created_date', 'image']

# Định nghĩa một serializer cho model Tag
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


# Định nghĩa một serializer chi tiết cho model Lesson
class LessonDetailSerializer(LessonSerializer):
    # Thêm trường tags để hiển thị danh sách các tag liên kết, sử dụng TagSerializer để serialize từng tag
    tags = TagSerializer(many=True)  # many=True nghĩa là một bài học có thể có nhiều tags
    class Meta:
        model = LessonSerializer.Meta.model
        # Kế thừa các trường từ LessonSerializer ban đầu, rồi thêm 'content' và 'tags
        fields = LessonSerializer.Meta.fields + ['content', 'tags']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'avatar']
        extra_kwargs = {
            # Trường password chỉ cho phép ghi (write-only), không hiển thị khi trả dữ liệu
            'password': {
                'write_only': True
            }
        }

    # Tạo user mới và mã hóa mật khẩu trước khi lưu
    def create(self, validated_data):
        data = validated_data.copy()
        u = User(**data)
        u.set_password(u.password)  # Mã hóa mật khẩu
        u.save()
        return u

    def to_representation(self, instance):
        d = super().to_representation(instance)
        d['avatar'] = instance.avatar.url if instance.avatar else ''

        return d


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'updated_date', 'user']
