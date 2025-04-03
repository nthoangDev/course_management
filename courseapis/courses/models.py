from django.db import models
from django.contrib.auth.models import AbstractUser

# Trong django có sẵn một model User kế thừa AbstractUser (Khó mở rộng sau này)
# => Vì vậy ta sẽ tự định nghĩa một model User để để mở rộng hơn
# Chý ý nên cấu hình lại trong settings.py thuộc tính AUTH_USER_MODEL = “myapp.MyUser”
class User(AbstractUser):
    pass
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



# Notes :
# - id: Trong django các trường dữ liệu sẽ tự sinh ra id -> nên không cần khai báo trường id

