from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from pdfrw import PdfReader, PdfWriter, PageMerge
from io import BytesIO
import qrcode

from django.core.mail import EmailMessage

import os
from django.conf import settings

from django.utils.translation import gettext as _

# Fechas
from datetime import timedelta
from django.utils import timezone

positions = [
    {
        "text": "FechaEmision",
        "x": 26.614365,
        "y": 769.157465,
        "font-size": 7,
        "font-color-R": 0,
        "font-color-G": 0,
        "font-color-B": 0,
    },
    {
        "text": "IdVenta",
        "x": 358.4195,
        "y": 387.02225,
        "font-size": 6,
        "font-color-R": 48,
        "font-color-G": 48,
        "font-color-B": 48,
    },
    {
        "text": "NombrePasajero",
        "x": 325.4145,
        "y": 367.7945,
        "font-size": 18,
        "font-color-R": 60,
        "font-color-G": 174,
        "font-color-B": 227,
    },
    {
        "text": "IdTicket",
        "x": 324.60249999999996,
        "y": 350.24850000000004,
        "font-size": 18,
        "font-color-R": 60,
        "font-color-G": 174,
        "font-color-B": 227,
    },
    {
        "text": "FechaBoleto",
        "x": 322.49649999999997,
        "y": 334.6095,
        "font-size": 10,
        "font-color-R": 0,
        "font-color-G": 0,
        "font-color-B": 0,
    },
    {
        "text": "EstacionSalida",
        "x": 341.4525,
        "y": 281.3025,
        "font-size": 10,
        "font-color-R": 48,
        "font-color-G": 48,
        "font-color-B": 48,
    },
    {
        "text": "HorarioPartida",
        "x": 341.0775,
        "y": 271.4175,
        "font-size": 10,
        "font-color-R": 60,
        "font-color-G": 174,
        "font-color-B": 227,
    },
    {
        "text": "EstacionLlegada",
        "x": 341.4525,
        "y": 255.0525,
        "font-size": 10,
        "font-color-R": 48,
        "font-color-G": 48,
        "font-color-B": 48,
    },
    {
        "text": "HorarioLlegada",
        "x": 341.0775,
        "y": 245.1675,
        "font-size": 10,
        "font-color-R": 60,
        "font-color-G": 174,
        "font-color-B": 227,
    },
    {
        "text": "IdAsiento",
        "x": 320.905,
        "y": 222.855,
        "font-size": 20,
        "font-color-R": 60,
        "font-color-G": 174,
        "font-color-B": 227,
    },
    {
        "text": "CategoriaAsiento",
        "x": 321.905,
        "y": 210.363,
        "font-size": 12,
        "font-color-R": 48,
        "font-color-G": 48,
        "font-color-B": 48,
    },
    {
        "text": "HorarioEspera",
        "x": 325.1645,
        "y": 155.5445,
        "font-size": 18,
        "font-color-R": 60,
        "font-color-G": 174,
        "font-color-B": 227,
    },
    {
        "text": "HorarioSalida",
        "x": 500.14599999999996,
        "y": 155.5445,
        "font-size": 18,
        "font-color-R": 60,
        "font-color-G": 174,
        "font-color-B": 227,
    },
    {
        "text": "EnlaceWeb",
        "x": 26.614365,
        "y": 14.157465,
        "font-size": 6.66,
        "font-color-R": 0,
        "font-color-G": 0,
        "font-color-B": 0,
    },
]

qr_data = {
    "qr_x": 464.1459,
    "qr_y": 260.6095,
    "url": "https://www.trenalasnubes.com.ar",
}


def generate_qr_code(data):
    # Generar el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Crear la imagen QR en memoria
    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def generate_pdf(replacements, language):

    #     # Ruta de la fuente
    font_path = os.path.join(
        settings.BASE_DIR, "static", "fonts", "OpenSans-Regular.ttf"
    )

    if language == "es":
        #     # Ruta de la pdf
        pdf_path = os.path.join(settings.BASE_DIR, "static", "pdf", "base-es.pdf")
    else:
        pdf_path = os.path.join(settings.BASE_DIR, "static", "pdf", "base-en.pdf")

    # Registrar la fuente personalizada
    pdfmetrics.registerFont(TTFont("OpenSans-Regular", font_path))

    buffer = BytesIO()
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Generar el código QR en memoria
    qr_buffer = generate_qr_code(replacements["EnlaceWeb"])
    qr_image = ImageReader(qr_buffer)

    for page_number, page in enumerate(reader.pages, start=1):
        # Crear una nueva capa para los reemplazos en memoria
        packet = BytesIO()
        overlay = canvas.Canvas(packet, pagesize=letter)

        # Añadir la imagen QR en la posición deseada
        overlay.drawImage(
            qr_image, qr_data["qr_x"], qr_data["qr_y"], width=100, height=100
        )

        # Añadir texto reemplazado en las posiciones correctas
        for text_data in positions:
            placeholder = text_data["text"]
            if placeholder in replacements:
                replacement_text = replacements[placeholder]
                x, y = text_data["x"], text_data["y"]
                font_size = text_data["font-size"]
                R, G, B = (
                    text_data["font-color-R"] / 255.0,
                    text_data["font-color-G"] / 255.0,
                    text_data["font-color-B"] / 255.0,
                )
                overlay.setFillColorRGB(R, G, B)
                overlay.setFont("OpenSans-Regular", font_size)
                overlay.drawString(x, y, replacement_text)

        # Asegúrate de finalizar la página y guardar el canvas
        overlay.showPage()
        overlay.save()
        packet.seek(0)

        # Leer el PDF de la capa desde el buffer de memoria
        overlay_pdf = PdfReader(packet)

        if overlay_pdf.pages:
            merger = PageMerge(page)
            merger.add(overlay_pdf.pages[0]).render()

        writer.addpage(page)

    writer.write(buffer)
    buffer.seek(0)
    return buffer


def send_pdf_via_email(tickets, email_):
    subject = _("Notification of Ticket Purchase")
    message = _(
        "You have made a ticket purchase. Please find attached the purchase receipt"
    )
    email_from = settings.DEFAULT_FROM_EMAIL
    email = EmailMessage(
        subject,
        message,
        email_from,
        [email_],
    )
    language = "en" if subject == "Notification of Ticket Purchase" else "es"
    for ticket in tickets:
        replacements = ticket.getDataPublic()
        pdf_buffer = generate_pdf(replacements, language)

        filename = (
            ticket.passenger.dni_or_passport + "_" + str(ticket.schedule) + ".pdf"
        )
        email.attach(filename, pdf_buffer.getvalue(), "application/pdf")

    email.send()


def send_pdf_via_email_change_passenger(ticket, email_):
    subject = _("Notification of Passenger Change")
    message = _(
        "There has been a change of passenger on a ticket you have purchased. The ticket is attached below."
    )
    email_from = settings.DEFAULT_FROM_EMAIL
    email = EmailMessage(
        subject,
        message,
        email_from,
        [email_],
    )
    language = "en" if subject == "Notification of Passenger Change" else "es"
    replacements = ticket.getDataPublic()
    pdf_buffer = generate_pdf(replacements, language)

    filename = ticket.passenger.dni_or_passport + "_" + str(ticket.schedule) + ".pdf"
    email.attach(filename, pdf_buffer.getvalue(), "application/pdf")

    email.send()
