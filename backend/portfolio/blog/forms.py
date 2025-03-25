from core.admin_validations import validate_tags
from wagtail.admin.forms import WagtailAdminPageForm


class BlogPostForm(WagtailAdminPageForm):
    def clean(self):
        """Validate the number of tags."""
        cleaned_data = super().clean()
        tags = cleaned_data.get("tags", [])

        try:
            validate_tags(tags)
        except ValueError as e:
            self.add_error("tags", str(e))

        return cleaned_data
