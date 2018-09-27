from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from ..models import Period

__all__ = ('PeriodAdmin',)


class PeriodAdmin(MPTTModelAdmin):
    """Translation admin."""

    mptt_level_indent = 20
    list_display = (
        'name_en',
        'name_nl',
        'date_range',
    )
    search_fields = (
        'name_nl',
        'name_en'
    )
    fields = (
        'name_en',
        'name_nl',
        'parent_tree',
    )
    readonly_fields = ('parent_tree',)

    def parent_tree(self, obj):
        """Read only semantic representation of the parent.

        :param obj:
        :return:
        :rtype: str
        """
        return " > ".join([el.name_en for el in obj.get_ancestors()])


admin.site.register(Period, PeriodAdmin)

