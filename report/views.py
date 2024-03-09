import os
from datetime import datetime
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
import tempfile

from django.core.files.storage import default_storage
from .models import Patient


def generate_report(request):
    if request.method == 'POST':
        clinic_name = request.POST.get('clinic_name')
        physician = request.POST.get('physician')
        physician_contact = request.POST.get('physician_contact')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        contact = request.POST.get('contact')
        chief_complaint = request.POST.get('chief_complaint')
        consultation_note = request.POST.get('consultation_note')
        clinic_logo = request.FILES.get('clinic_logo')

        # Create a new Patient instance
        patient = Patient.objects.create(
            clinic_name=clinic_name,
            physician=physician,
            physician_contact=physician_contact,
            first_name=first_name,
            last_name=last_name,
            dob=dob,
            contact=contact,
            chief_complaint=chief_complaint,
            consultation_note=consultation_note,
            clinic_logo=clinic_logo
        )

        # Generate the PDF report
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="CR_{last_name}_{first_name}_{dob}.pdf"'

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)

        # Add header with clinic logo
        if clinic_logo:
            # Save the uploaded image to a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                for chunk in clinic_logo.chunks():
                    tmp_file.write(chunk)
            pdf.drawImage(tmp_file.name, 72, 800, width=72, height=72)
            os.unlink(tmp_file.name)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ip_address = request.META.get('REMOTE_ADDR', '')
        footer_text = f'This report is generated on {timestamp} from {ip_address}'
        pdf.drawString(72, 36, footer_text)

        pdf.drawString(72, 750, f'Clinic Name: {clinic_name}')
        pdf.drawString(72, 730, f'Physician: {physician}')
        pdf.drawString(72, 710, f'Physician Contact: {physician_contact}')
        pdf.drawString(72, 690, f'First Name: {first_name}')
        pdf.drawString(72, 670, f'Last Name: {last_name}')
        pdf.drawString(72, 650, f'DOB: {dob}')
        pdf.drawString(72, 630, f'Contact: {contact}')
        pdf.drawString(72, 610, f'Chief Complaint: {chief_complaint}')
        pdf.drawString(72, 590, f'Consultation Note: {consultation_note}')

        pdf.showPage()
        pdf.save()

        pdf_data = buffer.getvalue()
        buffer.close()
        response.write(pdf_data)

        return response
    else:
        return render(request, "report_form.html")


