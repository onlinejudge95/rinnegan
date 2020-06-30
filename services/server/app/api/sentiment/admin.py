from flask_admin.contrib.sqla import ModelView


class SentimentAdminView(ModelView):
    column_searchable_list = ("user_id", "keyword", "id")
    column_editable_list = ("keyword",)
    column_filters = ("user_id", "keyword", "id")
    column_sortable_list = ("user_id", "keyword", "id")
    column_default_sort = ("id", False)
