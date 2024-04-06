from django.contrib import admin
from .models import Contact
from django.contrib.auth.models import User

# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    # accessibility and notes contain lengthy text, so ignorem them in the list view
    list_display = ('name', 'email', 'phone', 'preferred_contact', 'pronoun', 'tag_line')
    search_fields = ('name', 'email')

    def email(self, obj):
        return obj.user.email

admin.site.register(Contact, ContactAdmin)