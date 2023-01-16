from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
import openpyxl
from zipfile import BadZipfile

from .models import  StatusModel, WorkersModel
from .forms import  StatusForm, UserForm, WorkerForm


# ##############################
#                              #
#   Umumiy                     #
#                              #
################################

def index(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active and not user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse('attendance:profile', pk=user.pk))
            elif user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse('attendance:dashboard'))
            else:
                return HttpResponse("ACCOUNT IS DEACTIVATED")

        else:
            return render(request, 'attendance/index.html', {'error_message': 'Invalid login'})
    return render(request, 'attendance/index.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active and not user.is_superuser:
                login(request, user)
                return redirect('attendance:profile', pk=user.pk)
            elif user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse('attendance:dashboard'))
            else:
                return HttpResponse("ACCOUNT IS DEACTIVATED")

        else:
            return render(request, 'attendance/index.html', {'error_message': 'Invalid login'})
    return render(request, 'attendance/index.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('attendance:index'))


def custom_page_not_found_view(request, exception):
    return render(request, "attendance/errors/404.html", {})


def custom_error_view(request, exception=None):
    return render(request, "attendance/errors/500.html", {})


def custom_permission_denied_view(request, exception=None):
    return render(request, "attendance/errors/403.html", {})


def custom_bad_request_view(request, exception=None):
    return render(request, "attendance/errors/400.html", {})

# ##############################
#                              #
#     Administrator uchun      #
#                              #
################################
# Main page for administer
class AdminDashboardView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'attendance/dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super(AdminDashboardView, self).get_context_data(**kwargs)
        context['title'] = StatusModel.objects.all()
        # context['workers'] = Workers.objects.all()
        # context['attendance'] = Attendance.objects.all()
        return context

# ######################### Status Model Start #################################
# Status List View and Bulk delete View
class AdminStatusView(SuccessMessageMixin, LoginRequiredMixin, View):
    success_url = reverse_lazy('attendance:admin_status')
    success_message = "Поздравляем. Выбранные должности удаляются!"
    danger_message = "You can't delete first element!"
    def get(self, request):
        status_title = StatusModel.objects.all()
        context = {'status_title': status_title}
        return render(request, 'attendance/dashboard/admin_status.html',context)

    def post(self, request, *args, **kwargs):
        status_title = self.request.POST.getlist('title')
        try:
            StatusModel.objects.filter(pk__in=status_title).delete()
            messages.success(self.request, self.success_message, extra_tags='alert-danger')
        except ObjectDoesNotExist:
            messages.success(self.request, self.danger_message, extra_tags='alert-danger')

        return redirect('attendance:admin_status')

# Status Update View
class AdminStatusUpdateView(LoginRequiredMixin,UpdateView):
    model = StatusModel
    fields = ['status_name', 'status_description']
    template_name = 'attendance/dashboard/admin_status_update.html'
    success_url = reverse_lazy('attendance:admin_status')
    
    def form_valid(self, form):
        messages.success(self.request, "Должность успешно обновлена.")
        return super(AdminStatusUpdateView,self).form_valid(form)

# Create a new status
@user_passes_test(lambda u: u.is_superuser)
def StatusCreateView(request):
    registered = False
    if request.method == "POST":
        worker_form = StatusForm(data=request.POST)
        if worker_form.is_valid():
            s_create = worker_form.save(commit=True)
            s_create.save()
            registered = True
    else:
            worker_form = StatusForm()

    return render(request, 'attendance/dashboard/admin_status_create.html', {
        'worker_form': worker_form,'registered':registered,
    })
# ######################### StatusModel Model End #################################


# ######################### WorkersModel Model Start ################################
# All workers list and Bulk deletion View
class AdminWorkerView(SuccessMessageMixin, LoginRequiredMixin, View):
    success_url = reverse_lazy('attendance:admin_worker')
    success_message = "Поздравляем. Выбранные рабочие удаляются!"
    def get(self, request):
        workers = WorkersModel.objects.all()
        context = {'workers': workers}
        return render(request, 'attendance/dashboard/admin_worker.html',context)

    def post(self, request, *args, **kwargs):
        workers = self.request.POST.getlist('worker')
        WorkersModel.objects.filter(pk__in=workers).delete()
        messages.success(self.request, self.success_message, extra_tags='alert-danger')
        return redirect('attendance:admin_worker')

# Worker's Details
@user_passes_test(lambda u: u.is_superuser)
def WorkerDetailView(request, pk):
    worker  = get_object_or_404(WorkersModel, pk=pk)
    context ={}
    if request.user.is_superuser:
        sc_form = WorkerForm(request.POST or None, instance = worker)
        if request.method == 'POST':
            if 'worker_update_btn' in request.POST:
                if sc_form.is_valid():
                    sc_form.save()
            elif 'worker_delete_btn' in request.POST:
                worker.delete()
                return  redirect('attendance:admin_worker')
            return  redirect('attendance:admin_worker_detail',pk=worker.pk)
        
    context = {
        'worker': worker,
        'sc_form':sc_form,
    }

    return render(request,'attendance/dashboard/admin_worker_detail.html', context)

# Create a new worker
@user_passes_test(lambda u: u.is_superuser)
def WorkerCreateView(request):
    registered = False
    if request.method == "POST":
        worker_form = WorkerForm(data=request.POST)
        if worker_form.is_valid():
            s_create = worker_form.save(commit=True)
            s_create.save()
            registered = True
    else:
            worker_form = WorkerForm()

    return render(request, 'attendance/dashboard/admin_worker_create.html', {
        'worker_form': worker_form,'registered':registered,
    })

# Create a new worker with xlsx file
@user_passes_test(lambda u: u.is_superuser)
def AdminXlsxFileAdd(request):
    if "GET" == request.method:
        return render(request, 'attendance/dashboard/add_xlsx_file.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        is_bad_zip = False
        try:
            wb = openpyxl.load_workbook(excel_file)
            sheet_list = [sheet.title for sheet in wb]
            for i in sheet_list:
                try:
                    worksheet = wb[i]
                    excel_data = list()
                    for row in range(1, 17):
                        row_data = list()
                        for cell in worksheet[row]:
                            row_data.append(str(cell.value))
                        excel_data.append(row_data)
                        
                    for row in range(2, worksheet.max_row ):
                        worker_name = (worksheet[f'B{row}'].value)
                        worker_id = (worksheet[f'D{row}'].value)
                        day_off = (worksheet[f'E{row}'].value)
                        UserName = (worksheet[f'F{row}'].value)
                        print(UserName)
                        if worker_name is None or worker_id is None or day_off is None or UserName is None:
                            break
                        manager_name = User.objects.get(username=UserName)
                        worker_status, created = StatusModel.objects.get_or_create(
                                            status_name=(worksheet[f'C{row}'].value)
                                    )

                       
                        worker_add, created = WorkersModel.objects.get_or_create(
                                    worker_name = worker_name,
                                    worker_status = worker_status,
                                    worker_id = worker_id,
                                    day_off = day_off,
                                    manager_name = manager_name,
                                )
                    break
                except KeyError:
                    excel_data = "Ma'lumot kiritishda xatolik"
        except BadZipfile:
            is_bad_zip = True
            excel_data = "XLSX fayl bo'lishi kerak"
        
            
        context = {"excel_data":excel_data, 'is_bad_zip':is_bad_zip}

        return render(request, 'attendance/dashboard/add_xlsx_file.html', context)

# ######################### WorkersModel Model End ################################


# ######################### User Model Start ################################
# Adding new Active User Form for Workers' Attendance
@user_passes_test(lambda u: u.is_superuser)
def CreateUserView(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            username = user_form.cleaned_data['username']
            password1 = user_form.cleaned_data['password1']
            user.set_password(password1)
            user.save()
            user = authenticate(username=username, password=password1)

            registered = True

        
    else:
        user_form = UserForm()

    return render(request, 'attendance/dashboard/add_user.html', {
        'registered': registered,
        'user_form': user_form,
    })

# ######################### User Model End ################################


# ##############################
#                              #
#           User uchun         #
#                              #
################################
# Main page for user
class UserDashboardView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'attendance/profile/index.html'

    def get_context_data(self, **kwargs):
        context = super(UserDashboardView, self).get_context_data(**kwargs)
        context['workers'] = WorkersModel.objects.filter(manager_name=context['user'])
        return context

    def get_queryset(self):
        queryset = User.objects.filter(username=self.request.user)
        test_queryset = WorkersModel.objects.filter(manager_name=self.request.user)
        if queryset:
            return queryset

        else:
            return queryset