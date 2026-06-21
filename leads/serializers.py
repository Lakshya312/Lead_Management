"""
Django REST Framework serializers for the leads app.

Provides serialization, deserialization, and validation for all models:
Region, ProductCategory, LeadSource, LeadStatus, Territory, Product, Lead, LeadFollowUp.

Exception handling strategy:
  - Field-level validators (validate_<field>) → HTTP 400 ValidationError before DB hit
  - create()/update() IntegrityError catch → HTTP 400 safety net for race conditions
  - ProtectedError on delete handled in views.py (HTTP 409)
  - All exceptions are logged to logs/errors.log via the 'leads' logger
"""
import re
import logging
from datetime import datetime
from django.db import IntegrityError
from rest_framework import serializers
from .models import (
    Region, ProductCategory, LeadSource, LeadStatus,
    Territory, Product, Lead, LeadFollowUp,
)

# ---------------------------------------------------------------------------
# Module-level logger — messages flow to logs/errors.log & logs/general.log
# ---------------------------------------------------------------------------
logger = logging.getLogger('leads')


# ---------------------------------------------------------------------------
# Helper mixin — shared _get_added_by logic & IntegrityError safety net
# ---------------------------------------------------------------------------

class AuditMixin:
    """
    Mixin that provides:
      - _get_added_by()  : resolves the logged-in user name for audit columns.
      - _safe_create()   : wraps super().create() and converts IntegrityError
                           (e.g. race-condition duplicate) into HTTP 400.
      - _safe_update()   : wraps super().update() with the same protection.
    """

    def _get_added_by(self):
        """Return the name of the authenticated user making the API request."""
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return request.user.get_full_name() or request.user.username
        return 'API'

    def _safe_create(self, validated_data):
        """Call super().create() and convert IntegrityError → HTTP 400."""
        try:
            return super().create(validated_data)
        except IntegrityError as exc:
            # ✅ LOG: Race-condition duplicate insert at DB level
            logger.error(
                "%s._safe_create: IntegrityError — duplicate record attempt. Data=%s — %s",
                self.__class__.__name__, list(validated_data.keys()), exc, exc_info=True,
            )
            raise serializers.ValidationError(
                {"detail": f"A record with the same unique value already exists. ({exc})"}
            )

    def _safe_update(self, instance, validated_data):
        """Call super().update() and convert IntegrityError → HTTP 400."""
        try:
            return super().update(instance, validated_data)
        except IntegrityError as exc:
            # ✅ LOG: Race-condition duplicate update at DB level
            logger.error(
                "%s._safe_update: IntegrityError — duplicate record on update pk=%s. — %s",
                self.__class__.__name__, getattr(instance, 'pk', None), exc, exc_info=True,
            )
            raise serializers.ValidationError(
                {"detail": f"A record with the same unique value already exists. ({exc})"}
            )


# ---------------------------------------------------------------------------
# Region
# ---------------------------------------------------------------------------

class RegionSerializer(AuditMixin, serializers.ModelSerializer):
    """Serializer for Region master data."""

    class Meta:
        model = Region
        fields = ['regionid', 'regionname', 'added_by', 'added_dts']
        read_only_fields = ['regionid', 'added_dts']

    def validate_regionname(self, value):
        """
        Reject blank/whitespace-only region names.
        Also enforce uniqueness at the serializer level (before DB hit).
        """
        name = value.strip() if value else ''
        if not name:
            raise serializers.ValidationError("Region name is required and cannot be blank.")
        # Uniqueness check (exclude current instance on update)
        qs = Region.objects.filter(regionname__iexact=name)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                f'A region named "{name}" already exists. Please use a different name.'
            )
        return value

    def create(self, validated_data):
        validated_data['added_dts'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        validated_data.setdefault('added_by', self._get_added_by())
        return self._safe_create(validated_data)

    def update(self, instance, validated_data):
        return self._safe_update(instance, validated_data)


# ---------------------------------------------------------------------------
# ProductCategory
# ---------------------------------------------------------------------------

class ProductCategorySerializer(AuditMixin, serializers.ModelSerializer):
    """Serializer for ProductCategory master data."""

    class Meta:
        model = ProductCategory
        fields = ['categoryid', 'categoryname', 'added_by', 'added_dts']
        read_only_fields = ['categoryid', 'added_dts']

    def validate_categoryname(self, value):
        """Reject blank names and enforce case-insensitive uniqueness."""
        name = value.strip() if value else ''
        if not name:
            raise serializers.ValidationError("Category name is required and cannot be blank.")
        qs = ProductCategory.objects.filter(categoryname__iexact=name)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                f'A category named "{name}" already exists. Please use a different name.'
            )
        return value

    def create(self, validated_data):
        validated_data['added_dts'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        validated_data.setdefault('added_by', self._get_added_by())
        return self._safe_create(validated_data)

    def update(self, instance, validated_data):
        return self._safe_update(instance, validated_data)


# ---------------------------------------------------------------------------
# LeadSource
# ---------------------------------------------------------------------------

class LeadSourceSerializer(AuditMixin, serializers.ModelSerializer):
    """Serializer for LeadSource master data."""

    class Meta:
        model = LeadSource
        fields = ['leadsourceid', 'leadsourcename', 'added_by', 'added_dts']
        read_only_fields = ['leadsourceid', 'added_dts']

    def validate_leadsourcename(self, value):
        """Reject blank names and enforce case-insensitive uniqueness."""
        name = value.strip() if value else ''
        if not name:
            raise serializers.ValidationError("Lead source name is required and cannot be blank.")
        qs = LeadSource.objects.filter(leadsourcename__iexact=name)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                f'A lead source named "{name}" already exists. Please use a different name.'
            )
        return value

    def create(self, validated_data):
        validated_data['added_dts'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        validated_data.setdefault('added_by', self._get_added_by())
        return self._safe_create(validated_data)

    def update(self, instance, validated_data):
        return self._safe_update(instance, validated_data)


# ---------------------------------------------------------------------------
# LeadStatus
# ---------------------------------------------------------------------------

class LeadStatusSerializer(AuditMixin, serializers.ModelSerializer):
    """Serializer for LeadStatus master data."""

    class Meta:
        model = LeadStatus
        fields = ['statusid', 'statusname', 'added_by', 'added_dts']
        read_only_fields = ['statusid', 'added_dts']

    def validate_statusname(self, value):
        """Reject blank names and enforce case-insensitive uniqueness."""
        name = value.strip() if value else ''
        if not name:
            raise serializers.ValidationError("Status name is required and cannot be blank.")
        qs = LeadStatus.objects.filter(statusname__iexact=name)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                f'A lead status named "{name}" already exists. Please use a different name.'
            )
        return value

    def create(self, validated_data):
        validated_data['added_dts'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        validated_data.setdefault('added_by', self._get_added_by())
        return self._safe_create(validated_data)

    def update(self, instance, validated_data):
        return self._safe_update(instance, validated_data)


# ---------------------------------------------------------------------------
# Territory
# ---------------------------------------------------------------------------

class TerritorySerializer(AuditMixin, serializers.ModelSerializer):
    """Serializer for Territory master data with nested region detail on read."""
    region_detail = RegionSerializer(source='regionid', read_only=True)

    class Meta:
        model = Territory
        fields = [
            'territoryid', 'territoryname', 'regionid',
            'region_detail', 'added_by', 'added_dts',
        ]
        read_only_fields = ['territoryid', 'added_dts']

    def validate_territoryname(self, value):
        """Reject blank territory names."""
        name = value.strip() if value else ''
        if not name:
            raise serializers.ValidationError("Territory name is required and cannot be blank.")
        return value

    def validate_regionid(self, value):
        """Ensure the referenced Region actually exists."""
        if value is None:
            raise serializers.ValidationError("A valid Region must be selected.")
        return value

    def create(self, validated_data):
        validated_data['added_dts'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        validated_data.setdefault('added_by', self._get_added_by())
        return self._safe_create(validated_data)

    def update(self, instance, validated_data):
        return self._safe_update(instance, validated_data)


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------

class ProductSerializer(AuditMixin, serializers.ModelSerializer):
    """Serializer for Product master data with nested category detail on read."""
    category_detail = ProductCategorySerializer(source='categoryid', read_only=True)

    class Meta:
        model = Product
        fields = [
            'productid', 'productname', 'categoryid',
            'category_detail', 'is_active', 'added_by', 'added_dts',
        ]
        read_only_fields = ['productid', 'added_dts']

    def validate_productname(self, value):
        """
        Reject product names that are:
          - blank / whitespace-only
          - purely numeric (e.g. '1234', '007')
        Alphanumeric names like 'Product2', '3M Tape', 'A1B2' are accepted.
        """
        name = value.strip() if value else ''
        if not name:
            raise serializers.ValidationError("Product name is required.")
        if name.replace(' ', '').isdigit():
            raise serializers.ValidationError(
                "Product name cannot be purely numeric. "
                "Please include at least one letter (e.g. 'Product 101' or '3M Cable')."
            )
        return value

    def validate_is_active(self, value):
        """Ensure is_active is only 0 or 1."""
        if value not in (0, 1):
            raise serializers.ValidationError("Status must be 1 (Active) or 0 (Inactive).")
        return value

    def create(self, validated_data):
        validated_data['added_dts'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        validated_data.setdefault('added_by', self._get_added_by())
        return self._safe_create(validated_data)

    def update(self, instance, validated_data):
        return self._safe_update(instance, validated_data)


# ---------------------------------------------------------------------------
# Lead
# ---------------------------------------------------------------------------

class LeadSerializer(AuditMixin, serializers.ModelSerializer):
    """
    Serializer for the core Lead model.
    Provides nested read-only representations for all foreign key relationships
    and validates all key fields before any DB operation.
    """
    territory_detail = TerritorySerializer(source='territoryid', read_only=True)
    region_detail = RegionSerializer(source='regionid', read_only=True)
    product_detail = ProductSerializer(source='productid', read_only=True)
    status_detail = LeadStatusSerializer(source='statusid', read_only=True)
    source_detail = LeadSourceSerializer(source='leadsourceid', read_only=True)

    class Meta:
        model = Lead
        fields = [
            'leadid', 'personname', 'gender', 'companyname',
            'contactno', 'email', 'city', 'state',
            'territoryid', 'territory_detail',
            'regionid', 'region_detail',
            'productid', 'product_detail',
            'statusid', 'status_detail',
            'leadsourceid', 'source_detail',
            'businessneed', 'lead_gen_date', 'executiveid',
            'added_by', 'added_dts',
        ]
        read_only_fields = ['leadid', 'added_dts']

    def validate_personname(self, value):
        """Person name must not be blank."""
        name = value.strip() if value else ''
        if not name:
            raise serializers.ValidationError("Person name is required and cannot be blank.")
        return value

    def validate_email(self, value):
        """
        ✅ IMPROVED — uses a proper RFC-5322 regex instead of a weak '@' string check.
        Rejects: 'a@b', '@.com', 'noatsign', 'missing@dot'
        Accepts: 'name@domain.com', 'user.name+tag@sub.domain.org'
        """
        if value:
            value = value.strip()
            # Proper email regex pattern
            email_regex = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, value):
                logger.warning(
                    "LeadSerializer.validate_email: Invalid email format submitted — '%s'",
                    value,
                )
                raise serializers.ValidationError(
                    "Please provide a valid email address (e.g. name@domain.com)."
                )
        return value

    def validate_contactno(self, value):
        """Validate contact number contains only digits, spaces, +, and -."""
        if value:
            cleaned = value.replace(' ', '').replace('-', '').replace('+', '')
            if not cleaned.isdigit():
                raise serializers.ValidationError(
                    "Contact number should contain only digits, spaces, + and -."
                )
            if len(cleaned) < 7 or len(cleaned) > 15:
                raise serializers.ValidationError(
                    "Contact number must be between 7 and 15 digits."
                )
        return value

    def validate_executiveid(self, value):
        """Executive ID must be a positive integer."""
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Executive ID must be a positive integer (greater than 0)."
            )
        return value

    def validate(self, data):
        """
        Cross-field validation:
          - Check for duplicate email or contact number (exclude current instance on update).
        """
        email = data.get('email')
        contactno = data.get('contactno')

        if email or contactno:
            from django.db.models import Q
            query = Q()
            if email:
                query |= Q(email=email)
            if contactno:
                query |= Q(contactno=contactno)

            qs = Lead.objects.filter(query)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"detail": "A lead with this Email or Contact Number already exists."}
                )
        return data

    def create(self, validated_data):
        validated_data['added_dts'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        validated_data.setdefault('added_by', self._get_added_by())
        return self._safe_create(validated_data)

    def update(self, instance, validated_data):
        return self._safe_update(instance, validated_data)


# ---------------------------------------------------------------------------
# LeadFollowUp
# ---------------------------------------------------------------------------

class LeadFollowUpSerializer(AuditMixin, serializers.ModelSerializer):
    """
    Serializer for the LeadFollowUp history model.
    Includes nested lead and status details on read.
    """
    lead_detail = LeadSerializer(source='leadid', read_only=True)
    status_detail = LeadStatusSerializer(source='leadstatusid', read_only=True)

    class Meta:
        model = LeadFollowUp
        fields = [
            'followupid', 'leadid', 'lead_detail',
            'executiveid', 'actiontaken', 'remarks',
            'leadstatusid', 'status_detail',
            'followupdate', 'executive_name',
            'added_by', 'added_dts',
        ]
        read_only_fields = ['followupid', 'added_dts']

    def validate_actiontaken(self, value):
        """Ensure action taken is not empty or whitespace."""
        if not value or not value.strip():
            raise serializers.ValidationError("Action taken is required and cannot be blank.")
        return value

    def validate_executiveid(self, value):
        """Executive ID must be a positive integer."""
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Executive ID must be a positive integer (greater than 0)."
            )
        return value

    def validate_leadid(self, value):
        """Ensure the referenced Lead exists (DRF FK validation handles this, extra clarity)."""
        if value is None:
            raise serializers.ValidationError("A valid Lead must be referenced.")
        return value

    def create(self, validated_data):
        validated_data['added_dts'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        validated_data.setdefault('added_by', self._get_added_by())
        return self._safe_create(validated_data)

    def update(self, instance, validated_data):
        return self._safe_update(instance, validated_data)
