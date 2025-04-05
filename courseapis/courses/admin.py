from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from courses.models import Category, Course, Lesson, Tag
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path

# Chỉnh sửa template admin
class MyAdminSite(admin.AdminSite):
    site_header = 'Quản lý khóa học trực tuyến'

    # Ta cũng có thể thêm view mới vào admin site.
    def get_urls(self):
        return [
            path('course-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        stats = Course.objects.annotate(lesson_count=Count('lesson__id')).values('id', 'subject', 'lesson_count')

        return TemplateResponse(request, 'admin/stats_view.html', {
            'stats': stats
        })

# Tạo một instance mới ta tự định nghĩa
admin_site = MyAdminSite(name='admin')


class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'


# Ghi đè lại giao diện admin cho lesson
class MyLessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'active', 'created_date', 'course_id']
    search_fields = ['subject', 'content']
    list_filter = ['id', 'created_date', 'subject']
    readonly_fields = ['image_view'] # Ngoài những field có sẵn sinh ra từ các thuộc tính ra, thì ta có thể thêm các field tự định nghĩa thông qua readonly_fields
    form = LessonForm

    def image_view(self, lesson):
        if lesson:
            return mark_safe(
                f'<img src="/static/{lesson.image.name}" width="120" >'
            )


admin_site.register(Category)
admin_site.register(Course)
admin_site.register(Lesson, MyLessonAdmin)
admin_site.register(Tag)