from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Item, Application, BusinessDetails, BusinessOwner, PersonMet,
    CoApplicant, OtherBusiness, Loan, BankAccount, SecurityDetails, Conclusion
)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


# ============ Application Form Serializers ============

class BusinessOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessOwner
        fields = ['id', 'name']
        read_only_fields = ['id']


class PersonMetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonMet
        fields = ['id', 'name', 'phone']
        read_only_fields = ['id']


class BusinessDetailsSerializer(serializers.ModelSerializer):
    owners = BusinessOwnerSerializer(many=True, required=False)
    persons_met = PersonMetSerializer(many=True, required=False)
    
    class Meta:
        model = BusinessDetails
        fields = [
            'id', 'business_name', 'ownership_type', 'business_address', 'visit_address',
            'gst_number', 'business_location', 'gps_location', 'shop_ownership', 'rent_amount',
            'business_relates_to', 'business_since_year', 'turnover', 'net_income',
            'stock_value', 'txn_type', 'staff_count', 'monthly_salary',
            'creditors_payment_time', 'debtors_payment_time', 'payment_modes',
            'purchase_area', 'sale_area', 'owners', 'persons_met'
        ]
        read_only_fields = ['id']


class CoApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoApplicant
        fields = [
            'id', 'involvement_type', 'business_name', 'business_address', 'registered_name',
            'business_relates_to', 'business_since_year', 'turnover', 'net_income',
            'stock_value', 'txn_type', 'staff_count', 'monthly_salary',
            'employer_name', 'position', 'yearly_salary', 'duration', 'other_details'
        ]
        read_only_fields = ['id']


class OtherBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherBusiness
        fields = [
            'id', 'business_name', 'owner_name', 'address', 'relationship',
            'yearly_income', 'vintage_year', 'remarks'
        ]
        read_only_fields = ['id']


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'loan_type', 'bank_name', 'loan_amount', 'emi']
        read_only_fields = ['id']


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['id', 'bank_name', 'branch', 'account_type', 'cc_limit']
        read_only_fields = ['id']


class SecurityDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityDetails
        fields = [
            'id', 'house_address', 'house_area', 'house_market_value',
            'house_ownership', 'other_house_owner', 'amount_required',
            'end_use', 'other_end_use'
        ]
        read_only_fields = ['id']


class ConclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conclusion
        fields = [
            'id', 'general_observation', 'nearby_person1', 'nearby_person2',
            'sale_invoices', 'purchase_invoices', 'business_setup', 'stock_pictures',
            'signboard', 'biz_registration', 'education_proof', 'true_caller_name',
            'qr_availability', 'qr_other_owner', 'signboard_contact', 'signboard_contact_other',
            'electricity_bill', 'rent_agreement', 'commercial_vehicle',
            'other_findings', 'overall_status', 'status_remark'
        ]
        read_only_fields = ['id']


class ApplicationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing applications"""
    agent_name = serializers.CharField(source='agent.username', read_only=True)
    overall_status = serializers.CharField(source='conclusion.overall_status', read_only=True, default=None)
    
    class Meta:
        model = Application
        fields = [
            'id', 'applicant_name', 'file_no', 'telephone', 'allocation_date',
            'visit_date', 'agent_name', 'overall_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ApplicationDetailSerializer(serializers.ModelSerializer):
    """Full serializer for viewing/creating applications with all nested data"""
    business_details = BusinessDetailsSerializer(required=False)
    co_applicant = CoApplicantSerializer(required=False, allow_null=True)
    other_businesses = OtherBusinessSerializer(many=True, required=False)
    loans = LoanSerializer(many=True, required=False)
    bank_accounts = BankAccountSerializer(many=True, required=False)
    security_details = SecurityDetailsSerializer(required=False)
    conclusion = ConclusionSerializer(required=False)
    agent_name = serializers.CharField(source='agent.username', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'agent', 'agent_name', 'applicant_name', 'gender', 'file_no',
            'allocation_date', 'visit_date', 'dob', 'age', 'qualification',
            'other_qualification', 'prof_qualification', 'other_prof_qualification',
            'telephone', 'tel_owner', 'other_tel_owner', 'residential_address',
            'family_members', 'business_details', 'co_applicant', 'other_businesses',
            'loans', 'bank_accounts', 'security_details', 'conclusion',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'agent', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Extract nested data
        business_details_data = validated_data.pop('business_details', None)
        co_applicant_data = validated_data.pop('co_applicant', None)
        other_businesses_data = validated_data.pop('other_businesses', [])
        loans_data = validated_data.pop('loans', [])
        bank_accounts_data = validated_data.pop('bank_accounts', [])
        security_details_data = validated_data.pop('security_details', None)
        conclusion_data = validated_data.pop('conclusion', None)
        
        # Set agent from request
        validated_data['agent'] = self.context['request'].user
        
        # Create main application
        application = Application.objects.create(**validated_data)
        
        # Create business details with owners and persons met
        if business_details_data:
            owners_data = business_details_data.pop('owners', [])
            persons_met_data = business_details_data.pop('persons_met', [])
            
            business = BusinessDetails.objects.create(
                application=application, **business_details_data
            )
            
            for owner_data in owners_data:
                BusinessOwner.objects.create(business=business, **owner_data)
            
            for person_data in persons_met_data:
                PersonMet.objects.create(business=business, **person_data)
        
        # Create co-applicant if provided
        if co_applicant_data:
            CoApplicant.objects.create(application=application, **co_applicant_data)
        
        # Create other businesses
        for business_data in other_businesses_data:
            OtherBusiness.objects.create(application=application, **business_data)
        
        # Create loans
        for loan_data in loans_data:
            Loan.objects.create(application=application, **loan_data)
        
        # Create bank accounts
        for account_data in bank_accounts_data:
            BankAccount.objects.create(application=application, **account_data)
        
        # Create security details
        if security_details_data:
            SecurityDetails.objects.create(application=application, **security_details_data)
        
        # Create conclusion
        if conclusion_data:
            Conclusion.objects.create(application=application, **conclusion_data)
        
        return application
    
    def update(self, instance, validated_data):
        # Extract nested data
        business_details_data = validated_data.pop('business_details', None)
        co_applicant_data = validated_data.pop('co_applicant', None)
        other_businesses_data = validated_data.pop('other_businesses', None)
        loans_data = validated_data.pop('loans', None)
        bank_accounts_data = validated_data.pop('bank_accounts', None)
        security_details_data = validated_data.pop('security_details', None)
        conclusion_data = validated_data.pop('conclusion', None)
        
        # Update main application fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update business details
        if business_details_data is not None:
            owners_data = business_details_data.pop('owners', None)
            persons_met_data = business_details_data.pop('persons_met', None)
            
            business, created = BusinessDetails.objects.update_or_create(
                application=instance, defaults=business_details_data
            )
            
            if owners_data is not None:
                business.owners.all().delete()
                for owner_data in owners_data:
                    BusinessOwner.objects.create(business=business, **owner_data)
            
            if persons_met_data is not None:
                business.persons_met.all().delete()
                for person_data in persons_met_data:
                    PersonMet.objects.create(business=business, **person_data)
        
        # Update co-applicant
        if co_applicant_data is not None:
            if co_applicant_data:
                CoApplicant.objects.update_or_create(
                    application=instance, defaults=co_applicant_data
                )
            else:
                CoApplicant.objects.filter(application=instance).delete()
        
        # Update other businesses
        if other_businesses_data is not None:
            instance.other_businesses.all().delete()
            for business_data in other_businesses_data:
                OtherBusiness.objects.create(application=instance, **business_data)
        
        # Update loans
        if loans_data is not None:
            instance.loans.all().delete()
            for loan_data in loans_data:
                Loan.objects.create(application=instance, **loan_data)
        
        # Update bank accounts
        if bank_accounts_data is not None:
            instance.bank_accounts.all().delete()
            for account_data in bank_accounts_data:
                BankAccount.objects.create(application=instance, **account_data)
        
        # Update security details
        if security_details_data is not None:
            SecurityDetails.objects.update_or_create(
                application=instance, defaults=security_details_data
            )
        
        # Update conclusion
        if conclusion_data is not None:
            Conclusion.objects.update_or_create(
                application=instance, defaults=conclusion_data
            )
        
        return instance


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user authentication"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']
