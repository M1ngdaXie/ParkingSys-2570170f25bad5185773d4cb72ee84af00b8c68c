from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from .models import Driver, Vehicle, Payment, Violation, Permit
from .forms import DriverForm, VehicleForm, PermitForm, PaymentForm, ViolationForm
from django.views.generic import TemplateView
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

# -------- Security --------
class UnauthorizedView(LoginRequiredMixin, TemplateView):
    template_name = 'driver/unauthorized.html'

def admin(request):
    return request.user.groups.filter(name='Admin').exists()

def guest(request):
    return request.user.groups.filter(name='Guest').exists()


# -------- Homepage --------
class HomepageView(LoginRequiredMixin, TemplateView):
    template_name = 'driver/homepage.html'


# ------------------------ Driver Dashboard Use Cases ------------------------

#-----Add Personal Info Crud ------
class PersonalInfo(LoginRequiredMixin, TemplateView):
    template_name = 'driver/personalinfo.html'


class AddPersonalInfoView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'driver/personal_info_add.html', {'form': DriverForm()})
        else:
            return redirect(reverse('login')) 
    def post(self, request):
        if request.user.is_authenticated:
            form = DriverForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('personalinfo')
            return render(request, 'driver/personal_info_add.html', {'form': form})
        else:
            return redirect(reverse('login')) 


from datetime import datetime, timedelta
class AddDriverPermitView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            form = PermitForm()
            return render(request, 'driver/driver_permit_add.html', {'form': form})
        else:
            return redirect(reverse('login')) 
    def post(self, request):
        if request.user.is_authenticated:
            form = PermitForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('personalinfo')
            return render(request, 'driver/driver_permit_add.html', {'form': form})
        else:
            return redirect(reverse('login')) 


class AddDriverVehicleView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'driver/driver_vehicle_add.html', {'form': VehicleForm()})
        else:
            return redirect(reverse('login')) 
    def post(self, request):
        if request.user.is_authenticated:
            form = VehicleForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('personalinfo')
            return render(request, 'driver/driver_vehicle_add.html', {'form': form})
        else:
            return redirect(reverse('login')) 


#-----Payment Crud ------
class PaymentAdd(LoginRequiredMixin, View):
    def get(self, request):
        form = None
        if not guest(request):
            return redirect('unauthorized')
        else:
            form = PaymentForm()
        return render(request=request,
                      template_name='driver/payment_add.html',
                      context={'form': form})
    def post(self, request):
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('payment_list'))
        return render(request=request,
                      template_name='driver/payment_add.html',
                      context={'form': form})


class PaymentList(LoginRequiredMixin, View):
    def get(self, request):
        payments = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            payments = Payment.objects.all()
        return render(request=request,
                      template_name='driver/payment_list.html',
                      context={'payments': payments})


class PaymentDelete(LoginRequiredMixin, View):
    def get(self, request, payment_id=None):
        if payment_id:
            payment = Payment.objects.get(pk=payment_id)
        else:
            payment = Payment()
        form = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            form = PaymentForm(instance=payment)
        for field in form.fields:
            form.fields[field].widget.attrs['disabled'] = True
        payment_list = Payment.objects.all()
        return render(request=request,
                      template_name='driver/payment_delete.html',
                      context={'payment': payment, 'form': form, 'payment_list': payment_list})
    def post(self, request, payment_id=None):
        payment = Payment.objects.get(pk=payment_id)
        form = PaymentForm(request.POST, instance=payment)
        payment.delete()
        return redirect(reverse('payment_list'))


class PaymentUpdate(LoginRequiredMixin, View):
    def get(self, request, payment_id=None):
        if payment_id:
            payment = Payment.objects.get(pk=payment_id)
            form = None
            if not admin(request):
                return redirect('unauthorized')
            else:
                form = PaymentForm(instance=payment)
        else:
            pass
        return render(request=request,
                      template_name='driver/payment_update.html',
                      context={'payment': payment, 'form': form})
    def post(self, request, payment_id=None):
        if payment_id:
            payment = Payment.objects.get(pk=payment_id)
        else:
            payment = Payment()
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save()
            return redirect(reverse('payment_list'))
        return render(request=request,
                      template_name='driver/payment_update.html',
                      context={'payment': payment, 'form': form})


class PaymentDetails(LoginRequiredMixin, View):
    def get(self, request, payment_id=None):
        payment = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            payment = Payment.objects.get(pk=payment_id)
        return render(request=request,
                      template_name='driver/payment_details.html',
                      context={'payment': payment})


#-----Pay for Violation (creates new payment and updates violation status to 'settled')------
def SelectViolationView(request):
    violations = Violation.objects.filter(status='Outstanding')
    return render(request, 'driver/select_violation.html', {'violations': violations})


class ViolationPaymentView(View):
    def get(self, request, violation_id=None):
        violation = Violation.objects.get(pk=violation_id)
        form = PaymentForm()
        return render(request, 'driver/violation_payment.html', {'violation': violation, 'form': form})
    def post(self, request, violation_id=None):
        violation = Violation.objects.get(pk=violation_id)
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            violation.status = 'Settled'
            violation.save()
            return redirect('select_violation')
        return render(request, 'driver/violation_payment.html', {'violation': violation, 'form': form})
    

#-----Pay for Permit (creates new payment and updates permit status to 'payed')------
def SelectPermitView(request):
    permits = Permit.objects.filter(status='Not Payed')
    return render(request, 'driver/select_permit.html', {'permits': permits})


def PermitPaymentView(request, permit_id):
    permit = Permit.objects.get(permit_id=permit_id)
    if permit.status == 'Payed':
        return redirect('homepage')
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            permit.status = 'Payed'
            permit.save()
            form.save() 
            return redirect('select_permit')
    else:
        form = PaymentForm()
    return render(request, 'driver/permit_payment.html', {'form': form})



# ------------------------ Admin Dashboard Use Cases ------------------------

#-----Driver Crud ------
class AddDriverView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'driver/driver_add.html', {'form': DriverForm()})
        else:
            return redirect(reverse('login')) 

    def post(self, request):
        if request.user.is_authenticated:
            form = DriverForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('personalinfo')
            return render(request, 'driver/driver_add.html', {'form': form})
        else:
            return redirect(reverse('login')) 


class DriverListView(LoginRequiredMixin, View):
    def get(self, request):
        drivers = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            drivers = Driver.objects.all()
        return render(request=request,
                      template_name='driver/driver_list.html', 
                      context={'drivers': drivers})


class DriverDelete(LoginRequiredMixin, View):
    def get(self,request,driver_id=None):
        if driver_id:
            driver = Driver.objects.get(pk=driver_id)
        else:
            driver = Driver()
        form = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            form = DriverForm(instance=driver)
        for field in form.fields:
            form.fields[field].widget.attrs['disabled'] = True
        driver_list = Driver.objects.all()
        return render(request=request,
                      template_name='driver/driver_delete.html', 
                      context={'driver': driver,'form':form, 'driver_list':driver_list})
    def post(self,request,driver_id=None):
        driver = Driver.objects.get(pk=driver_id)
        form = DriverForm(request.POST,instance=driver)
        driver.delete()
        return redirect(reverse('driver_list'))


class DriverUpdate(LoginRequiredMixin, View):
    def get(self,request,driver_id=None):
        if driver_id:
            driver = Driver.objects.get(pk=driver_id)
            form = None
            if not admin(request):
                return redirect('unauthorized')
            else:
                form = DriverForm(instance=driver)
        else:
            pass
        return render(request=request,
                      template_name='driver/driver_update.html', 
                      context={'driver':driver,'form':form})
    def post(self,request,driver_id=None):
        if driver_id:
            driver = Driver.objects.get(pk=driver_id)
        else:
            driver = Driver()
        form = DriverForm(request.POST,instance=driver)
        if form.is_valid():
            driver = form.save()
            return redirect(reverse('driver_list'))
        return render(request=request,
                      template_name='driver/driver_update.html', 
                      context={'driver':driver,'form':form})
        

class DriverDetailView(LoginRequiredMixin, View):
    def get(self,request,driver_id=None):
        driver = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            driver = Driver.objects.get(pk = driver_id)
        return render(request=request,
                      template_name='driver/driver_details.html', 
                      context={'driver':driver})



#-----Vehicle Crud ------
class VehicleAdd(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'driver/vehicle_add.html', {'form': VehicleForm()})
        else:
            return redirect(reverse('login')) 

    def post(self, request):
        if request.user.is_authenticated:
            form = VehicleForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('personalinfo')
            return render(request, 'driver/vehicle_add.html', {'form': form})
        else:
            return redirect(reverse('login')) 


class VehicleList(LoginRequiredMixin, View):
    def get(self, request):
        vehicles = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            vehicles = Vehicle.objects.all()
        return render(request=request,
                      template_name='driver/vehicle_list.html', 
                      context={'vehicles': vehicles})


class VehicleDelete(LoginRequiredMixin, View):
    def get(self,request,vehicle_id=None):
        if vehicle_id:
            vehicle = Vehicle.objects.get(pk=vehicle_id)
        else:
            vehicle = Vehicle()
        form = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            form = VehicleForm(instance=vehicle)
        for field in form.fields:
            form.fields[field].widget.attrs['disabled'] = True
        vehicle_list = Vehicle.objects.all()
        return render(request=request,
                      template_name='driver/vehicle_delete.html', 
                      context={'vehicle': vehicle,'form':form, 'vehicle_list':vehicle_list})
    def post(self,request,vehicle_id=None):
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        form = VehicleForm(request.POST,instance=vehicle)
        vehicle.delete()
        return redirect(reverse('vehicle_list'))


class VehicleUpdate(LoginRequiredMixin, View):
    def get(self,request,vehicle_id=None):
        if vehicle_id:
            vehicle = Vehicle.objects.get(pk=vehicle_id)
            form = None
            if not admin(request):
                return redirect('unauthorized')
            else:
                form = VehicleForm(instance=vehicle)
        else:
            pass
        return render(request=request,
                      template_name='driver/vehicle_update.html', 
                      context={'vehicle': vehicle,'form':form})
    def post(self,request,vehicle_id=None):
        if vehicle_id:
            vehicle = Vehicle.objects.get(pk=vehicle_id)
        else:
            vehicle = Vehicle()
        form = VehicleForm(request.POST,instance=vehicle)
        if form.is_valid():
            vehicle = form.save()
            return redirect(reverse('vehicle_list'))
        return render(request=request,
                      template_name='driver/vehicle_update.html', 
                      context={'vehicle':vehicle,'form':form})


class VehicleDetails(LoginRequiredMixin, View):
    def get(self,request,vehicle_id=None):
        vehicle = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            vehicle = Vehicle.objects.get(pk=vehicle_id)
        return render(request=request,
                      template_name='driver/vehicle_details.html', 
                      context={'vehicle':vehicle})



#----- Violation Crud -----
class ViolationList(LoginRequiredMixin, View):
    def get(self, request):
        violations = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            violations = Violation.objects.all()
        return render(request=request, 
                      template_name='driver/violation_list.html', 
                      context={'violations':violations})
    

class ViolationAdd(LoginRequiredMixin, View):
    def get(self, request):
        form = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            form = ViolationForm()
        return render(request=request,
                      template_name='driver/violation_add.html',
                      context={'form':form})
    def post(self, request):
        form = ViolationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("violation_list"))
        return render(request=request,
                      template_name='driver/violation_add.html',
                      context={'form':form})


class ViolationDelete(LoginRequiredMixin, View):
    def get(self,request,violation_id=None):
        if violation_id:
            violation = Violation.objects.get(pk=violation_id)
        else:
            violation = Violation()
        form = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            form = ViolationForm(instance=violation)
        for field in form.fields:
            form.fields[field].widget.attrs['disabled'] = True
        violation_list = Violation.objects.all()
        return render(request=request,
                      template_name='driver/violation_delete.html',
                      context={'violation':violation,'form':form,'violation_list':violation_list})
    def post(self,request,violation_id=None):
        violation = Violation.objects.get(pk=violation_id)   
        form = ViolationForm(request.POST,instance=violation)
        violation.delete()
        return redirect(reverse("violation_list"))


class ViolationUpdate(LoginRequiredMixin, View):
    def get(self,request,violation_id=None):
        if violation_id:
            violation = Violation.objects.get(pk=violation_id)
            form = None
            if not admin(request):
                return redirect('unauthorized')
            else:
                form = ViolationForm(instance=violation)
        else:
            pass
        return render(request=request,
                      template_name='driver/violation_update.html', 
                      context={'violation': violation,'form':form})
    def post(self,request,violation_id=None):
        if violation_id:
            violation = Violation.objects.get(pk=violation_id)
        else:
            violation = Violation()
        form = ViolationForm(request.POST,instance=violation)
        if form.is_valid():
            violation = form.save()
            return redirect(reverse('violation_list'))
        return render(request=request,
                      template_name='driver/violation_update.html', 
                      context={'violation':violation,'form':form})


class ViolationDetails(LoginRequiredMixin, View):
    def get(self,request,violation_id=None):
        violation = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            violation = Violation.objects.get(pk=violation_id)
        return render(request=request,
                      template_name='driver/violation_details.html', 
                      context={'violation':violation})
    


#-----Permit Crud -----
class PermitAdd(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'driver/permit_add.html', {'form': PermitForm()})
        else:
            return redirect(reverse('login')) 

    def post(self, request):
        if request.user.is_authenticated:
            form = PermitForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('personalinfo')
            return render(request, 'driver/permit_add.html', {'form': form})
        else:
            return redirect(reverse('login')) 


class PermitList(LoginRequiredMixin, View):
    def get(self, request):
        permits = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            permits = Permit.objects.all()
        return render(request=request,
                      template_name='driver/permit_list.html', 
                      context={'permits': permits})


class PermitDelete(LoginRequiredMixin, View):
    def get(self,request,permit_id=None):
        if permit_id:
            permit = Permit.objects.get(pk=permit_id)
        else:
            permit = Permit()
        form = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            form = PermitForm(instance=permit)
        for field in form.fields:
            form.fields[field].widget.attrs['disabled'] = True
        permit_list = Permit.objects.all()
        return render(request=request,
                      template_name='driver/permit_delete.html', 
                      context={'permit': permit,'form':form, 'permit_list':permit_list})
    def post(self,request,permit_id=None):
        permit = Permit.objects.get(pk=permit_id)
        form = PermitForm(request.POST,instance=permit)
        permit.delete()
        return redirect(reverse('permit_list'))


class PermitUpdate(LoginRequiredMixin, View):
    def get(self,request,permit_id=None):
        if permit_id:
            permit = Permit.objects.get(pk=permit_id)
        else:
            permit = Permit()
        form = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            form = PermitForm(instance=permit)
        permits = Permit.objects.all()
        return render(request=request,
                      template_name='driver/permit_update.html', 
                      context={'permit': permit,'form':form, 'permits':permits})
    def post(self,request,permit_id=None):
        if permit_id:
            permit = Permit.objects.get(pk=permit_id)
        else:
            permit = Permit()
        form = PermitForm(request.POST,instance=permit)
        if form.is_valid():
            permit = form.save()
            return redirect(reverse('permit_list'))
        return render(request=request,
                      template_name='driver/permit_update.html', 
                      context={'permit':permit,'form':form})
    
class PaymentList(LoginRequiredMixin, View):
    def get(self, request):
        payments = None
        total_payment_sum = None
        if not admin(request):
            return redirect('unauthorized')
        else:
            payments = Payment.objects.all()
            total_payment_sum = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        return render(request=request,
                      template_name='driver/payment_list.html',
                      context={'payments': payments, 'total_payment_sum': total_payment_sum})