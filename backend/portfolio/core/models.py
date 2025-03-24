import subprocess

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, PublishingPanel
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.models import DraftStateMixin, RevisionMixin
from wagtail.search import index

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


class Person(DraftStateMixin, RevisionMixin, index.Indexed, ClusterableModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    nickname = models.CharField(blank=True, max_length=255)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    bio = models.TextField(blank=True)
    revisions = GenericRelation("wagtailcore.Revision", related_query_name="author")

    panels = [
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("nickname"),
        FieldPanel("email"),
        FieldPanel("bio"),
        PublishingPanel(),
    ]

    search_fields = [
        index.FilterField("full_name"),
        index.SearchField("full_name"),
        index.AutocompleteField("full_name"),
    ]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = "People"
        verbose_name = "Person"
        unique_together = ("first_name", "last_name")


class Organization(DraftStateMixin, RevisionMixin, index.Indexed, ClusterableModel):
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(null=True, blank=True, unique=True)
    revisions = GenericRelation(
        "wagtailcore.Revision", related_query_name="oranization"
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("website"),
        PublishingPanel(),
    ]

    search_fields = [
        index.FilterField("name"),
        index.SearchField("name"),
        index.AutocompleteField("name"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Organizations"
        verbose_name = "Organization"

    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
    
