from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Order)

admin.site.register(Stops)
admin.site.register(Transport)
admin.site.register(Bus)
admin.site.register(Train)
admin.site.register(JourneyPrices)
admin.site.register(Seat)
admin.site.register(Meal)
admin.site.register(Journey)
admin.site.register(JourneyStage)
admin.site.register(JourneySchedule)
admin.site.register(Passenger)
admin.site.register(DetailFoodOrder)
admin.site.register(DetailsProductOrder)
admin.site.register(PurchaseReceipt)
admin.site.register(Payments)


class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ["price"]


class TicketSalesAdmin(admin.ModelAdmin):
    readonly_fields = ["price", "purchase_date"]


admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketSales, TicketSalesAdmin)
