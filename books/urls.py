from rest_framework.routers import DefaultRouter

from books import views

router = DefaultRouter()
router.register(r"books", views.BookViewSet, basename="book")
router.register(r"pages", views.PageViewSet, basename="page")
