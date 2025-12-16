from rest_framework import serializers 
from transaction.models import Transaction

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self,file):
        name = str(file.name).lower()
        if not name.endswith(".xlsx"):
            name = name.split(".")[-1]
            raise serializers.ValidationError(f"only .xlsx Excel files are allowed not this .{name}")
        return file


class Transaction_serializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = Transaction
        fields = '__all__'

        
class Transaction_View_serializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = Transaction
        fields = ["id","account_name","credit","debit","txn_date","description","payment_method"]
        read_only_fields = ["id"]       

