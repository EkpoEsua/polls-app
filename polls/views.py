from functools import partial
from typing import Any, Dict
from django.db.models import query
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm, BaseModelFormSet, modelformset_factory
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, FormView, CreateView
from polls.models import PollingUnit, AnnouncedPUResults, LGA, Party
from polls.forms import (
    AnnouncedPUResultsForm,
    ResultPerLGAForm,
    PollingUnitForm,
    BaseAnnouncedPUResultsFormSet,
)
from django.urls import reverse_lazy
from django.utils import timezone


class PUResultView(ListView):
    model = PollingUnit
    paginate_by = 10
    queryset = PollingUnit.objects.all()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        pus = context.get("pollingunit_list", None)
        for pu in pus:
            pu.announced_results = AnnouncedPUResults.objects.filter(
                polling_unit_uniqueid=pu.uniqueid
            )
        return context


class LGAResultRequestView(FormView):
    form_class = ResultPerLGAForm
    template_name = "polls/lga_result_request.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        lga_id = request.GET.get("lga", None)
        if lga_id:
            return HttpResponseRedirect(reverse_lazy("lga-result", args=[str(lga_id)]))

        return super().get(request, *args, **kwargs)


class LGAResultView(ListView):
    model = PollingUnit
    queryset = PollingUnit.objects.all()
    template_name = "polls/lga_result.html"

    def get_queryset(self) -> QuerySet:
        query = super().get_queryset()

        lga = self.kwargs.get("pk", None)
        self.lga = lga
        if lga:
            query = query.filter(lga_id=lga)
        return query

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        pus = context.get("pollingunit_list", None)

        total = 0
        result = False
        lga_name = LGA.objects.get(lga_id=self.lga).lga_name
        if pus:
            result = True
            for pu in pus:
                pu.total = 0
                announced_results: QuerySet[
                    AnnouncedPUResults
                ] = AnnouncedPUResults.objects.filter(polling_unit_uniqueid=pu.uniqueid)
                for ar in announced_results:
                    pu.total += ar.party_score
                    total += ar.party_score

        context.update(total=total, lga_name=lga_name, result=result)

        return context


class PollingUnitCreationView(CreateView):
    """Render view to create a new Polling Unit."""

    model = PollingUnit
    form_class = PollingUnitForm
    success_url = reverse_lazy("add-pu-result")

    def form_valid(self, form: PollingUnitForm) -> HttpResponse:
        """"""
        form.instance.date_entered = timezone.now()
        form.instance.user_ip_address = self.request.META.get("REMOTE_ADDR", "0.0.0.0")
        form.instance.ward_id = form.cleaned_data["uniquewardid"].ward_id
        form.instance.uniquewardid = form.cleaned_data["uniquewardid"].uniqueid
        form.instance.lga_id = form.cleaned_data["lga_id"].lga_id
        self.object = form.save()
        success_url = reverse_lazy("add-pu-results", args=[str(self.object.pk)])
        return HttpResponseRedirect(str(success_url))


class AnnouncedResultCreationView(CreateView):
    model = AnnouncedPUResults
    form_class = modelformset_factory(
        AnnouncedPUResults,
        form=AnnouncedPUResultsForm,
        formset=BaseAnnouncedPUResultsFormSet,
    )
    success_url = reverse_lazy("pu-result-add-success")

    def get_initial(self) -> Dict[str, Any]:
        parties = Party.objects.all()
        initial = list()
        for party in parties:
            init = {"party_abbreviation": party.partyname[:4]}
            initial.append(init)

        return initial

    def get_form_class(self):
        initial = self.get_initial()
        form_class = modelformset_factory(
            AnnouncedPUResults,
            form=AnnouncedPUResultsForm,
            extra=len(initial),
            formset=BaseAnnouncedPUResultsFormSet,
        )
        return form_class

    def get_success_url(self) -> str:
        return self.success_url

    def form_valid(self, form: BaseAnnouncedPUResultsFormSet) -> HttpResponse:
        date_entered = timezone.now()
        user_ip_address = self.request.META.get("REMOTE_ADDR", "0.0.0.0")
        polling_unit_uniqueid = self.kwargs["pk"]
        polling_unit: PollingUnit = PollingUnit.objects.get(pk=self.kwargs["pk"])
        entered_by_user = polling_unit.entered_by_user
        for unit_form in form.forms:
            unit_form.instance.date_entered = date_entered
            unit_form.instance.user_ip_address = user_ip_address
            unit_form.instance.polling_unit_uniqueid = polling_unit_uniqueid
            unit_form.instance.entered_by_user = entered_by_user

        return super().form_valid(form)
