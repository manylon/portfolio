import subprocess
from django.db import models
from wagtail.images.models import AbstractImage, AbstractRendition, Image

class CustomImage(AbstractImage):
    alt = models.CharField(
        max_length=255,
        blank=True,
        help_text="Alt text for the image if it is used in gallery",
    )

    admin_form_fields = Image.admin_form_fields + ("alt",)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file:
            try:
                # Remove all EXIF data from the image but keep the orientation
                # The source image is saved with a _original suffix
                # The new image is saved with the original name and path
                subprocess.run(
                    [
                        "exiftool",
                        "-all=",
                        "-tagsfromfile",
                        "@",
                        "-Orientation",
                        self.file.path,
                    ],
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                print(f"Error running exiftool: {e}")

    def delete(self, *args, **kwargs):
        if self.file:
            subprocess.run(["rm", f"{self.file.path}_original"], check=True)
        super().delete(*args, **kwargs)


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)

    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
    
