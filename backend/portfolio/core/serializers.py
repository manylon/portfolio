from django.utils.crypto import constant_time_compare
from rest_framework import serializers


# Use for the ExternalLinkBlock in the core.blocks module.
class ExternalLinkBlockSerializer(serializers.Serializer):
    source_name = serializers.CharField()
    url = serializers.URLField()


# Use for the CarouselBlock in the core.blocks module.
class CarouselBlockSerializer(serializers.Serializer):
    title = serializers.CharField()
    images = serializers.SerializerMethodField()

    def to_representation(self, instance):
        self.rendition_filter = self.context.get("rendition_filter", "max-1050x1050")
        return super().to_representation(instance)

    def get_images(self, obj) -> list:
        images = []
        for image_data in obj["images"]:
            image = image_data["image"]
            rendition = image.get_rendition(self.rendition_filter)
            images.append(
                {
                    "url": rendition.url,
                    "alt": image_data.get("alt_text", ""),
                    "caption": image_data.get("caption", ""),
                }
            )
        return images

class PasswordRestrictionSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        self.restriction = kwargs.pop("restriction", None)
        super().__init__(*args, **kwargs)

    def validate_password(self, value):
        if not self.restriction:
            raise serializers.ValidationError("No restriction instance provided.")
        if not constant_time_compare(value, self.restriction.password):
            raise serializers.ValidationError(
                "The password you have entered is not correct."
            )
        return value


class PasswordFormSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
