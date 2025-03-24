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
