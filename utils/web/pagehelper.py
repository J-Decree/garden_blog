from utils.pagination import Pagination


class PageHelper(object):
    Pager_class = Pagination

    def __init__(self, queryset, request, page, data_num=None):
        self.queryset = queryset
        self.request = request
        self.page = page
        self.data_num = queryset.count() if not data_num else data_num
        self.page_obj = self.Pager_class(self.page, self.data_num)

    @property
    def data_list(self):
        return self.queryset[self.page_obj.start:self.page_obj.end]

    @property
    def page_str(self):
        return self.page_obj.page_str(self.request.path)

    @property
    def total_num(self):
        return self.page_obj.total_count

    def is_current_page(self, page):
        return page == self.page
