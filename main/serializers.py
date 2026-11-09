from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Education


class EducationSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = (
            "id",
            "school",
            "start_year",
            "end_year",
            "curriculum",
            "description",
            "star_count",
            "is_starred",
            "starred_by_names",
        )
        read_only_fields = (
            "id",
            "star_count",
            "is_starred",
            "starred_by_names",
        )

    def validate_school(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Nama sekolah tidak boleh kosong.")
        return value

    def validate_curriculum(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Kurikulum tidak boleh kosong.")
        return value

    def validate_description(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Deskripsi tidak boleh kosong.")
        return value

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        return bool(request and request.user.is_authenticated and
                    request.user in obj.starred_by.all())

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())
