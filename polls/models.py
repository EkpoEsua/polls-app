from typing import Iterator
from django.db import models
from django.db.models.query import QuerySet


class AgentName(models.Model):
    name_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    pollingunit_uniqueid = models.IntegerField()

    def __str__(self) -> str:
        return self.firstname + " " + self.lastname

    class Meta:
        # managed = False
        db_table = "agentname"


class AnnouncedLGAResults(models.Model):
    result_id = models.AutoField(primary_key=True)
    lga_name = models.CharField(max_length=50)
    party_abbreviation = models.CharField(max_length=4)
    party_score = models.IntegerField()
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateField()
    user_ip_address = models.CharField(max_length=50)

    class Meta:
        # managed = False
        db_table = "announced_lga_results"


class AnnouncedPUResults(models.Model):
    result_id = models.AutoField(primary_key=True)
    polling_unit_uniqueid = models.CharField(max_length=50)
    party_abbreviation = models.CharField(max_length=4)
    party_score = models.IntegerField()
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField()
    user_ip_address = models.CharField(max_length=50)

    class Meta:
        # managed = False
        db_table = "announced_pu_results"


class AnnouncedStateResults(models.Model):
    class Meta:
        # managed = False
        db_table = "announced_state_results"


class AnnouncedWardResults(models.Model):
    class Meta:
        # managed = False
        db_table = "announced_ward_results"


class LGA(models.Model):
    uniqueid = models.AutoField(primary_key=True)
    lga_id = models.IntegerField()
    lga_name = models.CharField(max_length=50)
    state_id = models.CharField(max_length=50)
    lga_description = models.TextField()
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField()
    user_ip_address = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.lga_name + " - " + str(self.lga_id)

    class Meta:
        # managed = False
        db_table = "lga"


class Party(models.Model):
    id = models.AutoField(primary_key=True)
    partyid = models.CharField(max_length=11)
    partyname = models.CharField(max_length=11)

    class Meta:
        # managed = False
        db_table = "party"


class PollingUnit(models.Model):
    uniqueid = models.AutoField(primary_key=True)
    polling_unit_id = models.IntegerField()
    ward_id = models.IntegerField()
    lga_id = models.IntegerField()
    uniquewardid = models.IntegerField(null=True)
    polling_unit_number = models.CharField(max_length=50, null=True)
    polling_unit_name = models.CharField(max_length=50, null=True)
    polling_unit_description = models.TextField(null=True)
    lat = models.CharField(max_length=255, null=True)
    long = models.CharField(max_length=255, null=True)
    entered_by_user = models.CharField(max_length=50, null=True)
    date_entered = models.DateTimeField(null=True)
    user_ip_address = models.CharField(max_length=50, null=True)

    class Meta:
        # managed = False
        db_table = "polling_unit"


class States(models.Model):
    class Meta:
        # managed = False
        db_table = "states"


class Ward(models.Model):
    uniqueid = models.AutoField(primary_key=True)
    ward_id = models.IntegerField()
    ward_name = models.CharField(max_length=50)
    lga_id = models.IntegerField()
    ward_description = models.TextField()
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField()
    user_ip_address = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.ward_name

    class Meta:
        # managed = False
        db_table = "ward"
        ordering = ["uniqueid"]
