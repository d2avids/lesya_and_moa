from rest_framework import serializers

from users.models import Child, ChildrenGroup, Region, User


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
        )


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class ChildSerializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())
    user = UserSerializer(read_only=True)

    class Meta:
        model = Child
        fields = (
            'id',
            'user',
            'first_name',
            'last_name',
            'sex',
            'age',
            'region',
            'school',
            'grade',
            'attended_speech_therapist',
            'data_processing_agreement',
        )

    def to_representation(self, instance):
        self.fields['region'] = RegionSerializer(read_only=True)
        return super().to_representation(instance)


class ChildrenGroupSerializer(serializers.ModelSerializer):
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())
    user = UserSerializer(read_only=True)

    class Meta:
        model = ChildrenGroup
        fields = (
            'id',
            'user',
            'name',
            'number_of_students',
            'average_age',
            'region',
            'school',
        )

    def to_representation(self, instance):
        self.fields['region'] = RegionSerializer(read_only=True)
        return super().to_representation(instance)


class ShortChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = (
            'id',
            'first_name',
            'last_name',
            'sex',
            'age',
        )


class ShortChildrenGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildrenGroup
        fields = (
            'id',
            'name',
            'number_of_students',
            'average_age',
        )
