"""
URL configuration for StockWebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    # Url der starter med admin, bliver behandlet af admin appen.
    path("admin/", admin.site.urls),

    # Url der starter med accounts, bliver behandlet af accounts appen.
    path("accounts/", include("accounts.urls")),  # new
    path('accounts/', include('django.contrib.auth.urls')),

    # Url der starter med stocks, bliver behandlet af stocks appen.
    path("stocks/", include("stocks.urls")),
    # Url der starter med portfolio, bliver behandlet af portfolio appen.
    path("portfolio/", include("portfolio.urls"))
]
