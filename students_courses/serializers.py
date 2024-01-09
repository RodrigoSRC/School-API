from rest_framework import serializers
from .models import StudentCourse


class StudentCourseSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(read_only=True, source="student.username")
    student_email = serializers.CharField(source="student.email")

    class Meta:
        model = StudentCourse
        fields = [
            "id",
            "status",
            "student_id",
            "student_username",
            "student_email",
        ]
