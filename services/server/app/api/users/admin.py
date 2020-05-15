from flask_admin.contrib.sqla import ModelView


class UserAdminView(ModelView):
    column_searchable_list = ("username", "email", "id")
    column_editable_list = ("username", "email")
    column_filters = ("username", "email", "id")
    column_sortable_list = ("username", "email", "id")
    column_default_sort = ("id", False)
