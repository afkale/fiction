from rest_framework.routers import DefaultRouter

from users import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"groups", views.GroupViewSet, basename="group")
