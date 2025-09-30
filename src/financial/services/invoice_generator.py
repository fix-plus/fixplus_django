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


def generate_invoice_pdf(invoice_id):
    """
    Generate PDF invoice based on CustomerInvoice model.
    Uses persian-tools for number to words conversion.
    File is stored with hashed name in mediafiles/invoices/ for security.
    Returns pdf_path.
    """
    invoice = CustomerInvoice.objects.get(id=invoice_id)
    service = invoice.service
    brand = service.brand  # Fallback to service.brand if not set

    # Prepare data from models
    items = [
        {
            'row': i + 1,
            'name': item.description,  # Use description as name
            'unit': 'عدد',  # Fixed or from model if exists
            'quantity': item.quantity,
            'price': f"{item.cost*10:,}",
            'total': f"{item.cost * item.quantity *10:,}",
            'description': ""
        }
        for i, item in enumerate(service.completed_service_items.all())
    ]

    # Add wage_cost and deadheading_cost as separate items
    last_row = len(items) + 1
    if invoice.wage_cost > 0:
        items.append({
            'row': last_row,
            'name': 'اجرت',
            'unit': 'خدمت',
            'quantity': 1,
            'price': f"{invoice.wage_cost*10:,}",
            'total': f"{invoice.wage_cost*10:,}",
            'description': ''
        })
        last_row += 1
    if invoice.deadheading_cost > 0:
        items.append({
            'row': last_row,
            'name': 'ایاب و ذهاب',
            'unit': 'خدمت',
            'quantity': 1,
            'price': f"{invoice.deadheading_cost*10:,}",
            'total': f"{invoice.deadheading_cost*10:,}",
            'description': ''
        })

    data = {
        'header_image': brand.header_image,
        'logo_image': brand.logo_image,
        'stamp_image': brand.stamp_image,
        'footer_image': brand.footer_image,
        'right_text1': brand.right_text1 or "مرکز تعمیرات دوو",
        'right_text2': brand.right_text2 or "مرکز خدمات پس از فروش / دوو",
        'invoice_number': invoice.identify_code,
        'date': to_jalali_date_string(invoice.created_at, '%Y/%m/%d'),
        'customer_name': ('آقای ' if service.customer.gender == Customer.Gender.MALE else 'خانم ') + service.customer.full_name if hasattr(service.customer, 'full_name') else '',
        'address': service.address.address if hasattr(service.address, 'address') else service.address.__str__(),
        'phone': service.customer.contact_numbers.filter(is_primary=True).first().number.replace('+98', '0') if service.customer else '',
        'items': items,
        'subtotal': invoice.get_total_invoice_amount()*10,
        'discount': invoice.discount_amount*10,
        'total': invoice.get_payable_amount()*10,
        'total_words': '',
        'notes': invoice.get_notes(),
        'repair_address': brand.repair_address,
        'phone_numbers': brand.phone_numbers,
    }

    # Convert total to Persian words using persian-tools
    data['total_words'] = digits.convert_to_word(data['total']) + ' ریال' if data['total'] else 'صفر ریال'
    data['subtotal_str'] = f"{data['subtotal']:,}"
    data['discount_str'] = f"{data['discount']:,}"
    data['total_str'] = f"{data['total']:,}"
    data["font_path"] = Path(settings.BASE_DIR, "src/templates/Koodak.ttf").as_uri()

    # Load template
    env = Environment(loader=FileSystemLoader('src/templates/'))
    template = env.get_template('invoice_template.html')
    html_content = template.render(**data)

    # Generate hashed filename
    hash_input = f"{invoice_id}_{datetime.now().timestamp()}"
    file_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]  # 16 chars for shorter name
    pdf_path = f'invoices/{file_hash}.pdf'

    # Generate PDF
    pdf_full_path = os.path.join(settings.MEDIA_ROOT, pdf_path)
    os.makedirs(os.path.dirname(pdf_full_path), exist_ok=True)
    HTML(string=html_content, base_url="http://127.0.0.1:8000/").write_pdf(pdf_full_path)  # Adjust base_url if needed

    return pdf_path