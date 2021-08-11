from django.contrib import admin
from .models import Question, Choices
# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choices
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    fieldsets = [
        ("question info", {'fields': ['question_text']}),
        ("Date info", {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choices)
