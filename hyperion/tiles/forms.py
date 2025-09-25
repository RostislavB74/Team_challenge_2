from django import forms


class UploadLabelForm(forms.Form):
    file = forms.FileField()
    file_name = forms.CharField(max_length=255)
