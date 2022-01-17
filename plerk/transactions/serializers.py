#Django restframework
from dataclasses import field
from rest_framework import serializers
from .models import Company, Transaction


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        



class TransactionSerializer(serializers.ModelSerializer):
    company_id = CompanySerializer()
    class Meta:
        model = Transaction
        fields = '__all__'
        depth = 2

