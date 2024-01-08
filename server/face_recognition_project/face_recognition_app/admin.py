from django.contrib import admin


from .models import Users, FaceEmbeddings, AccessLogs

admin.site.register(Users)
admin.site.register(FaceEmbeddings)
admin.site.register(AccessLogs)
