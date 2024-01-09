from rest_framework import serializers
from courses.models import Course
from students_courses.serializers import StudentCourseSerializer
from contents.serializers import ContentSerializer
from accounts.models import Account
from rest_framework.exceptions import ValidationError
# from django.shortcuts import get_object_or_404


class CourseSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(read_only=True, many=True)
    students_courses = StudentCourseSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "status",
            "start_date",
            "end_date",
            "instructor",
            "contents",
            "students_courses",
        ]

    def create(self, validated_data: dict):
        return Course.objects.create(**validated_data)


class CourseStudentsSerializer(serializers.ModelSerializer):
    students_courses = StudentCourseSerializer(many=True)

    class Meta:
        model = Course
        fields = ["id", "name", "students_courses"]
        read_only_fields = ["name"]

    def update(self, instance: Course, validated_data: dict):
        
        students = []
        students_not_found = []

        for student_course in validated_data["students_courses"]:
            student = student_course["student"]
            student_found = Account.objects.filter(email=student["email"]).first()

            if student_found:
                students.append(student_found)
            else:
                students_not_found.append(student["email"])

        if students_not_found:
            raise ValidationError(
                {"detail": f"No active accounts was found: {', '.join(students_not_found)}."}
            )
        
        if not self.partial:
            instance.students.add(*students)
            return instance
        return super().update(instance, validated_data)
