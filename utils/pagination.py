import math
from django.core.paginator import Paginator  # type: ignore


def make_pagination_range(
        page_range,
        qty_pages,
        current_page):
    '''
        Method to make pagination range.
        Requires:
            page_range -> list of pages.
            qty_pages -> number of pages to be displayed to the user
            current_page -> current page number
    '''

    total_pages = len(page_range)  # Total number of pages

    # Getting the half of the pages to be displayed to the user
    # in navigation.
    middle_range = math.ceil(qty_pages / 2)

    # First page to be displayed in the navigation
    start_range = current_page - middle_range

    # Last page to be displayed in the navigation
    stop_range = current_page + middle_range

    # Offset adjustment: if the start_range is bellow 0, its absolute value
    # will be used to the offset; else, it will be set to zero
    start_range_offset = abs(start_range) if start_range < 0 else 0

    # If start range < 0 => indicate that the current page is less than the
    # middle of navigation So, start_range will be set to the first page
    # And stop_range will be set to the value it had before + the
    # start_range_offset

    # Same logic is aplied to the next block (stop_range)
    # There is an error here
    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        stop_range_offset = total_pages - stop_range
        possible_start_range = start_range - abs(stop_range_offset)
        start_range = possible_start_range if possible_start_range >= 0 else 0
        stop_range = total_pages

    # Pagination is what this function returns
    # It returns all the information that was used or created here
    pagination = {
        'pagination': page_range[start_range: stop_range],
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages,

    }
    return pagination


def make_pagination(request, queryset, per_page, qty_pages=4):
    '''
            Method to create the pagination scheme.
        queryset -> list of items to be displayed in the pages
        per_page -> number os items to be displayed in each page
        qty_pages -> number of options in the navigation scheme
            Example: if qty_pages = 5 and the current page is 5
                It will be displayed the navigation itens to
                page 3,4,5,6,7
    '''
    # Try to get the page query in the url. If no attribute page is found
    # use 1 (representing the first page)
    try:
        current_page = int(request.GET.get('page', 1))
    # if the try raises an ValueError (ex: a letter was passed to page)
    # uses page 1
    except ValueError:
        current_page = 1

    # paginator (from docs): Give Paginator a list of objects, plus the number
    # of items you’d like to have on each page, and it gives you methods for
    # accessing the items for each page.
    paginator = Paginator(queryset, per_page)

    # Get the current page from paginator
    # this method allows to get any page
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        current_page=current_page,
        page_range=paginator.page_range,
        qty_pages=qty_pages
    )

    return page_obj, pagination_range
