from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from rules.forms import RuleForm
from rules.models import Rule


class RuleListView(ListView):
    model = Rule
    template_name = "rules/rule_list.html"
    context_object_name = "rules"


class RuleCreateView(CreateView):
    model = Rule
    form_class = RuleForm
    template_name = "rules/rule_form.html"

    def get_success_url(self):
        messages.success(self.request, "Regla creada correctamente.")
        return reverse("rules:list")


class RuleUpdateView(UpdateView):
    model = Rule
    form_class = RuleForm
    template_name = "rules/rule_form.html"

    def get_success_url(self):
        messages.success(self.request, "Regla actualizada correctamente.")
        return reverse("rules:list")


class RuleDeleteView(DeleteView):
    model = Rule
    template_name = "rules/rule_confirm_delete.html"
    success_url = reverse_lazy("rules:list")

    def form_valid(self, form):
        messages.success(self.request, "Regla eliminada correctamente.")
        return super().form_valid(form)