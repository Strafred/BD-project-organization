from django.db import connection
from django.shortcuts import render

from .forms import *


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


# Create your views here.
def query1(request):
    data = None

    if request.method == 'POST':
        form = Query1Form(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                required_department = form.cleaned_data.get("required_department").pk
                required_category = form.cleaned_data.get("required_category").pk
                min_age = form.cleaned_data.get("min_age")
                max_age = form.cleaned_data.get("max_age")

                cursor.execute("select organization_department.department_name, organization_worker.worker_name, "
                               "organization_worker.worker_age, organization_worker.worker_address from "
                               "organization_department inner join organization_worker_assigned_departments on "
                               "organization_department.id = organization_worker_assigned_departments.department_id "
                               "inner join organization_worker on organization_worker_assigned_departments.worker_id "
                               "= organization_worker.id where (organization_department.id = %s) and ("
                               "organization_worker.worker_category_id = %s) and (organization_worker.worker_age "
                               "between %s and %s)" % (required_department, required_category, min_age, max_age))

                data = dict_fetchall(cursor)
    else:
        form = Query1Form()
    return render(request, 'queries/query1.html', {'form': form, 'data': data})


def query2(request):
    with connection.cursor() as cursor:
        cursor.execute("select chief_name, chief_age, chief_address, department_name from organization_thelead inner "
                       "join organization_department on organization_thelead.id = organization_department.chief_id")

        data = dict_fetchall(cursor)
    return render(request, 'queries/query2.html', {'data': data})


def query3(request):
    contracts_data = None
    projects_data = None

    if request.method == 'POST':
        form = Query3Form(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                from_date = form.cleaned_data.get("from_date")
                to_date = form.cleaned_data.get("to_date")

                cursor.execute("select contract_info, group_name, beginning_of_work, end_of_work from "
                               "organization_contract inner join organization_groupscontracts on "
                               "organization_contract.id = organization_groupscontracts.contract_id inner join "
                               "organization_thegroup on organization_groupscontracts.group_id = "
                               "organization_thegroup.id where ('{0}' between "
                               "organization_groupscontracts.beginning_of_work and "
                               "organization_groupscontracts.end_of_work) or ('{1}' between "
                               "organization_groupscontracts.beginning_of_work and "
                               "organization_groupscontracts.end_of_work) or ("
                               "organization_groupscontracts.beginning_of_work >= '{0}' and "
                               "organization_groupscontracts.end_of_work <= '{1}')".format(from_date, to_date))

                contracts_data = dict_fetchall(cursor)

                cursor.execute("select project_info, group_name, beginning_of_work, end_of_work, work_price, "
                               "subcontractor_info from organization_project inner join organization_groupsprojects "
                               "on organization_project.id = organization_groupsprojects.project_id inner join "
                               "organization_thegroup on organization_groupsprojects.group_id = "
                               "organization_thegroup.id left join organization_subcontractor on "
                               "organization_groupsprojects.subcontractor_id = organization_subcontractor.id where ("
                               "'{0}' between organization_groupsprojects.beginning_of_work and "
                               "organization_groupsprojects.end_of_work) or ('{1}' between "
                               "organization_groupsprojects.beginning_of_work and "
                               "organization_groupsprojects.end_of_work) or ("
                               "organization_groupsprojects.beginning_of_work >= '{0}' and "
                               "organization_groupsprojects.end_of_work <= '{1}')".format(from_date, to_date))

                projects_data = dict_fetchall(cursor)

    else:
        form = Query3Form()
    return render(request, 'queries/query3.html',
                  {'form': form, 'contracts_data': contracts_data, 'projects_data': projects_data})


def query4(request):
    contract_form = Query4ContractForm()
    project_form = Query4ProjectForm()

    contract_data = None
    project_data = None

    if request.method == 'POST':
        if 'contract_form_request' in request.POST:
            contract_form = Query4ContractForm(request.POST)
            if contract_form.is_valid():
                with connection.cursor() as cursor:
                    contract = contract_form.cleaned_data.get("contract").pk

                    cursor.execute("select contract_info, project_info, project_price, project_sign_time, "
                                   "project_end_time from organization_contract inner join "
                                   "organization_contractsprojects oc on organization_contract.id = oc.contract_id "
                                   "inner join organization_project op on oc.project_id = op.id where contract_id = "
                                   "%s" % contract)

                    contract_data = dict_fetchall(cursor)

        if 'project_form_request' in request.POST:
            project_form = Query4ProjectForm(request.POST)
            if project_form.is_valid():
                with connection.cursor() as cursor:
                    project = project_form.cleaned_data.get("project").pk

                    cursor.execute("select project_info, contract_info, contract_sign_time, contract_end_time from "
                                   "organization_project inner join organization_contractsprojects oc on "
                                   "organization_project.id = oc.project_id inner join organization_contract orc on "
                                   "oc.contract_id = orc.id where project_id = %s" % project)  # check this

                    project_data = dict_fetchall(cursor)

    else:
        contract_form = Query4ContractForm()
        project_form = Query4ProjectForm()

    return render(request, 'queries/query4.html', {'contract_form': contract_form,
                                                   'contract_data': contract_data,
                                                   'project_form': project_form,
                                                   'project_data': project_data})


def query5(request):
    contracts_data = None
    projects_data = None

    if request.method == 'POST':
        form = Query5Form(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                from_date = form.cleaned_data.get("from_date")
                to_date = form.cleaned_data.get("to_date")

                cursor.execute("select contract_info, contract_sign_time, contract_end_time, sum(project_price) as "
                               "contract_price from organization_contract inner join organization_contractsprojects "
                               "oc on organization_contract.id = oc.contract_id inner join organization_project op on "
                               "oc.project_id = op.id where contract_end_time between '{0}' and '{1}' "
                               "group by contract_info, contract_sign_time, contract_end_time".format(from_date,
                                                                                                      to_date))

                contracts_data = dict_fetchall(cursor)

                cursor.execute("select project_info, project_sign_time, project_end_time, project_price from "
                               "organization_project where project_end_time between '{0}' and "
                               "'{1}'".format(from_date, to_date))

                projects_data = dict_fetchall(cursor)

    else:
        form = Query5Form()
    return render(request, 'queries/query5.html',
                  {'form': form, 'contracts_data': contracts_data, 'projects_data': projects_data})


def query6(request):
    data = None

    if request.method == 'POST':
        form = Query6Form(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                date_point = form.cleaned_data.get("date_point")

                cursor.execute("select equipment_name, signed_start_date, signed_end_date, group_name from "
                               "organization_equipment inner join organization_groupsequipment og on "
                               "organization_equipment.id = og.equipment_id inner join organization_thegroup ot on "
                               "og.group_id = ot.id where '{0}' between signed_start_date and signed_end_date".format(
                    date_point))

                data = dict_fetchall(cursor)
    else:
        form = Query6Form()
    return render(request, 'queries/query6.html', {'form': form, 'data': data})


def query7(request):
    contract_form = Query7ContractForm()
    project_form = Query7ProjectForm()

    contract_data = None
    project_data = None

    if request.method == 'POST':
        if 'contract_form_request' in request.POST:
            contract_form = Query7ContractForm(request.POST)
            if contract_form.is_valid():
                with connection.cursor() as cursor:
                    contract = contract_form.cleaned_data.get("contract").pk

                    cursor.execute("select contract_info, beginning_of_work, end_of_work, group_name, equipment_name, "
                                   "signed_start_date, signed_end_date from organization_contract inner join "
                                   "organization_groupscontracts og on organization_contract.id = og.contract_id "
                                   "inner join organization_thegroup ot on og.group_id = ot.id inner join "
                                   "organization_groupsequipment o on ot.id = o.group_id inner join "
                                   "organization_equipment oe on o.equipment_id = oe.id where ((signed_start_date "
                                   "between beginning_of_work and  end_of_work) or (signed_end_date between "
                                   "beginning_of_work and end_of_work) or (beginning_of_work >= signed_start_date and "
                                   "end_of_work <= signed_end_date)) and contract_id = %s" % contract)

                    contract_data = dict_fetchall(cursor)

        if 'project_form_request' in request.POST:
            project_form = Query7ProjectForm(request.POST)
            if project_form.is_valid():
                with connection.cursor() as cursor:
                    project = project_form.cleaned_data.get("project").pk

                    cursor.execute(
                        "select project_info, beginning_of_work, end_of_work, work_price,group_name, equipment_name, "
                        "signed_start_date, signed_end_date from organization_project inner join "
                        "organization_groupsprojects og on organization_project.id = og.project_id inner join "
                        "organization_thegroup ot on og.group_id = ot.id inner join organization_groupsequipment o on "
                        "ot.id = o.group_id inner join organization_equipment oe on o.equipment_id = oe.id where (("
                        "signed_start_date between beginning_of_work and  end_of_work) or (signed_end_date between "
                        "beginning_of_work and end_of_work) or (beginning_of_work >= signed_start_date and "
                        "end_of_work <= signed_end_date)) and project_id = %s" % project)

                    project_data = dict_fetchall(cursor)

    else:
        contract_form = Query7ContractForm()
        project_form = Query7ProjectForm()

    return render(request, 'queries/query7.html', {'contract_form': contract_form,
                                                   'contract_data': contract_data,
                                                   'project_form': project_form,
                                                   'project_data': project_data})


def query8(request):
    worker_form = Query8WorkerForm()
    category_form = Query8CategoryForm()

    worker_data_contracts = None
    worker_data_projects = None
    category_data_contracts = None
    category_data_projects = None

    if request.method == 'POST':
        if 'worker_form_request' in request.POST:
            worker_form = Query8WorkerForm(request.POST)
            if worker_form.is_valid():
                with connection.cursor() as cursor:
                    worker = worker_form.cleaned_data.get("worker").pk
                    worker_from_date = worker_form.cleaned_data.get("worker_from_date")
                    worker_to_date = worker_form.cleaned_data.get("worker_to_date")

                    cursor.execute("select worker_name, group_name, appointment_date, dismissal_date, contract_info, "
                                   "beginning_of_work, end_of_work from organization_worker inner join "
                                   "organization_workersgroups ow on "
                                   "organization_worker.id = ow.worker_id inner join organization_thegroup ot on "
                                   "ow.group_id = ot.id inner join organization_groupscontracts og on ot.id = "
                                   "og.group_id inner join organization_contract oc on og.contract_id = oc.id where ("
                                   "(appointment_date between '{0}' and '{1}') or (dismissal_date "
                                   "between '{0}' and '{1}') or (appointment_date <= '{0}' and "
                                   "dismissal_date >= '{1}') or (appointment_date <= '{1}' and "
                                   "dismissal_date is null )) and ((beginning_of_work between '{0}' and "
                                   "'{1}') or (end_of_work between '{0}' and '{1}') or ("
                                   "beginning_of_work <= '{0}' and end_of_work >= '{1}')) and "
                                   "organization_worker.id = {2} and ((appointment_date between beginning_of_work and "
                                   "end_of_work) or (dismissal_date between beginning_of_work and end_of_work) or ("
                                   "appointment_date <= beginning_of_work and dismissal_date >= "
                                   "end_of_work) or (appointment_date <= end_of_work and dismissal_date is null))".format(
                        worker_from_date, worker_to_date, worker))

                    worker_data_contracts = dict_fetchall(cursor)

                    cursor.execute("select worker_name, group_name, appointment_date, dismissal_date, project_info, "
                                   "beginning_of_work, end_of_work, work_price from organization_worker inner join "
                                   "organization_workersgroups ow on "
                                   "organization_worker.id = ow.worker_id inner join organization_thegroup ot on "
                                   "ow.group_id = ot.id inner join organization_groupsprojects og on ot.id = "
                                   "og.group_id inner join organization_project op on og.project_id = op.id where (("
                                   "appointment_date between '{0}' and '{1}') or (dismissal_date "
                                   "between '{0}' and '{1}') or (appointment_date <= '{0}' and "
                                   "dismissal_date >= '{1}') or (appointment_date <= '{1}' and "
                                   "dismissal_date is null )) and ((beginning_of_work between '{0}' and "
                                   "'{1}') or (end_of_work between '{0}' and '{1}') or ("
                                   "beginning_of_work <= '{0}' and end_of_work >= '{1}')) and "
                                   "organization_worker.id = {2} and ((appointment_date between beginning_of_work and "
                                   "end_of_work) or (dismissal_date between beginning_of_work and end_of_work) or ("
                                   "appointment_date <= beginning_of_work and dismissal_date >= "
                                   "end_of_work) or (appointment_date <= end_of_work and dismissal_date is null))".format(
                        worker_from_date, worker_to_date, worker))

                    worker_data_projects = dict_fetchall(cursor)

        if 'category_form_request' in request.POST:
            category_form = Query8CategoryForm(request.POST)
            if category_form.is_valid():
                with connection.cursor() as cursor:
                    category = category_form.cleaned_data.get("category").pk
                    category_from_date = category_form.cleaned_data.get("category_from_date")
                    category_to_date = category_form.cleaned_data.get("category_to_date")

                    cursor.execute(
                        "select worker_name, worker_category_id, group_name, appointment_date, dismissal_date, "
                        "contract_info, beginning_of_work, end_of_work from organization_worker inner join "
                        "organization_workersgroups ow on "
                        "organization_worker.id = ow.worker_id inner join organization_thegroup ot on ow.group_id = "
                        "ot.id inner join organization_groupscontracts og on ot.id = og.group_id inner join "
                        "organization_contract oc on og.contract_id = oc.id where ((appointment_date between "
                        "'{0}' and '{1}') or (dismissal_date between '{0}' and '{1}') or "
                        "(appointment_date <= '{0}' and dismissal_date >= '{1}') or (appointment_date "
                        "<= '{1}' and dismissal_date is null )) and ((beginning_of_work between '{0}' "
                        "and '{1}') or (end_of_work between '{0}' and '{1}') or ("
                        "beginning_of_work <= '{0}' and end_of_work >= '{1}')) and "
                        "organization_worker.worker_category_id = {2} and ((appointment_date between "
                        "beginning_of_work and end_of_work) or (dismissal_date between beginning_of_work and "
                        "end_of_work) or (appointment_date <= beginning_of_work and dismissal_date >= "
                        "end_of_work) or (appointment_date <= end_of_work and dismissal_date is null))".format(
                            category_from_date, category_to_date,
                            category))

                    category_data_contracts = dict_fetchall(cursor)

                    cursor.execute(
                        "select worker_name, worker_category_id, group_name, appointment_date, dismissal_date, "
                        "project_info, beginning_of_work, end_of_work, work_price from organization_worker inner join "
                        "organization_workersgroups ow on "
                        "organization_worker.id = ow.worker_id inner join organization_thegroup ot on ow.group_id = "
                        "ot.id inner join organization_groupsprojects og on ot.id = og.group_id inner join "
                        "organization_project op on og.project_id = op.id where ((appointment_date between "
                        "'{0}' and '{1}') or (dismissal_date between '{0}' and '{1}') or "
                        "(appointment_date <= '{0}' and dismissal_date >= '{1}') or (appointment_date "
                        "<= '{1}' and dismissal_date is null )) and ((beginning_of_work between '{0}' "
                        "and '{1}') or (end_of_work between '{0}' and '{1}') or ("
                        "beginning_of_work <= '{0}' and end_of_work >= '{1}')) and "
                        "organization_worker.worker_category_id = {2} and ((appointment_date between "
                        "beginning_of_work and end_of_work) or (dismissal_date between beginning_of_work and "
                        "end_of_work) or (appointment_date <= beginning_of_work and dismissal_date >= "
                        "end_of_work) or (appointment_date <= end_of_work and dismissal_date is null))".format(
                            category_from_date, category_to_date, category))

                    category_data_projects = dict_fetchall(cursor)

    else:
        worker_form = Query8WorkerForm()
        category_form = Query8CategoryForm()

    return render(request, 'queries/query8.html', {'worker_form': worker_form,
                                                   'worker_data_contracts': worker_data_contracts,
                                                   'worker_data_projects': worker_data_projects,
                                                   'category_form': category_form,
                                                   'category_data_contracts': category_data_contracts,
                                                   'category_data_projects': category_data_projects})


def query9(request):
    with connection.cursor() as cursor:
        cursor.execute("select subcontractor_info, project_info, beginning_of_work, end_of_work, work_price from "
                       "organization_subcontractor inner join organization_groupsprojects og on "
                       "organization_subcontractor.id = og.subcontractor_id inner join organization_project op on "
                       "og.project_id = op.id")

        data = dict_fetchall(cursor)
    return render(request, 'queries/query9.html', {'data': data})


def query10(request):
    data_with_categories = None
    data_all_workers = None

    if request.method == 'POST':
        form = Query10Form(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                category = form.cleaned_data.get("category").pk
                project = form.cleaned_data.get("project").pk
                from_date = form.cleaned_data.get("from_date")
                to_date = form.cleaned_data.get("to_date")

                cursor.execute("select worker_name, category_name, group_name, appointment_date, dismissal_date, "
                               "project_info, work_price, beginning_of_work, end_of_work  from organization_project "
                               "inner join organization_groupsprojects og on organization_project.id = og.project_id "
                               "inner join organization_thegroup ot on og.group_id = ot.id inner join "
                               "organization_workersgroups ow on ot.id = ow.group_id inner join organization_worker o "
                               "on ow.worker_id = o.id inner join organization_category oc on o.worker_category_id = "
                               "oc.id where ((appointment_date between '{0}' and '{1}') or ("
                               "dismissal_date between '{0}' and '{1}') or (appointment_date <= "
                               "'{0}' and dismissal_date >= '{1}') or (appointment_date <= '{1}' "
                               "and dismissal_date is null )) and ((beginning_of_work between '{0}' and "
                               "'{1}') or (end_of_work between '{0}' and '{1}') or ("
                               "beginning_of_work <= '{0}' and end_of_work >= '{1}')) and "
                               "o.worker_category_id = {2} and organization_project.id = {3} and ((appointment_date "
                               "between beginning_of_work and end_of_work) or (dismissal_date between "
                               "beginning_of_work and end_of_work) or (appointment_date <= beginning_of_work and "
                               "dismissal_date >= end_of_work) or (appointment_date <= end_of_work and dismissal_date "
                               "is null))".format(from_date, to_date, category, project))

                data_with_categories = dict_fetchall(cursor)

                cursor.execute("select worker_name, category_name, group_name, appointment_date, dismissal_date, "
                               "project_info, work_price, beginning_of_work, end_of_work  from organization_project "
                               "inner join organization_groupsprojects og on organization_project.id = og.project_id "
                               "inner join organization_thegroup ot on og.group_id = ot.id inner join "
                               "organization_workersgroups ow on ot.id = ow.group_id inner join organization_worker o "
                               "on ow.worker_id = o.id inner join organization_category oc on o.worker_category_id = "
                               "oc.id where ((appointment_date between '{0}' and '{1}') or ("
                               "dismissal_date between '{0}' and '{1}') or (appointment_date <= "
                               "'{0}' and dismissal_date >= '{1}') or (appointment_date <= '{1}' "
                               "and dismissal_date is null )) and ((beginning_of_work between '{0}' and "
                               "'{1}') or (end_of_work between '{0}' and '{1}') or ("
                               "beginning_of_work <= '{0}' and end_of_work >= '{1}')) and "
                               "organization_project.id = {2} and ((appointment_date "
                               "between beginning_of_work and end_of_work) or (dismissal_date between "
                               "beginning_of_work and end_of_work) or (appointment_date <= beginning_of_work and "
                               "dismissal_date >= end_of_work) or (appointment_date <= end_of_work and dismissal_date "
                               "is null))".format(from_date, to_date, project))

                data_all_workers = dict_fetchall(cursor)

    else:
        form = Query10Form()
    return render(request, 'queries/query10.html',
                  {'form': form, 'data_with_categories': data_with_categories, 'data_all_workers': data_all_workers})


def query11(request):
    efficiency_data = None
    data = None

    if request.method == 'POST':
        form = Query11Form(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                equipment = form.cleaned_data.get("equipment").pk

                cursor.execute("select equipment_name, count(equipment_name)/(select count(*) from "
                               "organization_groupsprojects)*100 as project_works_total from organization_equipment "
                               "inner join organization_groupsequipment og on organization_equipment.id = "
                               "og.equipment_id inner join organization_thegroup ot on og.group_id = ot.id inner join "
                               "organization_groupsprojects o on ot.id = o.group_id inner join organization_project "
                               "op on o.project_id = op.id where ((signed_start_date between beginning_of_work and  "
                               "end_of_work) or (signed_end_date between beginning_of_work and end_of_work) or ("
                               "beginning_of_work >= signed_start_date and end_of_work <= signed_end_date)) and "
                               "equipment_id = {0} group by equipment_name".format(equipment))

                efficiency_data = dict_fetchall(cursor)

                cursor.execute("select equipment_name, signed_start_date, signed_end_date, group_name, "
                               "beginning_of_work, end_of_work, project_info, work_price from organization_equipment "
                               "inner join organization_groupsequipment og on organization_equipment.id = "
                               "og.equipment_id inner join organization_thegroup ot on og.group_id = ot.id inner join "
                               "organization_groupsprojects o on ot.id = o.group_id inner join organization_project "
                               "op on o.project_id = op.id where ((signed_start_date between beginning_of_work and  "
                               "end_of_work) or (signed_end_date between beginning_of_work and end_of_work) or ("
                               "beginning_of_work >= signed_start_date and end_of_work <= signed_end_date)) and "
                               "equipment_id = {0}".format(equipment))

                data = dict_fetchall(cursor)

    else:
        form = Query11Form()
    return render(request, 'queries/query11.html',
                  {'form': form, 'efficiency_data': efficiency_data, 'data': data})


def query12(request):
    with connection.cursor() as cursor:
        cursor.execute("select contract_info, contract_price, sum(datediff(end_of_work, beginning_of_work)) as "
                       "group_days_consumed, (contract_price / sum(datediff(end_of_work, beginning_of_work))) as "
                       "efficiency from (select contract_id, contract_info, sum(project_price) as contract_price from "
                       "organization_contract inner join organization_contractsprojects oc on "
                       "organization_contract.id = oc.contract_id inner join organization_project op on oc.project_id "
                       "= op.id group by contract_info) as cis inner join organization_groupscontracts on "
                       "cis.contract_id = organization_groupscontracts.contract_id group by contract_info, "
                       "contract_price order by efficiency desc")

        data = dict_fetchall(cursor)
    return render(request, 'queries/query12.html', {'data': data})


def query13(request):
    data_with_categories = None
    data_all_workers = None

    if request.method == 'POST':
        form = Query13Form(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                category = form.cleaned_data.get("category").pk
                from_date = form.cleaned_data.get("from_date")
                to_date = form.cleaned_data.get("to_date")

                cursor.execute("select worker_name, category_name, group_name, appointment_date, dismissal_date, "
                               "project_info, work_price, beginning_of_work, end_of_work  from organization_project "
                               "inner join organization_groupsprojects og on organization_project.id = og.project_id "
                               "inner join organization_thegroup ot on og.group_id = ot.id inner join "
                               "organization_workersgroups ow on ot.id = ow.group_id inner join organization_worker o "
                               "on ow.worker_id = o.id inner join organization_category oc on o.worker_category_id = "
                               "oc.id where ((appointment_date between '{0}' and '{1}') or ("
                               "dismissal_date between '{0}' and '{1}') or (appointment_date <= "
                               "'{0}' and dismissal_date >= '{1}') or (appointment_date <= '{1}' "
                               "and dismissal_date is null )) and ((beginning_of_work between '{0}' and "
                               "'{1}') or (end_of_work between '{0}' and '{1}') or ("
                               "beginning_of_work <= '{0}' and end_of_work >= '{1}')) and "
                               "o.worker_category_id = {2} and ((appointment_date "
                               "between beginning_of_work and end_of_work) or (dismissal_date between "
                               "beginning_of_work and end_of_work) or (appointment_date <= beginning_of_work and "
                               "dismissal_date >= end_of_work) or (appointment_date <= end_of_work and dismissal_date "
                               "is null))".format(from_date, to_date, category))

                data_with_categories = dict_fetchall(cursor)

                cursor.execute("select worker_name, category_name, group_name, appointment_date, dismissal_date, "
                               "project_info, work_price, beginning_of_work, end_of_work  from organization_project "
                               "inner join organization_groupsprojects og on organization_project.id = og.project_id "
                               "inner join organization_thegroup ot on og.group_id = ot.id inner join "
                               "organization_workersgroups ow on ot.id = ow.group_id inner join organization_worker o "
                               "on ow.worker_id = o.id inner join organization_category oc on o.worker_category_id = "
                               "oc.id where ((appointment_date between '{0}' and '{1}') or ("
                               "dismissal_date between '{0}' and '{1}') or (appointment_date <= "
                               "'{0}' and dismissal_date >= '{1}') or (appointment_date <= '{1}' "
                               "and dismissal_date is null )) and ((beginning_of_work between '{0}' and "
                               "'{1}') or (end_of_work between '{0}' and '{1}') or ("
                               "beginning_of_work <= '{0}' and end_of_work >= '{1}')) and "
                               "((appointment_date "
                               "between beginning_of_work and end_of_work) or (dismissal_date between "
                               "beginning_of_work and end_of_work) or (appointment_date <= beginning_of_work and "
                               "dismissal_date >= end_of_work) or (appointment_date <= end_of_work and dismissal_date "
                               "is null))".format(from_date, to_date))

                data_all_workers = dict_fetchall(cursor)

    else:
        form = Query13Form()
    return render(request, 'queries/query13.html',
                  {'form': form, 'data_with_categories': data_with_categories, 'data_all_workers': data_all_workers})


def query14(request):
    with connection.cursor() as cursor:
        cursor.execute("select project_info, project_price, sum(datediff(end_of_work, beginning_of_work)) as "
                       "group_days_consumed, (project_price / sum(datediff(end_of_work, beginning_of_work))) as "
                       "efficiency from (select id, project_info, project_price from organization_project) as cis "
                       "inner join organization_groupsprojects on cis.id = organization_groupsprojects.project_id "
                       "group by project_info, project_price order by efficiency desc")

        data = dict_fetchall(cursor)
    return render(request, 'queries/query14.html', {'data': data})
