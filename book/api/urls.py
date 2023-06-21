from rest_framework.routers import DefaultRouter

from book.api import views

router = DefaultRouter()
router.register("books", views.BookViewSet)
router.register("pages", views.PageViewSet)

urlpatterns = router.urls
