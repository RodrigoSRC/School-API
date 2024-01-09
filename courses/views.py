from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Course
from accounts.models import Account
from .serializers import CourseSerializer, CourseStudentsSerializer
from accounts.permissions import IsSuperuser
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from .permissions import AccountOwner


class CreateListCourseView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AccountOwner]

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return Course.objects.filter(students=self.request.user)
        return self.queryset.all()


class RetrieveUpdateDestroyCourseView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperuser]

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_url_kwarg = "course_id"


class AddStudentToCourse(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Course.objects.all()
    serializer_class = CourseStudentsSerializer
    lookup_url_kwarg = "course_id"


class DeleteStudentFromCourseView(RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperuser]

    queryset = Course.objects.all()
    serializer_class = CourseStudentsSerializer
    lookup_url_kwarg = "course_id"

    def perform_destroy(self, instance: Course) -> None:
        student_id = self.kwargs["student_id"]
        found_student = get_object_or_404(Account, id=student_id)

        if found_student not in instance.students.all():
            raise NotFound("this id is not associated with this course.")
        else:
            instance.students.remove(found_student)
