import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import green
from datetime import datetime

PDF_FOLDER = "uploads/doctor_verified_pdfs"


def generate_verified_doctor_pdf(data):
    os.makedirs(PDF_FOLDER, exist_ok=True)

    filename = f"doctor_verified_{data['email']}.pdf"
    path = os.path.join(PDF_FOLDER, filename)

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "Doctor Verification Certificate")
    y -= 30

    # Status
    c.setFillColor(green)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "STATUS: VERIFIED")
    c.setFillColorRGB(0, 0, 0)
    y -= 30

    # Doctor details
    c.setFont("Helvetica", 11)
    details = [
        ("Name", data["name"]),
        ("Email", data["email"]),
        ("Specialization", data["specialization"]),
        ("Experience", f"{data['experience']} years"),
        ("Clinic", data["clinic"]),
        ("Location", data["location"]),
    ]

    for label, value in details:
        c.drawString(50, y, f"{label}: {value}")
        y -= 18

    y -= 20

    # Verification text
    c.setFont("Helvetica-Oblique", 11)
    c.drawString(
        50,
        y,
        "This document confirms that the above doctor has been verified"
    )
    y -= 16
    c.drawString(
        50,
        y,
        "through internal review and validation by HealthyLife."
    )

    y -= 40

    # Digital verification footer
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Digitally Verified by HealthyLife")
    y -= 15
    c.drawString(50, y, "Authorized by Mahboob Attar")
    y -= 15
    c.setFont("Helvetica", 9)
    c.drawString(
        50,
        y,
        f"Verification Date: {datetime.now().strftime('%d %b %Y')}"
    )

    # Watermark
    c.setFont("Helvetica-Bold", 40)
    c.setFillColorRGB(0.9, 0.9, 0.9)
    c.saveState()
    c.translate(300, 400)
    c.rotate(45)
    c.drawCentredString(0, 0, "VERIFIED")
    c.restoreState()

    c.showPage()
    c.save()

    return path
