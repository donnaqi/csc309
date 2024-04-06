from rest_framework.serializers import ModelSerializer
from .models import Contact

class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        #fields = '__all__'
        fields = ['user', 'name', 'email', 'phone', 'preferred_contact', 'pronoun', 'tag_line', 'accessibility', 'notes']
        read_only_fields = ('user', 'email')