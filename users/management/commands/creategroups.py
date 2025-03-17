from typing import Any

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from fiction.permissions import GROUPS_PERMISSIONS


class Command(BaseCommand):
    """This command will create all the required groups and permissions."""

    help = "Creates and updates the default groups and permissions."

    def handle(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=unused-argument
        ok = self.style.SUCCESS("[OK]")  # pylint: disable=no-member
        error = self.style.ERROR("[ERROR]")  # pylint: disable=no-member

        for group_name, perm_codes in GROUPS_PERMISSIONS.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"{ok} Created group {group_name}.")

            # Fetch permissions in one query for efficiency
            permissions = Permission.objects.filter(codename__in=perm_codes)

            # Check for missing permissions
            found_perms = set(permissions.values_list("codename", flat=True))
            missing_perms = set(perm_codes) - found_perms
            if missing_perms:
                for perm in missing_perms:
                    self.stdout.write(f"{error} Missing permission {perm}.")

            # Assign permissions in bulk
            group.permissions.set(permissions)
            self.stdout.write(
                f"{ok} Assigned {len(found_perms)} permissions to {group_name}."
            )

        self.stdout.write(f"{ok} Default groups and permissions setup complete.")
