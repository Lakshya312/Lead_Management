import logging
from django.contrib import admin, messages
from django.db.models import ProtectedError
from .models import (
    Region, ProductCategory, LeadSource, LeadStatus,
    Territory, Product, Lead, LeadFollowUp
)

# ---------------------------------------------------------------------------
# Module-level logger — admin errors flow to logs/errors.log
# ---------------------------------------------------------------------------
logger = logging.getLogger('leads')


# ---------------------------------------------------------------------------
# Mixin: overrides delete_model to catch ProtectedError in the admin panel
# instead of raising an unhandled 500 error page.
# ---------------------------------------------------------------------------
class ProtectedDeleteMixin:
    """
    ✅ NEW — Admin mixin that catches django.db.models.ProtectedError when
    a staff user tries to delete a record that is still referenced by child
    records (on_delete=PROTECT FK).

    Without this mixin, Django Admin raises an unhandled 500 error page.
    With this mixin, the admin shows a clear error message banner instead.
    """

    def delete_model(self, request, obj):
        """Single-object deletion from the admin change page."""
        try:
            obj.delete()
            logger.info(
                "Admin delete_model: %s '%s' (pk=%s) deleted by user '%s'.",
                obj.__class__.__name__, str(obj), obj.pk, request.user.username,
            )
        except ProtectedError as exc:
            logger.warning(
                "Admin delete_model: ProtectedError — %s '%s' (pk=%s) is "
                "referenced by child records. Delete blocked by user '%s'. Detail: %s",
                obj.__class__.__name__, str(obj), obj.pk,
                request.user.username, exc,
            )
            self.message_user(
                request,
                f'Cannot delete "{obj}" because it is still referenced by related records. '
                f'Please remove all dependent records first.',
                level=messages.ERROR,
            )
        except Exception as exc:
            logger.error(
                "Admin delete_model: Unexpected error deleting %s pk=%s — %s",
                obj.__class__.__name__, obj.pk, exc, exc_info=True,
            )
            self.message_user(
                request,
                f'An unexpected error occurred while deleting "{obj}". '
                f'Check server logs for details.',
                level=messages.ERROR,
            )

    def delete_queryset(self, request, queryset):
        """Bulk deletion from the admin list page (action: 'Delete selected')."""
        deleted_count = 0
        blocked_count = 0
        for obj in queryset:
            try:
                obj.delete()
                deleted_count += 1
                logger.info(
                    "Admin delete_queryset: %s '%s' (pk=%s) deleted by user '%s'.",
                    obj.__class__.__name__, str(obj), obj.pk, request.user.username,
                )
            except ProtectedError:
                blocked_count += 1
                logger.warning(
                    "Admin delete_queryset: ProtectedError — %s '%s' (pk=%s) "
                    "is referenced by child records. Skipped.",
                    obj.__class__.__name__, str(obj), obj.pk,
                )
            except Exception as exc:
                blocked_count += 1
                logger.error(
                    "Admin delete_queryset: Unexpected error on %s pk=%s — %s",
                    obj.__class__.__name__, obj.pk, exc, exc_info=True,
                )

        if deleted_count:
            self.message_user(
                request,
                f'Successfully deleted {deleted_count} record(s).',
                level=messages.SUCCESS,
            )
        if blocked_count:
            self.message_user(
                request,
                f'{blocked_count} record(s) could not be deleted because they are '
                f'still referenced by other records. Remove dependent records first.',
                level=messages.ERROR,
            )


# ---------------------------------------------------------------------------
# Admin registrations — all use ProtectedDeleteMixin
# ---------------------------------------------------------------------------

@admin.register(Region)
class RegionAdmin(ProtectedDeleteMixin, admin.ModelAdmin):
    list_display = ('regionid', 'regionname', 'added_by', 'added_dts')
    search_fields = ('regionname',)


@admin.register(ProductCategory)
class ProductCategoryAdmin(ProtectedDeleteMixin, admin.ModelAdmin):
    list_display = ('categoryid', 'categoryname', 'added_by', 'added_dts')
    search_fields = ('categoryname',)


@admin.register(LeadSource)
class LeadSourceAdmin(ProtectedDeleteMixin, admin.ModelAdmin):
    list_display = ('leadsourceid', 'leadsourcename', 'added_by', 'added_dts')
    search_fields = ('leadsourcename',)


@admin.register(LeadStatus)
class LeadStatusAdmin(ProtectedDeleteMixin, admin.ModelAdmin):
    list_display = ('statusid', 'statusname', 'added_by', 'added_dts')
    search_fields = ('statusname',)


@admin.register(Territory)
class TerritoryAdmin(ProtectedDeleteMixin, admin.ModelAdmin):
    list_display = ('territoryid', 'territoryname', 'regionid', 'added_by', 'added_dts')
    search_fields = ('territoryname',)
    list_filter = ('regionid',)


@admin.register(Product)
class ProductAdmin(ProtectedDeleteMixin, admin.ModelAdmin):
    list_display = ('productid', 'productname', 'categoryid', 'is_active', 'added_by', 'added_dts')
    search_fields = ('productname',)
    list_filter = ('categoryid', 'is_active')


@admin.register(Lead)
class LeadAdmin(ProtectedDeleteMixin, admin.ModelAdmin):
    list_display = ('leadid', 'personname', 'companyname', 'contactno', 'city', 'state', 'lead_gen_date', 'added_dts')
    list_filter = ('regionid', 'statusid', 'leadsourceid')
    search_fields = ('personname', 'companyname', 'contactno', 'email')


@admin.register(LeadFollowUp)
class LeadFollowUpAdmin(ProtectedDeleteMixin, admin.ModelAdmin):
    list_display = ('followupid', 'leadid', 'actiontaken', 'leadstatusid', 'followupdate', 'executive_name')
    list_filter = ('leadstatusid', 'followupdate')
    search_fields = ('actiontaken', 'executive_name')