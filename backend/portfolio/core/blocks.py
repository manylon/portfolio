from wagtail import blocks
from wagtail.blocks import CharBlock, ChoiceBlock, ListBlock, StructBlock, TextBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class ExternalLinkBlock(blocks.StructBlock):
    source_name = blocks.CharBlock(
        required=True, max_length=50, help_text="Name"
    )
    url = blocks.URLBlock(required=True, help_text="External URL")

    class Meta:
        label = "External Media Link"


class CarouselBlock(StructBlock):
    title = CharBlock(required=False, label="Carousel Title")

    images = ListBlock(
        StructBlock(
            [
                ("image", ImageChooserBlock(label="Image")),
                ("alt_text", CharBlock(required=False, label="Alternative Text")),
                ("caption", CharBlock(required=False, label="Caption")),
            ]
        ),
        label="Carousel Images",
    )

    class Meta:
        icon = "image"
        label = "Carousel Block"


class CodeBlock(StructBlock):
    language = ChoiceBlock(
        choices=[
            ("bash", "Bash/Shell"),
            ("css", "CSS"),
            ("html", "HTML"),
            ("javascript", "Javascript"),
            ("typescript", "Typescript"),
            ("json", "JSON"),
            ("python", "Python"),
            ("yaml", "YAML"),
            ("docker", "Docker"),
            ("sql", "SQL"),
        ],
        label="Language",
    )

    code = TextBlock(label="Code")

    class Meta:
        icon = "code"
        label = "Code Block"
