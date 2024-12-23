from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"

    def validate_username(self, value):
        if (
            Account.objects.filter(username=value).exists()
            or Account.objects.filter(email=value).exists()
        ):
            raise serializers.ValidationError(
                "This username(email) already taken by another user."
            )

        return value

    def validate_email(self, value):
        if (
            Account.objects.filter(username=value).exists()
            or Account.objects.filter(email=value).exists()
        ):
            raise serializers.ValidationError(
                "This email already taken by another user."
            )

        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class AccountDeleteSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["password"]

    def save(self, **kwargs):
        user = self.context.get("user")
        password = self.validated_data["password"]
        user.set_password(password)  # 비밀번호 해싱 및 저장
        user.save()
        return user


class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "email",
            "name",
            "nickname",
            "birth_date",
            "bio",
            "gender",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "name": {"required": True},
            "nickname": {"required": True},
            "birth_date": {"required": True},
            "bio": {"required": False},
            "gender": {"required": False},
        }

    def validate_email(self, value):
        user = self.context.get("user")
        email = user.email
        if value != email:
            if (
                Account.objects.exclude(id=user.id).filter(username=value).exists()
                or Account.objects.filter(email=value).exists()
            ):
                raise serializers.ValidationError(
                    "This email already taken by another user."
                )

        return value
