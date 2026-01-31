from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    """A simple model for demonstration purposes."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Application(models.Model):
    """Main application model - Step 1: Client Particulars"""
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
    QUALIFICATION_CHOICES = [
        ('Graduate', 'Graduate'),
        ('Post-Graduate', 'Post-Graduate'),
        ('Other', 'Other'),
    ]
    
    PROF_QUALIFICATION_CHOICES = [
        ('CA', 'CA'),
        ('Engineer', 'Engineer'),
        ('LLB', 'LLB'),
        ('Architect', 'Architect'),
        ('MBBS', 'MBBS'),
        ('Other', 'Other'),
    ]
    
    TEL_OWNER_CHOICES = [
        ('Applicant', 'Applicant'),
        ('Co Applicant', 'Co Applicant'),
        ('Other', 'Other'),
    ]
    
    OVERALL_STATUS_CHOICES = [
        ('Positive', 'Positive'),
        ('Negative', 'Negative'),
        ('Refer to credit', 'Refer to credit'),
    ]
    
    # Link to agent/user who filled the form
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    
    # Step 1: Client Particulars
    applicant_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    file_no = models.CharField(max_length=100, unique=True)
    allocation_date = models.CharField(max_length=20)  # DD/MM/YYYY format
    visit_date = models.CharField(max_length=20)
    dob = models.CharField(max_length=20, blank=True, null=True)
    age = models.PositiveIntegerField()
    qualification = models.CharField(max_length=50, choices=QUALIFICATION_CHOICES)
    other_qualification = models.CharField(max_length=100, blank=True, null=True)
    prof_qualification = models.CharField(max_length=50, choices=PROF_QUALIFICATION_CHOICES)
    other_prof_qualification = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=15)
    tel_owner = models.CharField(max_length=20, choices=TEL_OWNER_CHOICES)
    other_tel_owner = models.CharField(max_length=100, blank=True, null=True)
    residential_address = models.TextField()
    family_members = models.JSONField(default=list)  # Store as list of selected members
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.applicant_name} - {self.file_no}"


class BusinessDetails(models.Model):
    """Step 2 & 3: Business & Financial Details"""
    
    OWNERSHIP_TYPE_CHOICES = [
        ('Partner', 'Partner'),
        ('Proprietor', 'Proprietor'),
        ('Director', 'Director'),
        ('Contractual Employee', 'Contractual Employee'),
    ]
    
    BUSINESS_LOCATION_CHOICES = [
        ('Commercial', 'Commercial'),
        ('Residential', 'Residential'),
    ]
    
    SHOP_OWNERSHIP_CHOICES = [
        ('Owned', 'Owned'),
        ('Rented', 'Rented'),
    ]
    
    TXN_TYPE_CHOICES = [
        ('CASH', 'CASH'),
        ('ONLINE', 'ONLINE'),
    ]
    
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='business_details')
    
    # Step 2 fields
    business_name = models.CharField(max_length=255)
    ownership_type = models.CharField(max_length=50, choices=OWNERSHIP_TYPE_CHOICES)
    business_address = models.TextField()
    visit_address = models.TextField()
    gst_number = models.CharField(max_length=15)
    business_location = models.CharField(max_length=20, choices=BUSINESS_LOCATION_CHOICES)
    gps_location = models.CharField(max_length=100, blank=True, null=True)
    shop_ownership = models.CharField(max_length=20, choices=SHOP_OWNERSHIP_CHOICES)
    rent_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    # Step 3 fields - Business template
    business_relates_to = models.TextField(blank=True, null=True)
    business_since_year = models.PositiveIntegerField(blank=True, null=True)
    turnover = models.CharField(max_length=100, blank=True, null=True)
    net_income = models.CharField(max_length=100, blank=True, null=True)
    stock_value = models.CharField(max_length=100, blank=True, null=True)
    txn_type = models.CharField(max_length=10, choices=TXN_TYPE_CHOICES, default='CASH')
    staff_count = models.PositiveIntegerField(blank=True, null=True)
    monthly_salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    creditors_payment_time = models.CharField(max_length=100, blank=True, null=True)
    debtors_payment_time = models.CharField(max_length=100, blank=True, null=True)
    payment_modes = models.JSONField(default=list)  # Store as list: ['Cash', 'UPI', 'RTGS', etc.]
    purchase_area = models.CharField(max_length=255, blank=True, null=True)
    sale_area = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Business: {self.business_name}"


class BusinessOwner(models.Model):
    """Dynamic owner names for a business"""
    business = models.ForeignKey(BusinessDetails, on_delete=models.CASCADE, related_name='owners')
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class PersonMet(models.Model):
    """Person met during business visit"""
    business = models.ForeignKey(BusinessDetails, on_delete=models.CASCADE, related_name='persons_met')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.name} - {self.phone}"


class CoApplicant(models.Model):
    """Optional Co-Applicant Details - Step 3"""
    
    INVOLVEMENT_CHOICES = [
        ('Same Business', 'Same Business'),
        ('Other Business', 'Other Business'),
        ('Employment', 'Employment'),
        ('Other', 'Other'),
    ]
    
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='co_applicant')
    involvement_type = models.CharField(max_length=50, choices=INVOLVEMENT_CHOICES)
    
    # For 'Other Business' involvement
    business_name = models.CharField(max_length=255, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    registered_name = models.CharField(max_length=255, blank=True, null=True)
    business_relates_to = models.TextField(blank=True, null=True)
    business_since_year = models.PositiveIntegerField(blank=True, null=True)
    turnover = models.CharField(max_length=100, blank=True, null=True)
    net_income = models.CharField(max_length=100, blank=True, null=True)
    stock_value = models.CharField(max_length=100, blank=True, null=True)
    txn_type = models.CharField(max_length=10, blank=True, null=True)
    staff_count = models.PositiveIntegerField(blank=True, null=True)
    monthly_salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    # For 'Employment' involvement
    employer_name = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    yearly_salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    
    # For 'Other' involvement
    other_details = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Co-Applicant for {self.application.applicant_name}"


class OtherBusiness(models.Model):
    """Step 4: Other Businesses (Dynamic)"""
    
    RELATIONSHIP_CHOICES = [
        ('Self', 'Self'),
        ('Other', 'Other'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='other_businesses')
    business_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    address = models.TextField()
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    yearly_income = models.CharField(max_length=100)
    vintage_year = models.PositiveIntegerField()
    remarks = models.TextField()
    
    def __str__(self):
        return f"Other Business: {self.business_name}"


class Loan(models.Model):
    """Step 5: Loan Details (Dynamic)"""
    
    LOAN_TYPE_CHOICES = [
        ('Car loan', 'Car loan'),
        ('Home loan', 'Home loan'),
        ('Personal loan', 'Personal loan'),
        ('Business loan', 'Business loan'),
        ('LAP', 'LAP'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='loans')
    loan_type = models.CharField(max_length=50, choices=LOAN_TYPE_CHOICES)
    bank_name = models.CharField(max_length=255)
    loan_amount = models.CharField(max_length=100)
    emi = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.loan_type} - {self.bank_name}"


class BankAccount(models.Model):
    """Step 5: Bank Account Details (Dynamic)"""
    
    ACCOUNT_TYPE_CHOICES = [
        ('Saving Account', 'Saving Account'),
        ('Current Account', 'Current Account'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='bank_accounts')
    bank_name = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    cc_limit = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.bank_name} - {self.branch}"


class SecurityDetails(models.Model):
    """Step 6: Security & Loan Requirement"""
    
    HOUSE_OWNERSHIP_CHOICES = [
        ('Self', 'Self'),
        ('Spouse', 'Spouse'),
        ('Mother', 'Mother'),
        ('Father', 'Father'),
        ('Other', 'Other'),
    ]
    
    END_USE_CHOICES = [
        ('Home Loan', 'Home Loan'),
        ('Construction Loan', 'Construction Loan'),
        ('Business Expansion', 'Business Expansion'),
        ('Other', 'Other'),
    ]
    
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='security_details')
    house_address = models.TextField()
    house_area = models.DecimalField(max_digits=12, decimal_places=2)  # sq. ft.
    house_market_value = models.DecimalField(max_digits=15, decimal_places=2)
    house_ownership = models.CharField(max_length=20, choices=HOUSE_OWNERSHIP_CHOICES)
    other_house_owner = models.CharField(max_length=255, blank=True, null=True)
    amount_required = models.DecimalField(max_digits=15, decimal_places=2)
    end_use = models.CharField(max_length=50, choices=END_USE_CHOICES)
    other_end_use = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Security for {self.application.applicant_name}"


class Conclusion(models.Model):
    """Step 7: General Observation & Conclusion"""
    
    YES_NO_CHOICES = [
        ('YES', 'YES'),
        ('NO', 'NO'),
    ]
    
    RECEIVED_CHOICES = [
        ('Received', 'Received'),
        ('Not Received', 'Not Received'),
    ]
    
    BUSINESS_SETUP_CHOICES = [
        ('Exists & Satisfactory', 'Exists & Satisfactory'),
        ('Exists & Unsatisfactory', 'Exists & Unsatisfactory'),
        ('Not Exists', 'Not Exists'),
    ]
    
    PICTURES_CHOICES = [
        ('Available & Attached', 'Available & Attached'),
        ('Available but not attached', 'Available but not attached'),
        ('Not Available', 'Not Available'),
    ]
    
    QR_SIGNBOARD_CHOICES = [
        ('Yes - Belongs to Applicant', 'Yes - Belongs to Applicant'),
        ('Yes - Belongs to other', 'Yes - Belongs to other'),
        ('No', 'No'),
    ]
    
    RENT_AGREEMENT_CHOICES = [
        ('NO', 'NO'),
        ('YES', 'YES'),
        ('NA', 'NA'),
    ]
    
    OVERALL_STATUS_CHOICES = [
        ('Positive', 'Positive'),
        ('Negative', 'Negative'),
        ('Refer to credit', 'Refer to credit'),
    ]
    
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='conclusion')
    general_observation = models.TextField()
    
    # Conclusion template fields
    nearby_person1 = models.CharField(max_length=255)
    nearby_person2 = models.CharField(max_length=255)
    sale_invoices = models.CharField(max_length=20, choices=RECEIVED_CHOICES)
    purchase_invoices = models.CharField(max_length=20, choices=RECEIVED_CHOICES)
    business_setup = models.CharField(max_length=30, choices=BUSINESS_SETUP_CHOICES)
    stock_pictures = models.CharField(max_length=30, choices=PICTURES_CHOICES)
    signboard = models.CharField(max_length=5, choices=YES_NO_CHOICES)
    biz_registration = models.CharField(max_length=5, choices=YES_NO_CHOICES)
    education_proof = models.CharField(max_length=5, choices=YES_NO_CHOICES)
    true_caller_name = models.CharField(max_length=255)
    qr_availability = models.CharField(max_length=30, choices=QR_SIGNBOARD_CHOICES)
    qr_other_owner = models.CharField(max_length=255, blank=True, null=True)
    signboard_contact = models.CharField(max_length=30, choices=QR_SIGNBOARD_CHOICES)
    signboard_contact_other = models.CharField(max_length=255, blank=True, null=True)
    electricity_bill = models.CharField(max_length=5, choices=YES_NO_CHOICES)
    rent_agreement = models.CharField(max_length=5, choices=RENT_AGREEMENT_CHOICES)
    commercial_vehicle = models.CharField(max_length=5, choices=YES_NO_CHOICES)
    
    other_findings = models.TextField(blank=True, null=True)
    overall_status = models.CharField(max_length=20, choices=OVERALL_STATUS_CHOICES)
    status_remark = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Conclusion for {self.application.applicant_name} - {self.overall_status}"
