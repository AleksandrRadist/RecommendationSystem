from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (api_orders, api_orders_detail, api_orders_status_update,
                    api_orders_public, api_orders_public_detail)
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('orders/public/', api_orders_public, name='api_orders'),
    path('orders/public/<str:code>/', api_orders_public_detail, name='api_orders_detail'),
    path('orders/<str:code>/status/update/', api_orders_status_update, name='api_orders_status_change'),
    path('orders/', api_orders, name='api_orders'),
    path('orders/<str:code>/', api_orders_detail, name='api_orders_detail'),
]