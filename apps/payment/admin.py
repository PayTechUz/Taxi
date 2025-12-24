from django.contrib import admin

from unfold.admin import ModelAdmin
from unfold.decorators import display

from apps.payment.models import Wallet


@admin.register(Wallet)
class WalletAdmin(ModelAdmin):
    list_display = ('id', 'user', 'display_balance', 'created_at', 'updated_at')
    search_fields = ('id', 'user__username', 'user__email')
    ordering = ('-created_at',)
    list_filter = ('created_at',)
    list_filter_submit = True
    search_help_text = "Search by ID, username or email"

    @display(description="Balance", label=True)
    def display_balance(self, obj):
        return f"{obj.balance:,.2f} UZS"

    fieldsets = (
        (None, {
            "fields": ("user",)
        }),
        ("Financials", {
            "classes": ("tab",),
            "fields": ("balance",)
        }),
        ("Timestamps", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at")
        }),
    )
    readonly_fields = ("created_at", "updated_at")

