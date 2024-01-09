from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Content
from courses.models import Course
from .serializers import ContentSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsSuperuser
from contents.permissions import AccountOwner
from rest_framework.exceptions import NotFound


class CreateContentView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperuser]

    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    lookup_url_kwarg = "course_id"

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs[self.lookup_url_kwarg])


class RetrieveUpdateDestroyContentView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, AccountOwner]

    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    lookup_url_kwarg = "content_id"

    def get_object(self):
        try:
            Course.objects.get(id=self.kwargs["course_id"])
            content = Content.objects.get(id=self.kwargs["content_id"])
        except Course.DoesNotExist:
            raise NotFound({'detail': 'course not found.'})
        except Content.DoesNotExist:
            raise NotFound({'detail': 'content not found.'})

        self.check_object_permissions(self.request, content)

        return content
