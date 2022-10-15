from rest_framework.routers import DefaultRouter

from accounts.views import CustomUserViewSet


router = DefaultRouter()
router.register('', CustomUserViewSet)

urlpatterns = [] + router.urls
