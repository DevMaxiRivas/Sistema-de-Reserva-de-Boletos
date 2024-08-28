from django import forms
from django.forms.widgets import NumberInput

# Autenticacion
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Formularios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder

# Modelos
from .models import *

# Vistas
from django.forms import modelformset_factory
from django.forms import inlineformset_factory

# Traducciones
from django.utils.translation import gettext_lazy as _

# Roles
from django.contrib.auth.models import Group


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ["name", "order_quantity"]


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label=_("Correo electrónico"))
    first_name = forms.CharField(label=_("Nombre"))
    last_name = forms.CharField(label=_("Apellido"))

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
        labels = {
            "username": _("Username"),
            "email": _("email"),
            "first_name": _("first name"),
            "last_name": _("last name"),
            "password1": _("password"),
            "password2": _("confirm password"),
        }

    def clean_email(self):
        email_field = self.cleaned_data["email"]

        if User.objects.filter(email=email_field).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado")

        return email_field


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = [
            "name",
            "dni_or_passport",
            "emergency_telephone",
            "date_of_birth",
            "gender",
            "origin_country",
        ]
        labels = {
            "name": _("Name"),
            "dni_or_passport": _("DNI/Passport"),
            "emergency_telephone": _("Emergency Telephone"),
            "date_of_birth": _("Date of Birth"),
            "gender": _("Gender"),
            "origin_country": _("Origin Country"),
        }
        widgets = {
            "date_of_birth": NumberInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save"))


class TicketSalesForm(forms.ModelForm):
    email = forms.EmailField(required=False, label=_("Email (if not logged in)"))

    class Meta:
        model = TicketSales
        fields = [
            "email",
        ]
        labels = {
            "email": _("Email"),
        }


class TicketForm(forms.ModelForm):
    dni_or_passport = forms.CharField(
        max_length=50,
        label=_("DNI/Passport"),
        widget=forms.TextInput(attrs={"class": "dni_or_passport"}),
    )

    class Meta:
        model = Ticket
        fields = ["dni_or_passport", "schedule", "seat"]
        labels = {
            "dni_or_passport": _("DNI/Passport"),
            "schedule": _("Schedule"),
            "seat": _("Seat"),
        }


TicketFormSet = inlineformset_factory(
    TicketSales,
    Ticket,
    form=TicketForm,
    fields=["dni_or_passport", "schedule", "seat"],
    extra=1,
    can_delete=True,
)


class TicketFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "post"
        self.layout = Layout(
            Fieldset("Tickets", "passenger", "schedule", "seat"),
            ButtonHolder(
                Submit("submit", "Purchase Tickets", css_class="btn btn-primary")
            ),
        )
        self.render_required_fields = True
        self.form_tag = True


class PurchaseReceiptForm(forms.ModelForm):
    dni_or_passport = forms.CharField(max_length=50, label="DNI/Passport")

    class Meta:
        model = PurchaseReceipt
        fields = [
            "dni_or_passport",
        ]
        labels = {
            "dni_or_passport": _("DNI/Passport"),
        }


class DetailFoodOrderForm(forms.ModelForm):
    class Meta:
        model = DetailFoodOrder
        fields = ["meal", "quantity"]
        labels = {
            "meal": _("Meal"),
            "quantity": _("Quantity"),
        }


DetailFoodOrderFormSet = inlineformset_factory(
    PurchaseReceipt,
    DetailFoodOrder,
    form=DetailFoodOrderForm,
    fields=["meal", "quantity"],
    extra=1,
    can_delete=True,
)


class DetailsProductOrderForm(forms.ModelForm):
    class Meta:
        model = DetailsProductOrder
        fields = ["product", "quantity"]
        labels = {
            "product": _("product"),
            "quantity": _("Quantity"),
        }


DetailsProductOrderSet = inlineformset_factory(
    PurchaseReceipt,
    DetailsProductOrder,
    form=DetailsProductOrderForm,
    fields=["product", "quantity"],
    extra=1,
    can_delete=True,
)


class JourneyScheduleForm(forms.ModelForm):
    class Meta:
        model = JourneySchedule
        fields = [
            "journey",
            "departure_time",
            "arrival_time",
            "principal_transport",
        ]
        labels = {
            "journey": _("Journey"),
            "departure_time": _("Departure Time"),
            "arrival_time": _("Arrival Time"),
            "principal_transport": _("Principal Transport"),
        }
        widgets = {
            "departure_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "arrival_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "category",
            "stock",
            "description",
        ]
        labels = {
            "name": _("Name"),
            "price": _("Price"),
            "category": _("Category"),
            "stock": _("Stock"),
            "description": _("Description"),
        }


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = [
            "name",
            "category",
            "price",
        ]
        labels = {
            "name": _("Name"),
            "category": _("Category"),
            "price": _("Price"),
        }


class MealCategoryForm(forms.ModelForm):
    class Meta:
        model = MealCategory
        fields = [
            "name",
            "description",
        ]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
        }


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = [
            "name",
            "description",
        ]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
        }


class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = [
            "name",
            "capacity",
        ]
        labels = {
            "name": _("Name"),
            "capacity": _("Capacity"),
        }


class TrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = [
            "name",
            "capacity",
        ]
        labels = {
            "name": _("Name"),
            "capacity": _("Capacity"),
        }


class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = [
            "transport",
            "seat_number",
            "category",
        ]
        labels = {
            "transport": _("Transport"),
            "seat_number": _("Seat Number"),
            "category": _("Category"),
        }


class JourneyPricesForm(forms.ModelForm):
    class Meta:
        model = JourneyPrices
        fields = [
            "journey",
            "description",
            "category",
            "price",
        ]
        labels = {
            "journey": _("Journey"),
            "description": _("Description"),
            "category": _("Category"),
            "price": _("Price"),
        }


class JourneyForm(forms.ModelForm):
    class Meta:
        model = Journey
        fields = [
            "type",
            "description",
        ]
        labels = {
            "type": _("Type"),
            "description": _("Description"),
        }


class JourneyStageForm(forms.ModelForm):
    class Meta:
        model = JourneyStage
        fields = [
            "journey",
            "order",
            "departure_stop",
            "arrival_stop",
            "transport",
            "duration",
        ]
        labels = {
            "journey": _("Journey"),
            "order": _("Order"),
            "departure_stop": _("Departure Stop"),
            "arrival_stop": _("Arrival Stop"),
            "transport": _("Transport"),
            "duration": _("Duration"),
        }


class StopForm(forms.ModelForm):
    class Meta:
        model = Stops
        fields = [
            "name",
            "location",
            "type",
        ]
        labels = {
            "name": _("Name"),
            "location": _("Location"),
            "type": _("Type"),
        }


class ChangeUserGroupForm(forms.Form):
    GROUPS = (
        ("Admins", _("Admins")),
        ("Employees", _("Employees")),
        ("Customers", _("Customers")),
    )

    group = forms.ChoiceField(
        choices=GROUPS,
        label=_("Change Group"),
    )
    
    @classmethod
    def get_group_display(cls, group_value):
        return dict(cls.GROUPS).get(group_value, group_value)

    def __init__(self, *args, **kwargs):
        initial_group = kwargs.pop("initial_group", None)
        super(ChangeUserGroupForm, self).__init__(*args, **kwargs)
        if initial_group:
            self.fields['group'].initial = initial_group
