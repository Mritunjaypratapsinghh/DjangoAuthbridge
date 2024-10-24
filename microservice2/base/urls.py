from django.urls import path
from .views import LoginView, PrivateResourceView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    # path('logout/', logout_view, name='logout'),
    path('private', PrivateResourceView.as_view(),name='private-resource'),
]
