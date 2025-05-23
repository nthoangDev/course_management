from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField

# Trong django có sẵn một model User kế thừa AbstractUser (Khó mở rộng sau này)
# => Vì vậy ta sẽ tự định nghĩa một model User để để mở rộng hơn
# Chý ý nên cấu hình lại trong settings.py thuộc tính AUTH_USER_MODEL = “myapp.MyUser”
class User(AbstractUser):
    avatar = CloudinaryField(null=True) # models.ImageField(upload_to='users/%Y/%m', null=True)


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True) # Lấy giá trị datetime chỉ lần đầu tạo
    updated_date = models.DateTimeField(auto_now=True) # Cập nhật thời điểm hiện tại liên tục mỗi mỗi lần cập nhật

    class Meta:
        abstract = True # Khai báo lớp này là lớp trừu tượng để không cần phải tạo ra table khi chạy dưới database
        ordering = ['-id'] # Các trường dữ liệu sẽ sắp xếp giảm dần theo id


class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Course(BaseModel):
    subject = models.CharField(max_length=255)
    description = models.TextField(null=True)
    image = CloudinaryField(null=True) #models.ImageField(upload_to='courses/%Y/%m')
    category = models.ForeignKey(Category, on_delete=models.PROTECT) # on_delete=models.PROTECT trường này sẽ được bảo vệ và không thể xóa

    class Meta:
        unique_together = ('subject', 'category') # Nghiệp vụ ở đây muốn subject của môn học và trong cùng một category không được trùng với nhau

    def __str__(self):
        return self.subject


class Lesson(BaseModel):
    subject = models.CharField(max_length=255)
    content = RichTextField()
    image = CloudinaryField(null=True) # models.ImageField(upload_to='courses/%Y/%m')
    course = models.ForeignKey(Course, on_delete=models.CASCADE) # Khi mà course bị xóa th các lesson cũng sẽ bị xóa toàn bộ
    tags = models.ManyToManyField('Tag')

    class Meta:
        unique_together = ('subject', 'course')  # Trong cùng mô course không thể có subject trùng nhau

    def __str__(self):
        return self.subject


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Model trừu tượng dùng chung cho các tương tác giữa user và lesson (ví dụ: Like, Bookmark, View,...)
class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        abstract = True


# Model Comment kế thừa từ Interaction, đại diện cho bình luận của người dùng với bài học
class Comment(Interaction):
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content


# Model Like kế thừa từ Interaction, đại diện cho lượt thích của người dùng với bài học
class Like(Interaction):
    class Meta:
        # Đảm bảo mỗi người dùng chỉ like 1 lần cho mỗi bài học
        unique_together = ('user', 'lesson')



# Notes :
# - id: Trong django các trường dữ liệu sẽ tự sinh ra id -> nên không cần khai báo trường id

