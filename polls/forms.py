from django import forms
from polls.models import LGA, PollingUnit, AnnouncedPUResults, Ward, AgentName


class ResultPerLGAForm(forms.Form):
    lga = forms.ModelChoiceField(
        queryset=LGA.objects.all(), label="LGA",
        to_field_name="lga_id"
    )

class PollingUnitForm(forms.Form):
    ward_id = forms.ModelChoiceField(
        queryset=Ward.objects.all(), label="Ward",
        to_field_name="ward_id"
    )
    lga_id = forms.ModelChoiceField(
        queryset=LGA.objects.all(), label="LGA I.D.",
        to_field_name="lga_id"
    )
    uniquewardid = forms.IntegerField(disabled=True, widget=forms.HiddenInput)
    polling_unit_number = forms.CharField(max_length=50, help_text="e.g. DTXXXXXXX")
    entered_by_user = forms.ModelChoiceField(
        queryset=AgentName.objects.all(), label="Agent",
        to_field_name="first_name"
    )
    date_entered = forms.DateTimeField(
        disabled=True, widget=forms.HiddenInput
    )
    user_ip_address = forms.CharField(max_length=50, disabled=True, widget=forms.HiddenInput)

    class Meta:
        model = PollingUnit
        fields = [
            "polling_unit_id", "ward_id", "lga_id",
            "uniquewardid", "polling_unit_number", "polling_unit_name",
            "polling_unit_description", "lat", "long",
            "entered_by_user", "date_entered", "user_ip_address"
        ]

class AnnouncedPUResultsForm(forms.Form):

    class Meta:
        model = AnnouncedPUResults
        fields = [
            "polling_unit_uniqueid", "party_abbreviation", "party_score",
            "entered_by_user", "date_entered", "user_ip_address"
        ]