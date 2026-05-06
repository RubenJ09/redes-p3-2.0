from django import forms

from rules.models import Rule


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ["raw_text", "enabled"]
        widgets = {
            "raw_text": forms.TextInput(attrs={"placeholder": "si sensor_salon mayor que 25 entonces switch_caldera OFF"}),
        }
