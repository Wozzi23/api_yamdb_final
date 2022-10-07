from rest_framework.pagination import PageNumberPagination

from api_yamdb.settings import PAGE_SIZE


class CommentsPaginator(PageNumberPagination):
    """
    Пагинатор осуществляющий пагинацию комментариев.
    PAGE_SIZE - константа регулирующая число комментариев на страницы,
    определяется в настройках проекта.
    """
    page_size = PAGE_SIZE
