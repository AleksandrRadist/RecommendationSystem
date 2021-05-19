from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (api_orders, api_orders_detail, api_orders_confirm, api_orders_cancel,
                    api_orders_public, api_orders_public_detail, api_orders_complete,
                    api_orders_accept)
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('orders/public/', api_orders_public, name='api_orders'),
    path('orders/public/<str:code>/', api_orders_public_detail, name='api_orders_detail'),
    path('orders/<str:code>/confirm/', api_orders_confirm, name='api_orders_status_confirm'),
    path('orders/<str:code>/cancel/', api_orders_cancel, name='api_orders_status_cancel'),
    path('orders/<int:order_id>/complete/', api_orders_complete, name='api_orders_complete'),
    path('orders/<int:order_id>/accept/', api_orders_accept, name='api_orders_accept'),
    path('orders/', api_orders, name='api_orders'),
    path('orders/<str:code>/', api_orders_detail, name='api_orders_detail'),
]