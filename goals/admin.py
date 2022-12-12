from django.contrib import admin

from goals.models.goalcategory import GoalCategory


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


admin.site.register(GoalCategory, GoalCategoryAdmin)