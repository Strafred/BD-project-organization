from django.contrib import admin

from . import models
# Register your models here.

admin.site.register(models.Category)
admin.site.register(models.Worker)
admin.site.register(models.TheLead)
admin.site.register(models.Department)
admin.site.register(models.EngineerCategory)
admin.site.register(models.ConstructorCategory)
admin.site.register(models.TechniqueCategory)
admin.site.register(models.LabAssistantCategory)
admin.site.register(models.ServiceStaffCategory)
admin.site.register(models.Equipment)
admin.site.register(models.EquipmentInDepartments)
admin.site.register(models.TheGroup)
admin.site.register(models.Subcontractor)
admin.site.register(models.Project)
admin.site.register(models.Contract)
admin.site.register(models.GroupsContracts)
admin.site.register(models.WorkersGroups)
admin.site.register(models.ClientsContracts)
admin.site.register(models.ContractsProjects)
admin.site.register(models.GroupsProjects)
admin.site.register(models.GroupsEquipment)
admin.site.register(models.Client)
