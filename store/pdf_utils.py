import os
import random
import string
from fpdf import FPDF
from store.models import OrderItem 
class ReceiptGenerator:
    def __init__(self, order):
        self.order = order
        self.code = self._generate_code()

    def _generate_code(self, length=10):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def generate(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=f"Receipt - {self.code}", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Customer: {self.order.user.username}", ln=True)
        pdf.cell(200, 10, txt=f"Total Paid: {self.order.total_amount} GEL", ln=True)  # ⚠ no ₾ symbol
        pdf.cell(200, 10, txt=f"Date: {self.order.created_at.strftime('%Y-%m-%d %H:%M')}", ln=True)
        pdf.cell(200, 10, txt=f"Receipt Code: {self.code}", ln=True)
        pdf.ln(10)
        pdf.cell(200, 10, txt="Order Details:", ln=True)

        for item in OrderItem.objects.filter(order=self.order):

            line = f"- {item.item.name} | Qty: {item.quantity} | Unit Price: {item.price} GEL"
            pdf.cell(200, 10, txt=line, ln=True)

        file_path = f"media/receipts/receipt_{self.code}.pdf"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        pdf.output(file_path, 'F')

        return file_path
