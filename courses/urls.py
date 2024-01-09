from django.urls import path
from . import views
from contents.views import CreateContentView, RetrieveUpdateDestroyContentView


urlpatterns = [
    path("courses/", views.CreateListCourseView.as_view()),
    path("courses/<uuid:course_id>/", views.RetrieveUpdateDestroyCourseView.as_view()),
    path("courses/<uuid:course_id>/contents/", CreateContentView.as_view()),
    path(
        "courses/<uuid:course_id>/contents/<uuid:content_id>/",
        RetrieveUpdateDestroyContentView.as_view(),
    ),
    path("courses/<uuid:course_id>/students/", views.AddStudentToCourse.as_view()),
    path(
        "courses/<uuid:course_id>/students/<uuid:student_id>/",
        views.DeleteStudentFromCourseView.as_view(),
    ),
]