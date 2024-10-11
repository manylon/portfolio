from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def remove_exif(image_file):
    try:
        # Open the image and verify its validity
        with Image.open(image_file).convert('RGB') as image:

            # Correct orientation based on EXIF data
            image = ImageOps.exif_transpose(image)

            # Create a new image without EXIF metadata
            image_without_exif = Image.new(image.mode, image.size)
            image_without_exif.putdata(list(image.getdata()))

            # Save the image to a BytesIO object without EXIF data
            output = BytesIO()
            format_ = image.format if image.format else 'JPEG'  # Determine the format
            image_without_exif.save(output, format=format_)
            output.seek(0)  # Move the cursor to the beginning

            # Return a new InMemoryUploadedFile to replace the original one
            return InMemoryUploadedFile(
                output,
                'ImageField',
                image_file.name,
                format_,
                output.tell(),
                None
            )
    except Exception as e:
        raise ValueError(f"Error processing image file: {e}")


def create_thumbnail(image_field, thumbnail_field, size=(800, 800)):

    try:
        with Image.open(image_field).convert('RGB') as image:
            image = ImageOps.exif_transpose(image)
            image.thumbnail(size)
            image_file = BytesIO()
            format_ = image.format if image.format else 'JPEG'
            image.save(image_file, format=format_)
            image_file.seek(0)

            thumbnail_field.save(
                image_field.name,
                InMemoryUploadedFile(
                    image_file,
                    None,
                    image_field.name,
                    image_field.file.content_type,
                    image_file.tell(),
                    None
                ),
                save=False,
            )
    except Exception as e:
        raise ValueError(f"Error creating thumbnail: {e}")
