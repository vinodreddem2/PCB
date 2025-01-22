import uuid
from django.db import models
from masters.models.BaseModel import BaseModel

class FeeStructure(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column="ID")
    organization = models.ForeignKey("masters.Organization", on_delete=models.CASCADE, db_column="ORGANIZATION_ID")
    name = models.CharField(max_length=255, db_column="NAME")
    description = models.TextField(blank=True, null=True, db_column="DESCRIPTION")
    default_amount = models.FloatField(blank=True, null=True, db_column="DEFAULT_AMOUNT")

    class Meta:
        db_table = "FEE_STRUCTURE"

    def __str__(self):
        return self.name


class StudentFee(BaseModel):
    id = models.AutoField(primary_key=True, db_column="ID")
    student = models.OneToOneField("students.Student", on_delete=models.CASCADE, db_column="STUDENT_ID")
    total_fee = models.FloatField(db_column="TOTAL_FEE")
    paid_fee = models.FloatField(default=0.00, db_column="PAID_FEE")
    outstanding_balance = models.FloatField(db_column="OUTSTANDING_BALANCE")

    def save(self, *args, **kwargs):
        self.outstanding_balance = self.total_fee - self.paid_fee
        super().save(*args, **kwargs)

    class Meta:
        db_table = "STUDENT_FEE"

    def __str__(self):
        return f"StudentFee({self.student}, Total: {self.total_fee})"


class DetailedStudentFee(BaseModel):
    id = models.AutoField(primary_key=True, db_column="ID")
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, db_column="STUDENT_ID")
    student_fee = models.ForeignKey(StudentFee, on_delete=models.CASCADE, db_column="STUDENT_FEE_ID")
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, db_column="FEE_STRUCTURE_ID")
    total_amount = models.FloatField(db_column="TOTAL_AMOUNT")
    discounted_amount = models.FloatField(default=0.00, db_column="DISCOUNTED_AMOUNT")
    discounted_reason = models.TextField(blank=True, null=True, db_column="DISCOUNTED_REASON")

    class Meta:
        db_table = "DETAILED_STUDENT_FEE"

    def __str__(self):
        return f"Detail({self.student}, Fee: {self.fee_structure}, Discount: {self.discounted_amount})"


class FeePaymentTransaction(BaseModel):
    PAYMENT_METHODS = [
        ("CASH", "Cash"),
        ("CARD", "Card"),
        ("UPI", "UPI"),
        ("BANK", "Bank Transfer"),
        ("ONLINE", "Online Payment"),
    ]

    id = models.AutoField(primary_key=True, db_column="ID")
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, db_column="STUDENT_ID")
    student_fee = models.ForeignKey(StudentFee, on_delete=models.CASCADE, db_column="STUDENT_FEE_ID")
    payment_type = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, db_column="PAYMENT_TYPE")
    amount_paid = models.FloatField(db_column="AMOUNT_PAID")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, db_column="PAYMENT_METHOD")
    transaction_reference = models.CharField(max_length=255, blank=True, null=True, db_column="TRANSACTION_REFERENCE")
    status = models.CharField(max_length=50, default="Pending", db_column="STATUS")
    transaction_date = models.DateTimeField(auto_now_add=True, db_column="TRANSACTION_DATE")
    attachments = models.FileField(upload_to="fee_receipts/", blank=True, null=True, db_column="ATTACHMENTS")

    class Meta:
        db_table = "FEE_PAYMENT_TRANSACTION"

    def __str__(self):
        return f"Transaction({self.student}, {self.amount_paid}, {self.payment_method})"



class SalaryStructure(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column="ID")
    organization = models.ForeignKey("masters.Organization", on_delete=models.CASCADE, db_column="ORGANIZATION_ID")
    name = models.CharField(max_length=255, db_column="NAME")
    description = models.TextField(blank=True, null=True, db_column="DESCRIPTION")

    class Meta:
        db_table = "SALARY_STRUCTURE"

    def __str__(self):
        return self.name


class TeacherSalary(BaseModel):
    id = models.AutoField(primary_key=True, db_column="ID")
    teacher = models.OneToOneField("teachers.Teacher", on_delete=models.CASCADE, db_column="TEACHER_ID")
    total_salary = models.FloatField(db_column="TOTAL_SALARY")
    total_deductions = models.FloatField(default=0.00, db_column="TOTAL_DEDUCTIONS")
    salary_month = models.DateField(db_column="SALARY_MONTH")
    net_salary = models.FloatField(db_column="NET_SALARY")

    def save(self, *args, **kwargs):
        self.net_salary = self.total_salary - self.total_deductions
        super().save(*args, **kwargs)

    class Meta:
        db_table = "TEACHER_SALARY"

    def __str__(self):
        return f"Salary({self.teacher}, Net: {self.net_salary})"


class TeacherSalaryDeductions(BaseModel):
    id = models.AutoField(primary_key=True, db_column="ID")
    teacher = models.ForeignKey("teachers.Teacher", on_delete=models.CASCADE, db_column="TEACHER_ID")
    salary_deduction_id = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE, db_column="SALARY_DEDUCTION_ID")
    deduction_amount = models.FloatField(db_column="DEDUCTION_AMOUNT")
    salary_month = models.DateField(db_column="SALARY_MONTH")

    class Meta:
        db_table = "TEACHER_SALARY_DEDUCTIONS"

    def __str__(self):
        return f"Deduction({self.teacher}, {self.deduction_amount})"


class TeacherSalaryStructure(BaseModel):
    id = models.AutoField(primary_key=True, db_column="ID")
    teacher = models.ForeignKey("teachers.Teacher", on_delete=models.CASCADE, db_column="TEACHER_ID")
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE, db_column="SALARY_STRUCTURE_ID")
    annual_salary = models.FloatField(db_column="ANNUAL_SALARY")
    monthly_salary = models.FloatField(db_column="MONTHLY_SALARY")

    class Meta:
        db_table = "TEACHER_SALARY_STRUCTURE"

    def __str__(self):
        return f"Structure({self.teacher}, Annual: {self.annual_salary})"
