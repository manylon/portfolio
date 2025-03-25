import uuid

from blog.forms import BlogPostForm
from blog.utils import calculate_read_time
from core.blocks import CarouselBlock, CodeBlock, ExternalLinkBlock
from django.db import models
from django.utils.timezone import now
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, MultipleChooserPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail_headless_preview.models import HeadlessMixin


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPostPage", related_name="tagged_items", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Blog Post Tag"
        verbose_name_plural = "Blog Post Tags"


class BlogPostCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog Categories"


class BlogPostRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Role"
        verbose_name_plural = "Blog Roles"


class BlogPostPersonRelationship(Orderable, models.Model):
    blog_post = ParentalKey(
        "BlogPostPage",
        related_name="blog_post_person_relationship",
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        "core.Person",
        related_name="person_blog_post_relationship",
        on_delete=models.CASCADE,
    )
    role = models.ForeignKey(
        BlogPostRole, on_delete=models.SET_NULL, null=True, blank=True
    )
    panels = [FieldPanel("person"), FieldPanel("role")]


class BlogPostPage(HeadlessMixin, Page):
    excerpt = models.CharField(max_length=200)
    content = StreamField(
        [
            ("rich_text_block", RichTextBlock(label="Rich Text Block")),
            ("code_block", CodeBlock()),
            ("carousel_block", CarouselBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    category = models.ForeignKey(
        BlogPostCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)
    cover_image = models.ForeignKey(
        "core.CustomImage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    cover_image_alt = models.CharField(max_length=255, blank=True)
    external_link = StreamField(
        [
            ("external_link", ExternalLinkBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
        max_num=1,
    )
    read_time = models.PositiveIntegerField(default=0)
    date = models.DateField("Post date", default=now)

    content_panels = Page.content_panels + [
        FieldPanel("slug", help_text="The slug is the URL of the blog post"),
        FieldPanel("excerpt", help_text="A short description of the blog post"),
        FieldPanel("content", help_text="Add the content for the blog post"),
        MultiFieldPanel(
            [
                FieldPanel(
                    "cover_image", help_text="Upload an cover image for the blog post"
                ),
                FieldPanel(
                    "cover_image_alt",
                    help_text="Add an alternative text for the cover image",
                ),
            ],
            heading="Image",
        ),
        FieldPanel("date"),
        FieldPanel(
            "external_link", help_text="Link to the blog post on an external site"
        ),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        MultipleChooserPanel(
            "blog_post_person_relationship",
            chooser_field_name="person",
            heading="People who contributed to this blog post",
            label="Person",
            panels=[
                FieldPanel("person"),
                FieldPanel("role", help_text="Role of the person"),
            ],
        ),
        FieldPanel("category", help_text="Select a category for this blog post"),
        FieldPanel("tags", help_text="Add up to 3 tags for this blog post"),
    ]

    parent_page_types = ["BlogIndexPage"]

    subpage_types = []

    private_page_options = ["password"]

    base_form_class = BlogPostForm

    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("category"),
        index.RelatedFields(
            "tagged_items",
            [
                index.SearchField("tag"),
            ],
        ),
    ]

    def save(self, *args, **kwargs):
        if self.content:
            self.read_time = calculate_read_time(self.content)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ["-last_published_at"]


class BlogIndexPage(Page):
    subpage_types = ["BlogPostPage"]

    parent_page_types = ["wagtailcore.Page"]

    max_count = 1

    class Meta:
        verbose_name = "Blog Index Page"
        verbose_name_plural = "Blog Index Pages"
