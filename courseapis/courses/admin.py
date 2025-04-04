from django.contrib import admin
from courses.models import Category, Course, Lesson, Tag
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


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

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Lesson, MyLessonAdmin)
admin.site.register(Tag)