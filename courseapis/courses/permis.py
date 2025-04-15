from rest_framework import permissions


# Custom permission chỉ cho phép người dùng đã đăng nhập
# và là chủ sở hữu của đối tượng (object) mới được phép truy cập
class OwnerPerms(permissions.IsAuthenticated):

    # Kiểm tra quyền truy cập đối với từng object (ví dụ: chỉ xem/sửa object của chính mình)
    def has_object_permission(self, request, view, obj):
        # Gọi phương thức kiểm tra quyền từ lớp cha (IsAuthenticated) để đảm bảo user đã đăng nhập
        # Sau đó kiểm tra xem user hiện tại có phải là chủ sở hữu của object không
        return super().has_object_permission(request, view, obj) and request.user == obj

class CommentOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj) and request.user == obj.user
