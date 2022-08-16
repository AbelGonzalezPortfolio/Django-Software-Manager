from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
from .models import Computer, Software
from . import forms
from django.views import View

# Create your views here.
class ComputersView(View):
    template_name = "datasets/computers.html"

    def get(self, request, *args, **kwargs):
        search_term = request.GET.get("search_string")
        if search_term is not None:
            computers = Computer.objects.filter(hostname__icontains=search_term)
        else:
            search_term = ""
            computers = Computer.objects.all()

        order_by = request.GET.get("order_by")
        order_ascending = request.GET.get("order_ascending")
        if order_by is not None:
            computers = computers.order_by(order_by)
            if order_ascending == "False":
                order_ascending = False
                computers = computers.reverse()
            else:
                order_ascending = True

        paginator = Paginator(computers, 25)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        page_range = paginator.get_elided_page_range(
            page_obj.number, on_each_side=3, on_ends=1
        )
        context = {
            "page_obj": page_obj,
            "page_range": page_range,
            "search_term": search_term,
            "order_by": order_by,
            "order_ascending": order_ascending,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = forms.ComputerSelect(request.POST)
        if "enable_remoting" in request.POST:
            if form.is_valid():
                computers = form.cleaned_data["choices"]
                computers.update_ip()
                computers.update_network_status()
                computers.update_remoting_status()
                computers.enable_remoting()
                computers.update_remoting_status()
        elif "sync" in request.POST:
            if form.is_valid():
                computers = form.cleaned_data["choices"]
                computers.update_ip()
                computers.update_network_status()
                computers.update_remoting_status()
                computers.update_software()
        return redirect(reverse("computers") + "?" + request.GET.urlencode())


class ComputerDetailView(View):
    template_name = "datasets/computer_detail.html"

    def get(self, request, id, *args, **kwargs):
        computer = get_object_or_404(Computer, pk=id)
        software_list = computer.software.all()
        context = {"computer": computer, "software_list": software_list}
        return render(request, self.template_name, context=context)


class SoftwareView(View):
    template_name = "datasets/software.html"

    def get(self, request, *args, **kwargs):
        search_term = request.GET.get("search_string")
        if search_term is not None:
            software = Software.objects.with_client_count().filter(
                name__icontains=search_term
            )
        else:
            search_term = ""
            software = Software.objects.with_client_count().all()

        paginator = Paginator(software, 25)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        page_range = paginator.get_elided_page_range(
            page_obj.number, on_each_side=3, on_ends=1
        )

        context = {
            "page_obj": page_obj,
            "page_range": page_range,
            "search_term": search_term,
        }

        return render(request, self.template_name, context=context)


class SoftwareDetailView(View):
    template_name = "datasets/software_detail.html"

    def get(self, request, id, *args, **kwargs):
        software = Software.objects.get(pk=id)
        software_list = Software.objects.filter(name=software.name)
        computers = software.computer_set.all()
        context = {
            "software": software,
            "software_list": software_list,
        }
        return render(request, self.template_name, context=context)
