import hashlib
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime
from persian_tools import digits
from django.conf import settings

from src.common.utils import to_jalali_date_string
from src.customer.models import Customer
from src.financial.models import CustomerInvoice


def generate_invoice_pdf(*, invoice_id, request=None):
    """
    Generate PDF invoice for CustomerInvoice.
    Each service has its own folder.
    The filename will be in the format 'فاکتور_شماره_{identify_code}_مشتری_{full_name}.pdf'.
    If a file already exists, it will be replaced.
    """
    invoice = CustomerInvoice.objects.get(id=invoice_id)
    service = invoice.service
    brand = service.brand

    # Prepare invoice items
    items = [
        {
            'row': i + 1,
            'name': item.description,
            'unit': 'عدد',
            'quantity': item.quantity,
            'price': f"{item.cost * 10:,}",
            'total': f"{item.cost * item.quantity * 10:,}",
            'description': ""
        }
        for i, item in enumerate(service.completed_service_items.all())
    ]

    last_row = len(items) + 1
    if invoice.wage_cost > 0:
        items.append({
            'row': last_row,
            'name': 'اجرت',
            'unit': 'خدمت',
            'quantity': 1,
            'price': f"{invoice.wage_cost * 10:,}",
            'total': f"{invoice.wage_cost * 10:,}",
            'description': ''
        })
        last_row += 1
    if invoice.deadheading_cost > 0:
        items.append({
            'row': last_row,
            'name': 'ایاب و ذهاب',
            'unit': 'خدمت',
            'quantity': 1,
            'price': f"{invoice.deadheading_cost * 10:,}",
            'total': f"{invoice.deadheading_cost * 10:,}",
            'description': ''
        })

    # Prepare data for the template
    data = {
        'header_image': brand.header_image,
        'logo_image': brand.logo_image,
        'stamp_image': brand.stamp_image,
        'footer_image': brand.footer_image,
        'right_text1': brand.right_text1,
        'right_text2': brand.right_text2,
        'invoice_number': invoice.identify_code,
        'date': to_jalali_date_string(invoice.created_at, '%Y/%m/%d'),
        'customer_name': ('آقای ' if service.customer.gender == Customer.Gender.MALE else 'خانم ') +
                         service.customer.full_name if hasattr(service.customer, 'full_name') else '',
        'address': service.address.address if hasattr(service.address, 'address') else service.address.__str__(),
        'phone': service.customer.contact_numbers.filter(is_primary=True).first().number.replace('+98', '0')
                 if service.customer else '',
        'items': items,
        'subtotal': invoice.get_total_invoice_amount() * 10,
        'discount': invoice.discount_amount * 10,
        'total': invoice.get_payable_amount() * 10,
        'total_words': '',
        'notes': invoice.get_notes(),
        'repair_address': brand.repair_address,
        'phone_numbers': brand.phone_numbers,
    }

    data['total_words'] = digits.convert_to_word(data['total']) + ' ریال' if data['total'] else 'صفر ریال'
    data['subtotal_str'] = f"{data['subtotal']:,}"
    data['discount_str'] = f"{data['discount']:,}"
    data['total_str'] = f"{data['total']:,}"
    data["font_path"] = Path(settings.BASE_DIR, "src/templates/Koodak.ttf").as_uri()

    # Define the service folder path
    service_folder = Path(settings.MEDIA_ROOT) / "invoices" / "service" / str(service.id)
    os.makedirs(service_folder, exist_ok=True)

    # Generate filename based on invoice identify_code and customer full_name
    customer_name = service.customer.full_name.replace(' ', '_') if service.customer.full_name else 'unknown'
    filename = f"فاکتور_شماره_{invoice.identify_code}_مشتری_{customer_name}.pdf"
    pdf_full_path = service_folder / filename

    # If file already exists, remove it to replace with the new one
    if pdf_full_path.exists():
        os.remove(pdf_full_path)

    # Generate PDF
    env = Environment(loader=FileSystemLoader('src/templates/'))
    template = env.get_template('invoice_template.html')
    html_content = template.render(**data)

    base_url = request.build_absolute_uri('/') if request and hasattr(request, 'build_absolute_uri') else "http://127.0.0.1:8000/"
    HTML(string=html_content, base_url=base_url).write_pdf(str(pdf_full_path))

    # Save the relative path to the database
    relative_path = str(pdf_full_path.relative_to(settings.MEDIA_ROOT))
    invoice.pdf_output = relative_path
    invoice.save()

    # Return the URL for the PDF
    file_url = settings.MEDIA_URL + relative_path
    return file_url