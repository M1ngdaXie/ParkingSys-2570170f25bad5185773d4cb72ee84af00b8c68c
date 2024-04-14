from django import forms
from .models import Driver, Vehicle, Payment, Violation, Permit

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['credit_card_no', 'amount', 'check_no', 'cash', 'date']


class ViolationForm(forms.ModelForm):
    class Meta:
        model = Violation
        fields = '__all__'
        widgets = {
            'violation_type': forms.CheckboxSelectMultiple
        }


class PermitForm(forms.ModelForm):
    class Meta:
        model = Permit
        fields = '__all__'
        widgets = {
            'cost': forms.HiddenInput(),
            'expiration_date': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'amount_due': forms.HiddenInput(),
        }