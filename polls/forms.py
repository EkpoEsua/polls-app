from typing import Any, Dict
from django import forms
from polls.models import LGA, PollingUnit, AnnouncedPUResults, Ward, AgentName


class ResultPerLGAForm(forms.Form):
    lga = forms.ModelChoiceField(
        queryset=LGA.objects.all(), label="LGA",
        to_field_name="lga_id"
    )

class PollingUnitForm(forms.ModelForm):
    uniquewardid = forms.ModelChoiceField(
        queryset=Ward.objects.all(), label="Ward"
    )
    lga_id = forms.ModelChoiceField(
        queryset=LGA.objects.all(), label="LGA",
        to_field_name="lga_id"
    )
    polling_unit_number = forms.CharField(max_length=50, help_text="e.g. DTXXXXXXX")
    entered_by_user = forms.ModelChoiceField(
        queryset=AgentName.objects.all(), label="Agent",
        to_field_name="firstname"
    )

    class Meta:
        model = PollingUnit
        fields = [
            "uniqueid", "polling_unit_id",
            "polling_unit_number", "polling_unit_name",
            "polling_unit_description", "lat", "long",
            "entered_by_user"
        ]


class AnnouncedPUResultsForm(forms.ModelForm):
    entered_by_user = forms.ModelChoiceField(
        queryset=AgentName.objects.all(), label="Agent",
        to_field_name="firstname"
    )

    class Meta:
        model = AnnouncedPUResults
        fields = [
            "result_id", "party_abbreviation", "party_score",
            "entered_by_user", "date_entered", "user_ip_address"
        ]