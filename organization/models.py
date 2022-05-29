from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


@receiver(pre_delete)
def delete_repo(sender, instance, **kwargs):
    if sender == ServiceStaffCategory or sender == LabAssistantCategory or sender == TechniqueCategory or sender == EngineerCategory or sender == ConstructorCategory:
        instance.worker.worker_category_id = None
        Worker.save(instance.worker)


class TheLead(models.Model):
    chief_name = models.CharField(max_length=60)
    chief_age = models.IntegerField(null=True, blank=True)
    chief_address = models.CharField(max_length=80)

    def __str__(self):
        return self.chief_name + " | age: " + str(self.chief_age) + " | address: " + self.chief_address

    class Meta:
        verbose_name_plural = "2-1. TheLead"


class Category(models.Model):
    category_salary = models.IntegerField(default=0)
    category_name = models.CharField(max_length=100, editable=False)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "1. Categories"


class Department(models.Model):
    department_name = models.CharField(max_length=100)
    chief = models.ForeignKey(TheLead, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.department_name

    class Meta:
        verbose_name_plural = "2. Departments"


class Equipment(models.Model):
    equipment_name = models.CharField(max_length=60)
    assigned_departments = models.ManyToManyField(
        Department,
        through='EquipmentInDepartments',
        through_fields=('equipment', 'department')
    )

    def __str__(self):
        return self.equipment_name

    class Meta:
        verbose_name_plural = "3. Equipment"


class TheGroup(models.Model):
    group_name = models.CharField(max_length=80)
    assigned_equipment = models.ManyToManyField(
        Equipment,
        through="GroupsEquipment",
        through_fields=('group', 'equipment')
    )

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name_plural = "4. Groups"


class Worker(models.Model):
    worker_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, editable=False)
    worker_name = models.CharField(max_length=60)
    worker_age = models.IntegerField(null=True, blank=True)
    worker_address = models.CharField(max_length=80)
    assigned_departments = models.ManyToManyField(Department)
    assigned_groups = models.ManyToManyField(
        TheGroup,
        through="WorkersGroups",
        through_fields=('worker', 'group')
    )

    def __str__(self):
        return self.worker_name + " | " + self.worker_category.__str__()

    class Meta:
        verbose_name_plural = "0. Workers"


class Subcontractor(models.Model):
    subcontractor_info = models.CharField(max_length=255)

    def __str__(self):
        return self.subcontractor_info

    class Meta:
        verbose_name_plural = "8. Subcontractors"


class Project(models.Model):
    project_sign_time = models.DateField(null=True, blank=True)
    project_end_time = models.DateField(null=True, blank=True)
    project_price = models.IntegerField()
    project_info = models.CharField(max_length=255)
    leader = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_groups = models.ManyToManyField(
        TheGroup,
        through="GroupsProjects",
        through_fields=('project', 'group')
    )

    def __str__(self):
        return self.project_info + " | leader: " + self.leader.__str__() + \
               " | signed: " + str(self.project_sign_time) + " | unsigned: " \
               + str(self.project_end_time)

    class Meta:
        verbose_name_plural = "6. Projects"


class Contract(models.Model):
    contract_sign_time = models.DateField(null=True, blank=True)
    contract_end_time = models.DateField(null=True, blank=True)
    contract_info = models.CharField(max_length=255)
    leader = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_projects = models.ManyToManyField(
        Project,
        through="ContractsProjects",
        through_fields=('contract', 'project')
    )
    assigned_groups = models.ManyToManyField(
        TheGroup,
        through="GroupsContracts",
        through_fields=('contract', 'group')
    )

    def __str__(self):
        return self.contract_info + " | leader: " + self.leader.__str__() + \
               " | signed: " + str(self.contract_sign_time) + " | unsigned: " \
               + str(self.contract_end_time)

    class Meta:
        verbose_name_plural = "7. Contracts"


class GroupsContracts(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(TheGroup, on_delete=models.SET_NULL, null=True, blank=True)
    beginning_of_work = models.DateField(null=True, blank=True)
    end_of_work = models.DateField(null=True, blank=True)

    def __str__(self):
        return "Contract: " + self.contract.contract_info + " | Group: " + self.group.__str__() + \
               " | start: " + str(self.beginning_of_work) + " | end: " \
               + str(self.end_of_work)

    class Meta:
        verbose_name_plural = "4-2. Groups Contracts"


class GroupsProjects(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(TheGroup, on_delete=models.SET_NULL, null=True, blank=True)
    subcontractor = models.ForeignKey(Subcontractor, on_delete=models.SET_NULL, null=True, blank=True)
    beginning_of_work = models.DateField(null=True, blank=True)
    end_of_work = models.DateField(null=True, blank=True)
    work_price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "Project: " + self.project.project_info + " | Group: " + self.group.__str__() + \
               " | start: " + str(self.beginning_of_work) + " | end: " \
               + str(self.end_of_work)

    class Meta:
        verbose_name_plural = "4-3. Groups Projects"


class ContractsProjects(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return "Contract: " + self.contract.contract_info + " | Project: " + self.project.project_info

    class Meta:
        verbose_name_plural = "7-1. Contracts Projects"


class Client(models.Model):
    client_name = models.CharField(max_length=60)
    client_address = models.CharField(max_length=80)
    client_business = models.CharField(max_length=80)
    assigned_contracts = models.ManyToManyField(
        Contract,
        through="ClientsContracts",
        through_fields=('client', 'contract')
    )

    def __str__(self):
        return self.client_name + " | " + self.client_business

    class Meta:
        verbose_name_plural = "5. Clients"


class ClientsContracts(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

    def __str__(self):
        return "Client: " + self.client.__str__() + " | Contract: " + self.contract.contract_info + \
               " | signed: " + str(self.contract.contract_sign_time) + " | unsigned: " \
               + str(self.contract.contract_end_time)

    class Meta:
        verbose_name_plural = "5-1. Clients Contracts"


class WorkersGroups(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    group = models.ForeignKey(TheGroup, on_delete=models.CASCADE)
    appointment_date = models.DateField(null=True, blank=True)
    dismissal_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.worker.__str__() + " | " + self.group.__str__() + \
               " | signed: " + str(self.appointment_date) + " | unsigned: " \
               + str(self.dismissal_date)

    class Meta:
        verbose_name_plural = "4-0. Groups Workers"


class GroupsEquipment(models.Model):
    group = models.ForeignKey(TheGroup, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    signed_start_date = models.DateField(null=True, blank=True)
    signed_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.group.__str__() + " | " + self.equipment.__str__() + \
               " | signed: " + str(self.signed_start_date) + " | unsigned: " \
               + str(self.signed_end_date)

    class Meta:
        verbose_name_plural = "4-1. Groups Equipment"


class EquipmentInDepartments(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    signed_date = models.DateField(null=True, blank=True)
    unsigned_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.equipment.__str__() + " | " + self.department.__str__() + \
               " | signed: " + str(self.signed_date) + " | unsigned: " \
               + str(self.unsigned_date)

    class Meta:
        verbose_name_plural = "3-1. Equipment In Departments"


class EngineerCategory(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.worker.worker_category_id == 2:
            ConstructorCategory.objects.filter(worker=self.worker).delete()
        if self.worker.worker_category_id == 3:
            TechniqueCategory.objects.filter(worker=self.worker).delete()
        if self.worker.worker_category_id == 4:
            LabAssistantCategory.objects.filter(worker=self.worker).delete()
        if self.worker.worker_category_id == 5:
            ServiceStaffCategory.objects.filter(worker=self.worker).delete()

        self.worker.worker_category_id = 1
        self.worker.save()
        super(EngineerCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.worker.__str__()

    class Meta:
        verbose_name_plural = "1-1. Engineer Category"


class ConstructorCategory(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    certificates_number = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.worker.worker_category_id == 1:
            EngineerCategory.objects.filter(worker=self.worker).delete()
        if self.worker.worker_category_id == 3:
            TechniqueCategory.objects.filter(worker=self.worker).delete()
        if self.worker.worker_category_id == 4:
            LabAssistantCategory.objects.filter(worker=self.worker).delete()
        if self.worker.worker_category_id == 5:
            ServiceStaffCategory.objects.filter(worker=self.worker).delete()

        self.worker.worker_category_id = 2
        self.worker.save()
        super(ConstructorCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.worker.__str__() + " | " + str(self.certificates_number)

    class Meta:
        verbose_name_plural = "1-2. Constructor Category"


class TechniqueCategory(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    assigned_instruments = models.CharField(max_length=80)
    serviced_equipment = models.CharField(max_length=120)

    def save(self, *args, **kwargs):
        if self.worker.worker_category_id == 1:
            EngineerCategory.objects.filter(worker=self.worker).delete()
        if self.worker.worker_category_id == 2:
            ConstructorCategory.objects.filter(worker=self.worker).delete()
        if self.worker.worker_category_id == 4:
            LabAssistantCategory.objects.filter(worker=self.worker).delete()
        if self.worker.worker_category_id == 5:
            ServiceStaffCategory.objects.filter(worker=self.worker).delete()

        self.worker.worker_category_id = 3
        self.worker.save()
        super(TechniqueCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.worker.__str__() + " | " + self.assigned_instruments

    class Meta:
        verbose_name_plural = "1-3. Technique Category"


class LabAssistantCategory(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    assigned_lab = models.CharField(max_length=60)
    assigned_inventory = models.CharField(max_length=120)

    def save(self, *args, **kwargs):
        if self.worker.worker_category_id == 1:
            EngineerCategory.objects.filter(worker=self.worker).delete()
        if self.worker.worker_category_id == 2:
            ConstructorCategory.objects.filter(worker=self.worker).delete()
        if self.worker.worker_category_id == 3:
            TechniqueCategory.objects.filter(worker=self.worker).delete()
        if self.worker.worker_category_id == 5:
            ServiceStaffCategory.objects.filter(worker=self.worker).delete()

        self.worker.worker_category_id = 4
        self.worker.save()
        super(LabAssistantCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.worker.__str__() + " | " + self.assigned_lab

    class Meta:
        verbose_name_plural = "1-4. Lab Assistant Category"


class ServiceStaffCategory(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    service_zone = models.CharField(max_length=60)

    def save(self, *args, **kwargs):
        if self.worker.worker_category_id == 1:
            EngineerCategory.objects.filter(worker=self.worker).delete()
        if self.worker.worker_category_id == 2:
            ConstructorCategory.objects.filter(worker=self.worker).delete()
        if self.worker.worker_category_id == 3:
            TechniqueCategory.objects.filter(worker=self.worker).delete()
        if self.worker.worker_category_id == 4:
            LabAssistantCategory.objects.filter(worker=self.worker).delete()

        self.worker.worker_category_id = 5
        self.worker.save()
        super(ServiceStaffCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.worker.__str__() + " | " + self.service_zone

    class Meta:
        verbose_name_plural = "1-5. Service Staff Category"
