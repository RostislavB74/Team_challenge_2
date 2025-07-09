# journals/forms.py
from django import forms
from .models import ShiftReports



class ShiftReportRowForm(forms.Form):
    product_id = forms.IntegerField(label="ID продукту")
    quantity = forms.DecimalField(label="Кількість", max_digits=10, decimal_places=2)


class ShiftReportForm(forms.ModelForm):
    
    class Meta:
        model = ShiftReports
        fields = ["doc_number", "author", "doc_date", "total"]
        widgets = {
            "doc_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["doc_number"].widget.attrs["readonly"] = True
