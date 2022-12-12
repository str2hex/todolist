from django.contrib import admin

from goals.models.goalcategory import GoalCategory
from goals.models.goals import Goals
from goals.models.goalscommets import GoalComment


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goals)
admin.site.register(GoalComment)