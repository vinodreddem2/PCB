from django.contrib import admin
from .models import *

admin.site.register(FeeStructure)
admin.site.register(StudentFee)
admin.site.register(DetailedStudentFee)
admin.site.register(FeePaymentTransaction)
admin.site.register(SalaryStructure)
admin.site.register(TeacherSalary)
admin.site.register(TeacherSalaryDeductions)
admin.site.register(TeacherSalaryStructure)
