from django.urls import path, include
from Crawler_App import views

urlpatterns = [
    path('get-product-details-view/', views.ProductDetailsApiView.as_view()),
    path('html-view/', views.HtmlApiView.as_view()),
    path('get-product-historydetails-view/', views.ProductDetailsHistoryApiView.as_view()),
    path('price-trend-view/', views.PriceTrendApiView.as_view())

]
 