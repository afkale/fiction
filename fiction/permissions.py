from django.db.models.enums import StrEnum


class Groups(StrEnum):
    """Fiction app groups definition."""

    EDITORS = "Editors"
    VIEWERS = "Viewers"


GROUPS_PERMISSIONS = {
    Groups.VIEWERS: ["view_book", "view_page"],
    Groups.EDITORS: [
        "add_book",
        "delete_book",
        "change_book",
        "view_book",
        "add_page",
        "delete_page",
        "change_page",
        "view_page",
    ],
}
