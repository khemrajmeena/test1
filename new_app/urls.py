from django import views
from django.urls import path
from .views import *

urlpatterns = [
    path('school-stats/', SchoolStatsView.as_view(), name='school-stats'),
    path('enrolled/', EnrolledCoursesView.as_view(),name='enrolled'),
    path('test/',testView.as_view(),name='test'),
    path('detail/',DetailsView.as_view(),name='detail'),
    path('detail/<int:school_id>/', DetailsView.as_view(), name='detail_id'),
    path("student/",StudentdetailsView.as_view(),name='student_details'),
    path("student/<int:course_id>/",StudentdetailsView.as_view(),name='student_details'),
    path('live-stock-data/<str:symbol>/', LiveStockDataView.as_view(), name='live_stock_data'),
    path('extract-stock-data/', ExtractStockDataView.as_view(), name='extract_stock_data'),
    
    # Other URL patterns
]