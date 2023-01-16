from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'attendance'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'login/', views.login_user, name='login_user'),
    path(r'logout/', views.user_logout, name='user_logout'),
    #
    # # ##############################
    # #                              #
    # #     Administrator uchun      #
    # #                              #
    # ################################

    # Main Page
    path(r'dashboard/', views.AdminDashboardView.as_view(), name='dashboard'),

    # Status Model and View
    path(r'dashboard/admin_status/', views.AdminStatusView.as_view(), name='admin_status'),
    path(r'dashboard/admin_status_create/', views.StatusCreateView, name='admin_status_create'),
    path(r'dashboard/admin_status_update/<int:pk>/', views.AdminStatusUpdateView.as_view(), name='admin_status_update'),

    # Workers Model and View
    path(r'dashboard/admin_worker/', views.AdminWorkerView.as_view(), name='admin_worker'),
    path(r'dashboard/admin_worker_detail/<int:pk>/', views.WorkerDetailView, name='admin_worker_detail'),
    path(r'dashboard/admin_worker_create/', views.WorkerCreateView, name='admin_worker_create'),
    path(r'dashboard/add_xlsx_file/', views.AdminXlsxFileAdd, name='add_xlsx_file'),
    path(r'dashboard/add_user/', views.CreateUserView, name='admin_add_user'),
    
    # # ##############################
    # #                              #
    # #   Oddiy foydalanuvchi uchun  #
    # #                              #
    # ################################
    path(r'profile/(?P<pk>[0-9]+)/', views.UserDashboardView.as_view(), name='profile'),
    # path(r'profile/(?P<pk>[0-9]+)/teacher_class_list/', views.TeacherClassListView, name='teacher_class_list'),
    # path(r'profile/(?P<pk>[0-9]+)/teacher_attendance_ranking/', views.TeacherSchoolRankingView.as_view(),
    #      name='teacher_attendance_ranking'),
    # path(r'profile/(?P<pk>[0-9]+)/schools_ranking_list/', views.AllSchoolsRankingView.as_view(),
    #      name='schools_ranking_list'),
    # path(r'profile/(?P<pk>[0-9]+)/attendance_list/', views.TeacherAttendanceListView, name='attendance_list'),
    # path(r'profile/(?P<pk>[0-9]+)/attendance_form1/(?P<slug>[0-9]+)/', views.attendance_form, name='attendance_form1'),
    # path(r'profile/(?P<pk>[0-9]+)/teacher_class_detail/(?P<slug>[0-9]+)/', views.TeacherClassDetailView,
    #      name='teacher_class_detail'),
    # path(
    #     r'profile/(?P<pk>[0-9]+)/teacher_class_detail/(?P<str:class_slug>[0-9]+)/teacher_student_detail/(?P<slug:student_slug>(0-9)+)/',
    #     views.TeacherStudentDetailView, name='teacher_student_detail'),
    # path(r'profile/(?P<pk>[0-9]+)/user_attendance_report/', views.TeacherAttendanceReportView,
    #      name='user_attendance_report'),
    # path(r'profile/profile_detail/(?P<pk>[0-9]+)/', views.TeacherProfileView.as_view(), name='profile_detail'),
    # path(r'profile/profile_detail/(?P<pk>[0-9]+)/user_profile_update/', views.TeacherProfileUpdateView.as_view(),
    #      name='user_profile_update'),

]