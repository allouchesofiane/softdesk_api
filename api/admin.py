from django.contrib import admin
from .models import User, Project, Contributor, Issue, Comment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'age', 'can_be_contacted', 'created_time')
    list_filter = ('can_be_contacted', 'can_data_be_shared')
    search_fields = ('username', 'email')
    ordering = ('-created_time',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'author', 'created_time')
    list_filter = ('type',)
    search_fields = ('name', 'description')
    ordering = ('-created_time',)


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role', 'created_time')
    list_filter = ('role',)
    search_fields = ('user__username', 'project__name')
    ordering = ('-created_time',)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'priority', 'status', 'tag', 'author', 'assigned_to', 'created_time')
    list_filter = ('priority', 'status', 'tag')
    search_fields = ('title', 'description')
    ordering = ('-created_time',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'author', 'issue', 'created_time')
    search_fields = ('description', 'author__username', 'issue__title')
    ordering = ('-created_time',)
    readonly_fields = ('uuid',)
