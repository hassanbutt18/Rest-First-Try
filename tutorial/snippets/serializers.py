from rest_framework import serializers
from .models import User, Profile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.CharField(style={'input_type': 'email'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'password2', 'tc']

    def validate_name(self, name):
        print("This is the name we are getting ", name)
        print("and its type ", type(name))
        # name = int(name)
        # print("Name is converted into the integer",type(name))
        if name == '123':
            raise serializers.ValidationError("Name cannot be empty")
        return name

    def validate_tc(self, tc):
        if tc == False:
            raise serializers.ValidationError("Terms and Condition field cannot be False")
        return tc

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email already exists.")
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password is not matched kindly correct your password")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    # If I am not using this email field the system say the user with this email already exists
    # password = serializers.CharField(style={'input_type': 'password'}, write_only=True) WHY It's NT GIVING ACCESS?

    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs


class Dashboard(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        use_url=True
    )

    class Meta:
        model = Profile
        fields = ['image', 'nick_name', 'work_description', 'Family_detail']


class DashboardEdit(serializers.ModelSerializer):
    # nick_name = serializers.CharField(required=False)
    # work_description = serializers.CharField(required=False)
    # Family_detail = serializers.CharField(required=False)
    image = serializers.ImageField(max_length=None, use_url=True, required=True)

    class Meta:
        model = Profile
        fields = ['image', 'nick_name', 'work_description', 'Family_detail']


class DashboardRead(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'get_image', 'image', 'work_description', 'Family_detail']
        read_only_fields = ['nick_name', 'work_description', 'Family_detail']


class DashboardFilter(serializers.ModelSerializer):
    work_description = serializers.CharField(required=False)
    Family_detail = serializers.CharField(required=False)

    class Meta:
        model = Profile
        fields = ['nick_name', 'work_description', 'Family_detail']


class DashboardSearch(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['__all__']


class Search(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['nick_name', 'work_description', 'Family_detail']


class Imagee(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        use_url=True
    )

    class Meta:
        model = Profile
        fields = ['image', 'nick_name', 'work_description', 'Family_detail']
