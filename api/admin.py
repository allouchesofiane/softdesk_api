from django.contrib import admin
from .models import User, Project, Contributor, Issue, Comment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'email', 'age', 'can_be_contacted', 'created_time', 'can_be_contacted', 'can_data_be_shared')
    ordering = ('-created_time',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'type', 'author', 'created_time')
    ordering = ('-created_time',)


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'project', 'role', 'created_time')
    ordering = ('-created_time',)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'project', 'priority', 'status', 'tag', 'author', 'assigned_to', 'created_time')
    ordering = ('-created_time',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','uuid', 'author', 'issue', 'created_time', 'description', 'author__username', 'issue__title')
    readonly_fields = ('uuid',)
