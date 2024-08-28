from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", views.index, name="home"),
    # CUSTOMERS
    path("customers_index/", views.index_customer, name="dashboard-customers-index"),
    path("customer_tickets/", views.customer_tickets, name="customer_tickets"),
    path(
        "customer_sale_detail/<int:sale_id>/",
        customer_sale_detail,
        name="customer_sale_detail",
    ),
    path(
        "change_passenger_ticket/",
        change_passenger_ticket,
        name="change_passenger_ticket",
    ),
    path(
        "ticket-data/<int:pk>/",
        views.ticket_data,
        name="ticket_data",
    ),
    path(
        "checkin-ticket/",
        views.checkin_ticket,
        name="checkin_ticket",
    ),
    # EMPLOYEES
    path("employee_index/", views.index_employee, name="dashboard-employee-index"),
    # PRODUCTS
    path("products/", views.products, name="dashboard-products"),
    path(
        "products/delete/<int:pk>/",
        views.product_delete,
        name="dashboard-product-delete",
    ),
    path("products/edit/<int:pk>/", views.product_edit, name="dashboard-product-edit"),
    path(
        "products/detail/<int:pk>/",
        views.product_detail,
        name="dashboard-products-detail",
    ),
    # VENTAS
    path("purchases/", views.purchases, name="dashboard-purchases"),
    path("sale/<int:sale_id>/", sale_detail, name="dashboard-sale_detail"),
    path(
        "purchase_detail/<int:sale_id>",
        views.purchase_detail,
        name="purchase_detail",
    ),
    # Recibos
    path("receipts/", views.receipts, name="dashboard-receipts"),
    path(
        "receipt_detail/<int:sale_id>/", receipt_detail, name="dashboard-receipt_detail"
    ),
    path(
        "receipt_payment/<int:sale_id>",
        views.receipt_payment,
        name="dashboard-receipt_payment",
    ),
    # PLATOS
    path("meals/", views.meals, name="dashboard-meals"),
    path("meals/edit/<int:pk>/", views.meal_edit, name="dashboard-meal-edit"),
    path(
        "meals/delete/<int:pk>/",
        views.meal_delete,
        name="dashboard-meal-delete",
    ),
    # ASIENTOS
    path("seats/", views.seats, name="dashboard-seats"),
    path(
        "seats/edit/<int:pk>/",
        views.seat_edit,
        name="dashboard-seat-edit",
    ),
    path(
        "seats/delete/<int:pk>/",
        views.seat_delete,
        name="dashboard-seat-delete",
    ),
    # COLECTIVOS
    path("buses/", views.buses, name="dashboard-buses"),
    path(
        "buses/edit/<int:pk>/",
        views.bus_edit,
        name="dashboard-bus-edit",
    ),
    path(
        "buses/delete/<int:pk>/",
        views.bus_delete,
        name="dashboard-bus-delete",
    ),
    # TRENES
    path("trains/", views.trains, name="dashboard-trains"),
    path(
        "trains/edit/<int:pk>/",
        views.train_edit,
        name="dashboard-train-edit",
    ),
    path(
        "trains/delete/<int:pk>/",
        views.train_delete,
        name="dashboard-train-delete",
    ),
    # TIPOS DE RECORRIDO
    path("types_journey/", views.types_journey, name="dashboard-types_journey"),
    path(
        "types_journey/edit/<int:pk>/",
        views.type_journey_edit,
        name="dashboard-type_journey-edit",
    ),
    path(
        "types_journey/delete/<int:pk>/",
        views.type_journey_delete,
        name="dashboard-type_journey-delete",
    ),
    # ETAPAS DE RECORRIDOS
    path("journey_stages/", views.journey_stages, name="dashboard-journey_stages"),
    path(
        "journey_stages/edit/<int:pk>/",
        views.journey_stage_edit,
        name="dashboard-journey_stage-edit",
    ),
    path(
        "journey_stages/delete/<int:pk>/",
        views.journey_stage_delete,
        name="dashboard-journey_stage-delete",
    ),
    # CRONOGRAMAS DE RECORRIDOS
    path(
        "journey_schedules/",
        views.journey_schedules,
        name="dashboard-journey_schedules",
    ),
    path(
        "journey_schedules/edit/<int:pk>/",
        views.journey_schedule_edit,
        name="dashboard-journey_schedule-edit",
    ),
    path(
        "journey_schedules/delete/<int:pk>/",
        views.journey_schedule_delete,
        name="dashboard-journey_schedule-delete",
    ),
    # PARADAS
    path("stops/", views.stops, name="dashboard-stops"),
    path(
        "stops/edit/<int:pk>/",
        views.stop_edit,
        name="dashboard-stop-edit",
    ),
    path(
        "stops/delete/<int:pk>/",
        views.stop_delete,
        name="dashboard-stop-delete",
    ),
    # CATEGORIAS DE PLATOS
    path("meal_categories/", views.meal_categories, name="dashboard-meal_categories"),
    path(
        "meal_categories/edit/<int:pk>/",
        views.meal_category_edit,
        name="dashboard-meal_category-edit",
    ),
    path(
        "meal_categories/delete/<int:pk>/",
        views.meal_category_delete,
        name="dashboard-meal_category-delete",
    ),
    # CATEGORIAS DE PRODUCTOS
    path(
        "product_categories/",
        views.product_categories,
        name="dashboard-product_categories",
    ),
    path(
        "product_categories/edit/<int:pk>/",
        views.product_category_edit,
        name="dashboard-product_category-edit",
    ),
    path(
        "product_categories/delete/<int:pk>/",
        views.product_category_delete,
        name="dashboard-product_category-delete",
    ),
    # PRECIOS POR RECORRIDO
    path("journey_prices/", views.journey_prices, name="dashboard-journey_prices"),
    path(
        "journey_prices/edit/<int:pk>/",
        views.journey_price_edit,
        name="dashboard-journey_price-edit",
    ),
    path(
        "journey_prices/delete/<int:pk>/",
        views.journey_price_delete,
        name="dashboard-journey_price-delete",
    ),
    # DASHBOARD DE USUARIOS
    path("customers/", views.customers, name="dashboard-customers"),
    path("employees/", views.employees, name="dashboard-employees"),
    path("admins/", views.admins, name="dashboard-admins"),
    path("passengers/", views.passengers, name="dashboard-passengers"),
    path(
        "passengers/edit/<int:pk>/",
        views.passenger_edit,
        name="dashboard-passenger-edit",
    ),
    path(
        "passengers/delete/<int:pk>/",
        views.passenger_delete,
        name="dashboard-passenger-delete",
    ),
    path(
        "user_detail/detail/<int:pk>/",
        views.user_detail,
        name="dashboard-user-detail",
    ),
    path("order/", views.order, name="dashboard-order"),
    # VENTA DE TICKETS
    path("purchase-tickets/", views.purchase_tickets, name="purchase_tickets"),
    path("tickets_reserve/", views.tickets_reserve, name="tickets_reserve"),
    # Pagos
    path("payments/", views.payments, name="dashboard-payments"),
    path("payment_success/", views.payment_success, name="payment_success"),
    path("payment_failed/", views.payment_failed, name="payment_failed"),
    path("payment_pending/", views.payment_pending, name="payment_pending"),
    # Pasajeros
    path("create_passenger/", views.create_passenger, name="create_passenger"),
    path("finances/", views.finances, name="dashboard-finances"),
    path("supplies/", views.supplies, name="dashboard-supplies"),
    path("journeys/", views.journeys, name="dashboard-journeys"),
    path("transports/", views.transports, name="dashboard-transports"),
    path("planning/", views.planning, name="dashboard-planning"),
    path("users/", views.users, name="dashboard-users"),
    path("prueba/", views.prueba, name="prueba"),
    # VENTAS DE PRODUCTOS
    path(
        "product_sales/", views.register_sales_products, name="dashboard-product-sales"
    ),
    path("meals_sales/", views.register_sales_meals, name="dashboard-meal-sales"),
    # APIS
    # API Products
    path(
        "api/product_categories/",
        views.api_product_categories,
        name="api_product_categories",
    ),
    path(
        "api/type_payment/",
        views.api_type_payment,
        name="api_type_payment",
    ),
    path(
        "api/products_per_category/",
        views.api_products_per_category,
        name="api_products_per_category",
    ),
    path(
        "api/register_sale_products/",
        views.api_register_sale_products,
        name="api_register_sale_products",
    ),
    # API Meals
    path(
        "api/meal_categories/",
        views.api_meal_categories,
        name="api_meal_categories",
    ),
    path(
        "api/meals_per_category/",
        views.api_meals_per_category,
        name="api_meals_per_category",
    ),
    path(
        "api/register_sale_meals/",
        views.api_register_sale_meals,
        name="api_register_sale_meals",
    ),
    # API Journeys
    path(
        "api/types_journey/",
        views.api_types_journey,
        name="api_types_journey",
    ),
    path(
        "api/journey_per_date/",
        views.api_journey_per_date,
        name="api_journey_per_date",
    ),
    path(
        "api/get_data_schedule/",
        views.api_get_data_schedule,
        name="api_get_data_schedule",
    ),
    path(
        "api/available_seats_per_schedule/",
        views.api_available_seats_per_schedule,
        name="api_available_seats_per_schedule",
    ),
    path(
        "api/price_journey/",
        views.api_price_journey,
        name="api_price_journey",
    ),
    path(
        "api/reserve_tickets/",
        views.api_reserve_tickets,
        name="api_reserve_tickets",
    ),
    path(
        "prueba_reserva/",
        views.prueba_reserva,
        name="prueba_reserva",
    ),
]
