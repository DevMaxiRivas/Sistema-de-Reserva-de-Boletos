from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User

# Traducciones
from django.utils.translation import gettext_lazy as _

# Horarios
from django.utils import timezone
from django.utils.timezone import make_aware

# DataBase
from django.db.models import Count, Sum, Avg, F
from django.db.models.functions import TruncMonth, ExtractYear, ExtractHour, ExtractWeekDay

# Fechas
from datetime import datetime
from django.utils.timezone import now

# Modelos
from django.db.models import Avg, IntegerField, FloatField
from django.db.models.functions import Cast

def toStringDate_Hour(date, minutes):
        return (timezone.localtime(date) - timedelta(minutes=minutes)).strftime("%H:%M")

STATES1 = (
    ("h", _("Habilitado")),
    ("d", _("Deshabilitado")),
)

url_website = "http://127.0.0.1:8000/"

class Stops(models.Model):
    TYPES = (
            ("b", _("Bus")),
            ("t", _("Train")),
    )
    
    name = models.CharField(verbose_name=_("name"), max_length=100)
    location = models.CharField(verbose_name=_("location"), max_length=255)
    type = models.CharField(
        verbose_name=_("type"),
        max_length=1,
        choices=TYPES,
        blank=True,
        default="t",
    )
    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )
    
    def getType(self):
        for tuple in self.TYPES:
            if self.type == tuple[0]:
                return f"{tuple[1]}"
        return self.type

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Stop")
        verbose_name_plural = _("Stops")

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.hab_pv)
        return None


class Transport(models.Model):
    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def __str__(self):
        if Train.objects.filter(transport=self).exists():
            return f"Train {Train.objects.get(transport=self).name}"
        elif Bus.objects.filter(transport=self).exists():
            return f"Bus {Bus.objects.get(transport=self).name}"
        else:
            return f"Transport {self.id}"

    # Funciones
    # def average_occupancy_by_transport():
    #     return Transport.objects.annotate(
    #         avg_occupancy=Avg(Cast('seats__ticket__id', output_field=IntegerField()) / Cast('seats__count', output_field=FloatField()))
    #     ).values('id', 'avg_occupancy')
    
class Train(models.Model):
    transport = models.ForeignKey(
        Transport,
        verbose_name=_("transport"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(verbose_name=_("name"), max_length=100)
    capacity = models.PositiveIntegerField(
        verbose_name=_("capacity"), blank=True, null=True
    )

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    def save(self, *args, **kwargs):
        if not self.transport:
            self.transport = Transport.objects.create()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Train")
        verbose_name_plural = _("Trains")

    def __str__(self):
        return self.name


class Bus(models.Model):
    transport = models.ForeignKey(
        Transport,
        verbose_name=_("transport"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(verbose_name=_("name"), max_length=100)
    capacity = models.PositiveIntegerField(
        verbose_name=_("capacity"), blank=True, null=True
    )
    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    class Meta:
        ordering = ["name"]
        verbose_name = _("Bus")
        verbose_name_plural = _("Buses")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.transport:
            self.transport = Transport.objects.create()
        super().save(*args, **kwargs)


class Journey(models.Model):
    JOURNEY_TYPE_CHOICES = [
        ("TRAIN_ONLY", _("Train Only")),
        ("BUS_AND_TRAIN", _("Bus and Train")),
    ]

    type = models.CharField(
        verbose_name=_("type"), max_length=20, choices=JOURNEY_TYPE_CHOICES
    )
    description = models.TextField(verbose_name=_("description"))

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )
    #Funciones
    def passengers_for_journey():
        return Journey.objects.values('type').annotate(
            total_passengers=Count('journeyschedule__ticket__passenger')
        )
    
    def revenue_by_journey_type():
        return Journey.objects.values('type').annotate(total_revenue=Sum('journeyschedule__ticket__price'))
    
    def get_start_and_end_stop(self):
        
        stop_departure, stop_arrival = (
            JourneyStage.objects.filter(journey=self).values('departure_stop').order_by("order").first(),
            JourneyStage.objects.filter(journey=self).values('arrival_stop').order_by("-order").first()
        )
        
        return (
            Stops.objects.get(id=stop_departure["departure_stop"]).name,
            Stops.objects.get(id=stop_arrival["arrival_stop"]).name,
        )
    
    def getType(type):
        for tuple in Journey.JOURNEY_TYPE_CHOICES:
            if type == tuple[0]:
                return f"{tuple[1]}"
        return type
    
    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    class Meta:
        ordering = ["type"]
        verbose_name = _("Journey")
        verbose_name_plural = _("Journeys")

    def __str__(self):
        for tuple in self.JOURNEY_TYPE_CHOICES:
            if self.type == tuple[0]:
                return f"{tuple[1]}"
        return self.type

class JourneyPrices(models.Model):
    journey = models.ForeignKey(
        Journey,
        verbose_name=_("journey"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    description = models.TextField(verbose_name=_("description"), blank=True)
    CATEGORIES = (
        ("standar", _("Standar")),
        ("vip", _("VIP")),
        ("ejecutive", _("Ejecutive")),
    )

    category = models.CharField(
        verbose_name=_("category"),
        max_length=50,
        choices=CATEGORIES,
        blank=True,
        default="cash",
        help_text=_("Category"),
    )
    price = models.DecimalField(
        verbose_name=_("price"), max_digits=10, decimal_places=2
    )

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:

            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    class Meta:
        ordering = ["category"]
        verbose_name = _("Journey Price")
        verbose_name_plural = _("Journey Prices")

    # Funciones
    def getCategory(self):
        for tuple in self.CATEGORIES:
            if self.category == tuple[0]:
                return f"{tuple[1]}"
        return self.category

    def average_journey_prices_by_type():
        return JourneyPrices.objects.values('journey__type', 'category').annotate(avg_price=Avg('price'))

    def __str__(self):
        return self.getCategory() + "-" + str(self.journey)

class Seat(models.Model):
    transport = models.ForeignKey(
        Transport,
        verbose_name=_("transport"),
        related_name="seats",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    seat_number = models.CharField(verbose_name=_("seat_number"), max_length=10)
    CATEGORIES = (
        ("standar", _("Standar")),
        ("vip", _("VIP")),
        ("ejecutive", _("Ejecutive")),
    )

    category = models.CharField(
        verbose_name=_("type"),
        max_length=50,
        choices=CATEGORIES,
        blank=True,
        default="cash",
        help_text=_("Seat Category"),
    )

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:

            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    # def save(self, *args, **kwargs):
    #         # Si es el mismo asiento con el que se creo la venta no modificar el precio
    #         if self._state.adding:
    #             if self.ve_bl:
    #                 self.cli_bl = self.ve_bl.cli_ve
    #                 self.evt_bl = self.ve_bl.evt_ve

    #         super().save(*args, **kwargs)

    class Meta:
        ordering = ["seat_number"]
        verbose_name = _("Seat")
        verbose_name_plural = _("Seats")

    # Funciones
    def getCategory(self):
        for tuple in self.CATEGORIES:
            if self.category == tuple[0]:
                return f"{tuple[1]}"
        return self.category
    
    def getCategory2(category):
        for tuple in Seat.CATEGORIES:
            if category == tuple[0]:
                return f"{tuple[1]}"
        return category
    
    def sales_by_seat_category():
        return Seat.objects.values('category').annotate(total_sales=Sum('ticket__price'))
    
    def seat_distribution_in_trains():
        return Seat.objects.filter(transport__train__isnull=False).values('category').annotate(count=Count('id'))
    
    def __str__(self):
        return f"{self.seat_number} ({self.getCategory()})"


class MealCategory(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=50, null=True)
    description = models.TextField(verbose_name=_("description"), null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = _("Meal Category")
        verbose_name_plural = _("Meal Categories")


class Meal(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=100)
    category = models.ForeignKey(
        MealCategory,
        verbose_name=_("category"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    description = models.TextField(verbose_name=_("description"), null=True)
    price = models.DecimalField(
        verbose_name=_("price"), max_digits=10, decimal_places=2
    )

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Meal")
        verbose_name_plural = _("Meals")

    def __str__(self):
        return self.name

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None


class ProductCategory(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=50, null=True)
    description = models.TextField(verbose_name=_("description"), null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")


class Product(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=100, null=True)
    price = models.DecimalField(
        verbose_name=_("price"), max_digits=10, decimal_places=2, default=0
    )
    description = models.TextField(verbose_name=_("description"), null=True)
    stock = models.PositiveIntegerField(verbose_name=_("stock"), default=1)
    category = models.ForeignKey(
        ProductCategory, verbose_name=_("category"), on_delete=models.CASCADE, null=True
    )
    state = models.CharField(
        verbose_name=_("state"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        
        return f"{self.name}"
    
    # Funciones
    def update_stock(self, quantity):
        self.stock -= quantity
        self.save()
        
    def getStock(self):
        return self.stock


class Order(models.Model):
    name = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.customer}-{self.name}"



class JourneyStage(models.Model):
    journey = models.ForeignKey(
        Journey,
        verbose_name=_("journey"),
        related_name="stages",
        on_delete=models.CASCADE,
    )
    order = models.PositiveIntegerField()
    departure_stop = models.ForeignKey(
        Stops,
        verbose_name=_("departure_stop"),
        related_name="start_stages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    arrival_stop = models.ForeignKey(
        Stops,
        verbose_name=_("arrival_stop"),
        related_name="end_stages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    transport = models.ForeignKey(
        Transport,
        verbose_name=_("transport"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    duration = models.DurationField(verbose_name=_("duration"))

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    class Meta:
        ordering = ["order"]
        verbose_name = _("Journey Stage")
        verbose_name_plural = _("Journey Stages")

    def __str__(self):
        return f"{self.journey} - Stage {self.order}"


class JourneySchedule(models.Model):
    journey = models.ForeignKey(
        Journey, verbose_name=_("journey"), on_delete=models.CASCADE
    )
    departure_time = models.DateTimeField(verbose_name=_("departure_time"))
    arrival_time = models.DateTimeField(verbose_name=_("arrival_time"))
    principal_transport = models.ForeignKey(
        Transport, verbose_name=_("principal_transport"), on_delete=models.CASCADE, null=True, blank=True
    )

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    class Meta:
        ordering = ["journey"]
        verbose_name = _("Journey Schedule")
        verbose_name_plural = _("Journey Schedules")

    def __str__(self):
        return f"{self.journey} - {timezone.localtime(self.departure_time).strftime("%Y-%m-%d %H:%M")}"
    
    # Funciones
    
    def getDataSchedule(self):
        (stop_departure, stop_arrival) = self.journey.get_start_and_end_stop()
        
        return {
            "EstacionSalida": stop_departure,
            "HorarioPartida": toStringDate_Hour(self.departure_time, 0),
            "EstacionLlegada": stop_arrival,
            "HorarioLlegada": toStringDate_Hour(self.arrival_time, 0),
            "HorarioEspera": toStringDate_Hour(self.departure_time, 40),
            "HorarioSalida": toStringDate_Hour(self.departure_time, 0),
        }
        
    def getSchedules(type, date):
        # Convertir la fecha a un objeto datetime
        data_datetime = make_aware(datetime.strptime(date, "%Y-%m-%d"))
        # Realizar la consulta
        schedules = JourneySchedule.objects.filter(
            departure_time__gte=data_datetime, journey__type=type
        ).order_by('departure_time')

        list = []
        for schedule in schedules:
            list.append({
                "id" : schedule.id,
                "departure_time": timezone.localtime(schedule.departure_time).strftime("%Y-%m-%d %H:%M"),
                "arrival_time": timezone.localtime(schedule.arrival_time).strftime("%Y-%m-%d %H:%M"),
            })
        return list
    
    
    def top_5_popular_routes():
        return JourneySchedule.objects.values('journey__type').annotate(ticket_count=Count('ticket')).order_by('-ticket_count')[:5]
    
    # def occupancy_rate_by_journey():
    #     return JourneySchedule.objects.annotate(
    #         occupancy_rate=Count('ticket') / Cast(F('journey__stages__transport__seats__count'), output_field=FloatField())
    #     ).values('journey__type', 'occupancy_rate')

    def departure_time_distribution():
        return JourneySchedule.objects.annotate(
            hour=ExtractHour('departure_time')
        ).values('hour').annotate(count=Count('id')).order_by('hour')
        
    def journey_distribution_by_weekday():
        return JourneySchedule.objects.annotate(
            weekday=ExtractWeekDay('departure_time')
        ).values('weekday').annotate(count=Count('id')).order_by('weekday')
        
        
class Passenger(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=100)
    dni_or_passport = models.CharField(verbose_name=_("dni_or_passport"), max_length=50)
    origin_country = models.CharField(verbose_name=_("origin_country"), max_length=100)
    emergency_telephone = models.CharField(
        verbose_name=_("emergency_telephone"), max_length=50, null=True, blank=True
    )
    date_of_birth = models.DateField(
        verbose_name=_("date_of_birth"), null=True, blank=True
    )
    # Telefono (Emergencia)
    # Fecha de Nacimiento
    GENDER = (
        ("m", _("Male")),
        ("w", _("Female")),
    )

    gender = models.CharField(
        verbose_name=_("gender"),
        max_length=1,
        choices=GENDER,
        blank=True,
        default="m",
        help_text="Genero del pasajero",
    )

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    class Meta:
        ordering = ["dni_or_passport"]
        verbose_name = _("Passenger")
        verbose_name_plural = _("Passengers")

    def __str__(self):
        return self.name
    
    # Funciones
    def passengers_by_gender():
        return Passenger.objects.values('gender').annotate(count=Count('id'))
    
    def passengers_by_origin_country():
        return Passenger.objects.values('origin_country').annotate(count=Count('id'))
    
    def passenger_age_distribution():
        return Passenger.objects.annotate(
            age=ExtractYear(now()) - ExtractYear('date_of_birth')
        ).values('age').annotate(count=Count('id'))
        
    def getGender(type):
        for tuple in Passenger.GENDER:
            if type == tuple[0]:
                return f"{tuple[1]}"
        return type

class Payments(models.Model):
    voucher_no = models.CharField(verbose_name=_("voucher_no"), max_length=255, blank=True, null=True)
    TYPES = (
        ("credit_card", _("Credit Card")),
        ("debit_card", _("Debit Card")),
        ("account_money", _("Account Money MP")),
        ("cash", _("Cash")),
    )

    type = models.CharField(
        verbose_name=_("type"),
        max_length=50,
        choices=TYPES,
        blank=True,
        default="cash",
        help_text=_("Payment Type"),
    )
    status = models.CharField(
        verbose_name=_("payment_status"), max_length=50, null=True, blank=True, default="success"
    )

    created_at = models.DateTimeField(verbose_name=_("created_at"), auto_now_add=True)
    
    # Funciones
    
    def sales_by_payment_type():
        return Payments.objects.values('type').annotate(count=Count('id'), total=Sum('ticketsales__price'))

    def getType(self):
        for tuple in self.TYPES:
            if self.type == tuple[0]:
                return f"{tuple[1]}"
        return self.type
    
    def renameType(type):
        for tuple in Payments.TYPES:
            if type == tuple[0]:
                return f"{tuple[1]}"
        return type

    def __str__(self):
        if self.voucher_no and self.type:
            return f"Pago {self.voucher_no} - {self.type} - {timezone.localtime(self.created_at).strftime("%Y-%m-%d %H:%M")}"
        return "Pago - " + timezone.localtime(self.created_at).strftime("%Y-%m-%d %H:%M")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Payments")
        verbose_name_plural = _("Payments")


class TicketSales(models.Model):
    email = models.EmailField(verbose_name=_("email"), null=True, blank=True)
    user = models.ForeignKey(
        User, verbose_name=_("user"), on_delete=models.SET_NULL, null=True, blank=True
    )
    price = models.DecimalField(
        verbose_name=_("price"), max_digits=10, decimal_places=2, default=0
    )
    purchase_date = models.DateTimeField(
        verbose_name=_("purchase_date"), default=timezone.now
    )
    payment = models.ForeignKey(
        Payments,
        verbose_name=_("payment"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    
    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    def update_total_price(self):
        self.price = sum(ticket.price for ticket in self.tickets.all())
        self.save()

    def __str__(self):
        if self.user:
            return f"Sale for {self.user.username} on {timezone.localtime(self.purchase_date).strftime("%Y-%m-%d %H:%M")}"
        return f"Sale on {timezone.localtime(self.purchase_date).strftime("%Y-%m-%d %H:%M")}"
        
    
    # Funciones
    def ventas_por_año():
        hace_un_año = timezone.now() - timedelta(days=365)
        ventas = TicketSales.objects.filter(purchase_date__gte=hace_un_año)
        ventas_por_mes = ventas.annotate(mes=TruncMonth('purchase_date')).values('mes').annotate(cantidad=Count('id')).order_by('mes')
        return ventas_por_mes
    
    def sales_by_hour():
        return TicketSales.objects.annotate(hour=ExtractHour('purchase_date')).values('hour').annotate(total_sales=Count('id'))
    
    def average_revenue_per_sale():
        return TicketSales.objects.aggregate(avg_revenue=Avg('price'))
    
    def year_over_year_sales():
        return TicketSales.objects.annotate(
            year=ExtractYear('purchase_date')
        ).values('year').annotate(total_sales=Sum('price')).order_by('year')

    class Meta:
        ordering = ["-purchase_date"]
        verbose_name = _("Ticket Sale")
        verbose_name_plural = _("Ticket Sales")


class Ticket(models.Model):
    sale = models.ForeignKey(
        TicketSales,
        verbose_name=_("sale"),
        related_name="tickets",
        on_delete=models.CASCADE,
    )
    passenger = models.ForeignKey(
        Passenger, verbose_name=_("passenger"), on_delete=models.CASCADE
    )
    schedule = models.ForeignKey(
        JourneySchedule, verbose_name=_("schedule"), on_delete=models.CASCADE
    )
    seat = models.ForeignKey(Seat, verbose_name=_("seat"), on_delete=models.CASCADE)
    price = models.DecimalField(
        verbose_name=_("price"), max_digits=10, decimal_places=2, default=0
    )
    assistance = models.BooleanField(verbose_name=_("assistance"), default=False)
    
    # Funciones
    def revenue_by_seat_category():
        return Ticket.objects.values('seat__category__type').annotate(total_ingresos=Sum('price')).order_by('-total_ingresos')
    
    def getCategorySeat(self):
        return self.seat.getCategory()
    
    # Datos
    def getDataPublic(self):
        (stop_departure, stop_arrival) = self.schedule.journey.get_start_and_end_stop()
        
        return {
            "IdVenta": str(self.sale.id),
            "NombrePasajero": self.passenger.name,
            "IdTicket": str(self.id),
            "FechaBoleto": self.schedule.departure_time.strftime("%d/%m/%Y"),
            "EstacionSalida": stop_departure,
            "HorarioPartida": toStringDate_Hour(self.schedule.departure_time, 0),
            "EstacionLlegada": stop_arrival,
            "HorarioLlegada": toStringDate_Hour(self.schedule.arrival_time, 0),
            "IdAsiento": str(self.seat.seat_number),
            "CategoriaAsiento": str(self.seat.getCategory()),
            "HorarioEspera": toStringDate_Hour(self.schedule.departure_time, 40),
            "HorarioSalida": toStringDate_Hour(self.schedule.departure_time, 0),
            "EnlaceWeb": f"{url_website}ticket-data/{self.id}",
        }

    # Funcion para reservar el asiento
    # def reserveSeat(self):
    #     asiento = self.seat
    #     asiento.status = "v"
    #     asiento.save()

    def save(self, *args, **kwargs):
        # Si es el mismo asiento con el que se creo la venta no modificar el precio
        if self._state.adding:
            if self.seat:
                self.price = JourneyPrices.objects.filter(category = self.seat.category).first().price
        # Sino es el mismo asiento con el que se creo la venta modificar el precio de la venta al precio del asiento nuevo seleccionado.
        else:
            # Si el objeto ya existe en la base de datos
            old_instance = Ticket.objects.get(pk=self.pk)
            if old_instance.seat != self.seat:
                self.price = JourneyPrices.objects.filter(category = self.seat.category).first().price

        # self.reserveSeat()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Cambiar el campo status del asiento asociado a 'h' antes de eliminar el ticket
        self.seat.status = "h"
        self.seat.save()
        super().delete(*args, **kwargs)

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    def __str__(self):
        return f"Ticket for {self.passenger.name} - schedule {self.schedule.journey.type}"

    class Meta:
        ordering = ["-id"]
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")


class PurchaseReceipt(models.Model):
    passenger = models.ForeignKey(
        Passenger,
        verbose_name=_("passenger"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        verbose_name=_("price"), max_digits=10, decimal_places=2, default=0
    )
    purchase_date = models.DateTimeField(
        verbose_name=_("purchase_date"), default=timezone.now
    )
    payment = models.ForeignKey(
        Payments,
        verbose_name=_("payment"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    def update_total_price(self):
        self.price = sum(meal.unit_price * meal.quantity for meal in self.meals.all())
        self.save()

    def update_total_price_of_product(self):
        self.price = sum(
            product.unit_price * product.quantity for product in self.products.all()
        )
        self.save()

    def __str__(self):
        if self.passenger:
            return f"Sale for {self.passenger.name} on {self.purchase_date}"
        return f"Sale on {self.purchase_date}"

    class Meta:
        ordering = ["purchase_date"]
        verbose_name = _("Purchase Receipt")
        verbose_name_plural = _("Purchase Receipts")


class DetailFoodOrder(models.Model):
    receipt = models.ForeignKey(
        PurchaseReceipt,
        verbose_name=_("receipt"),
        related_name="meals",
        on_delete=models.CASCADE,
    )
    meal = models.ForeignKey(Meal, verbose_name=_("meal"), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name=_("quantity"), default=1)
    unit_price = models.DecimalField(
        verbose_name=_("unit_price"), max_digits=10, decimal_places=2, default=0
    )
    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )

    def delete(self, *args, **kwargs):
        # Cambiar el campo status del asiento asociado a 'h' antes de eliminar el ticket
        self.receipt.price = self.receipt.price - self.unit_price * self.quantity
        self.receipt.save()
        super().delete(*args, **kwargs)

    def update_receipt(self):
        receipt = self.receipt
        receipt.price = receipt.price + (self.unit_price * self.quantity)
        receipt.save()

    def save(self, *args, **kwargs):
        # Si es el mismo asiento con el que se creo la venta no modificar el precio
        if self._state.adding:
            if self.meal:
                self.unit_price = self.meal.price
                self.update_receipt()

        # Sino es el mismo asiento con el que se creo la venta modificar el precio de la venta al precio del asiento nuevo seleccionado.
        else:
            # Si el objeto ya existe en la base de datos
            old_instance = DetailFoodOrder.objects.get(pk=self.pk)
            if old_instance.meal != self.meal:
                # Quitar mercaderia del recibo
                self.receipt.price = self.receipt.price - (
                    old_instance.unit_price * old_instance.quantity
                )
                self.unit_price = self.meal.price
                self.update_receipt()

        super().save(*args, **kwargs)

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    def __str__(self):
        return f"{self.quantity} x {self.meal.name}"

    class Meta:
        ordering = ["receipt"]
        verbose_name = _("Detail Food Order")
        verbose_name_plural = _("Detail Food Orders")
        
    # Funciones
    def monthly_food_sales():
        return DetailFoodOrder.objects.annotate(month=TruncMonth('receipt__purchase_date')).values('month').annotate(total_sales=Sum('unit_price'))
    
    def sales_by_meal_category():
        return DetailFoodOrder.objects.values('meal__category__name').annotate(total_sales=Sum('unit_price'))
    

class DetailsProductOrder(models.Model):
    receipt = models.ForeignKey(
        PurchaseReceipt,
        verbose_name=_("receipt"),
        related_name="products",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product, verbose_name=_("product"), on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(verbose_name=_("quantity"), default=1)
    unit_price = models.DecimalField(
        verbose_name=_("unit_price"), max_digits=10, decimal_places=2, default=0
    )

    status = models.CharField(
        verbose_name=_("status"),
        max_length=1,
        choices=STATES1,
        blank=True,
        default="h",
    )
    # Funciones
    def revenue_per_product():
        return DetailsProductOrder.objects.values('product__name').annotate(total_ingresos=Sum('unit_price * quantity')).order_by('-total_ingresos')

    def top_selling_products():
        return DetailsProductOrder.objects.values('product__name').annotate(total_sold=Sum('quantity')).order_by('-total_sold')[:10]

    def delete(self, *args, **kwargs):
        # Cambiar el campo status del asiento asociado a 'h' antes de eliminar el ticket
        self.receipt.price = self.receipt.price - self.unit_price * self.quantity
        self.receipt.save()
        super().delete(*args, **kwargs)

    def update_receipt(self):
        receipt = self.receipt
        receipt.price = receipt.price + (self.unit_price * self.quantity)
        receipt.save()

    def save(self, *args, **kwargs):
        # Si es el mismo asiento con el que se creo la venta no modificar el precio
        if self._state.adding:
            if self.product:
                self.unit_price = self.product.price
                self.update_receipt()

        # Sino es el mismo asiento con el que se creo la venta modificar el precio de la venta al precio del asiento nuevo seleccionado.
        else:
            # Si el objeto ya existe en la base de datos
            old_instance = DetailsProductOrder.objects.get(pk=self.pk)
            if old_instance.product != self.product:
                # Quitar mercaderia del recibo
                self.receipt.price = self.receipt.price - (
                    old_instance.unit_price * old_instance.quantity
                )
                self.unit_price = self.product.price
                self.update_receipt()

        super().save(*args, **kwargs)

    def status_sample(self):
        if self.status:
            STATES = set(STATES1)
            # Retornar el valor correspondiente
            return STATES.get(self.status)
        return None

    class Meta:
        ordering = ["receipt"]
        verbose_name = _("Details Product Order")
        verbose_name_plural = _("Details Product Orders")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
