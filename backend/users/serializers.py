from rest_framework import serializers

from users.models import User

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)