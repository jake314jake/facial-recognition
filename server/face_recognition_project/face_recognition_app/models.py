from django.db import models

# Create your models here.
# face_recognition_app/models.py



class Users(models.Model):
    UserID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=50, null=True, blank=True)
    LastName = models.CharField(max_length=50, null=True, blank=True)
    Gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], null=True, blank=True)
    DateOfBirth = models.DateField(null=True, blank=True)
    IsActive = models.BooleanField(default=False)
    CreationTime = models.DateTimeField(auto_now_add=True)
    class Meta:
        app_label = 'face_recognition_app'


class FaceEmbeddings(models.Model):
    UserID = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    FaceEmbedding = models.BinaryField(null=True, blank=True)
    class Meta:
        app_label = 'face_recognition_app'


class AccessLogs(models.Model):
    LogID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE)
    AccessTime = models.DateTimeField(auto_now_add=True)
    AccessResult = models.CharField(max_length=10, choices=[('Granted', 'Granted'), ('Denied', 'Denied')])
    class Meta:
        app_label = 'face_recognition_app'


