from django import forms
from organization.models import *


class Query1Form(forms.Form):
    required_department = forms.ModelChoiceField(queryset=Department.objects.all())
    required_category = forms.ModelChoiceField(queryset=Category.objects.all())
    min_age = forms.IntegerField()
    max_age = forms.IntegerField()


class Query3Form(forms.Form):
    from_date = forms.DateField()
    to_date = forms.DateField()


class Query4ContractForm(forms.Form):
    contract = forms.ModelChoiceField(queryset=Contract.objects.all())


class Query4ProjectForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all())


class Query5Form(forms.Form):
    from_date = forms.DateField()
    to_date = forms.DateField()


class Query6Form(forms.Form):
    date_point = forms.DateField()


class Query7ContractForm(forms.Form):
    contract = forms.ModelChoiceField(queryset=Contract.objects.all())


class Query7ProjectForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all())


class Query8WorkerForm(forms.Form):
    worker = forms.ModelChoiceField(queryset=Worker.objects.all())
    worker_from_date = forms.DateField()
    worker_to_date = forms.DateField()


class Query8CategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    category_from_date = forms.DateField()
    category_to_date = forms.DateField()


class Query10Form(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    from_date = forms.DateField()
    to_date = forms.DateField()


class Query11Form(forms.Form):
    equipment = forms.ModelChoiceField(queryset=Equipment.objects.all())


class Query13Form(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    from_date = forms.DateField()
    to_date = forms.DateField()
