# from django.core.validators import FileExtensionValidator
#
# from rest_framework import serializers, status
# from easy_thumbnails.templatetags.thumbnail import thumbnail_url
#
# from fixplus.upload.validators import FileSizeValidator, ImageSizeValidator
#
#
# class InputParamsUploadSerializer(serializers.Serializer):
#     method = serializers.ChoiceField(
#         choices=['avatar',],
#     )
#
#
# class InputUploadSerializer(serializers.Serializer):
#     id = serializers.UUIDField(required=True)
#     image = serializers.ImageField(
#         validators=[
#             FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
#             FileSizeValidator(min_size=1, max_size=10 * 1024 * 1024),
#             ImageSizeValidator(max_height=4000, min_height=1, max_width=3000, min_width=1)
#         ],
#         required=True
#     )
#
#
# class OutPutUploadSerializer(serializers.Serializer):
#     id = serializers.UUIDField(required=True)
#     image = serializers.ImageField()
#     thumbnail_image = serializers.SerializerMethodField()
#
#     def get_thumbnail_image(self, obj):
#         # Use 'thumbnail_url' to get the relative URL of the thumbnail
#         thumbnail_relative_url = thumbnail_url(obj.image, 'large')
#
#         # Access the request from the context to build the absolute URL
#         request = self.context.get('request')
#         if request and thumbnail_relative_url:
#             # Build the absolute URI using the request object
#             return request.build_absolute_uri(thumbnail_relative_url)
#
#         # If request is not in context, return the relative URL (fallback)
#         return thumbnail_relative_url
#
#
