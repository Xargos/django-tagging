"""
Convenience module for access of custom tagging application settings,
which enforces default settings when the main settings module does not
contain the appropriate settings.
"""
from django.conf import settings

# The maximum length of a tag's name.
MAX_TAG_LENGTH = getattr(settings, 'MAX_TAG_LENGTH', 50)

# Whether to force all tags to lowercase before they are saved to the
# database.
FORCE_LOWERCASE_TAGS = getattr(settings, 'FORCE_LOWERCASE_TAGS', False)

# Maximum allowed number of tags per object
MAX_TAGS_PER_OBJECTS = getattr(settings, 'MAX_TAGS_PER_OBJECTS', 5)

# Determine if there is a limit on the number of allowed tags per objects
MAX_TAGS_PER_OBJECTS_ENABLED = getattr(settings, 'MAX_TAGS_PER_OBJECTS_ENABLED', False)