class PaginationLink:

    def __init__(self, link_number, link_type):
        self.link_number = link_number
        self.link_type = link_type

def generate_pagination_links(page_number, num_pages):

    pagination_links = list()

    if page_number > 1:

        pagination_links.append(PaginationLink(
            link_number = 1, 
            link_type = "nav_first"
        ))
        pagination_links.append(PaginationLink(
            link_number = page_number - 1, 
            link_type = "nav_prev"
        ))

    if page_number > 5:
        pagination_links.append(PaginationLink(
            link_number = None,
            link_type = "epsilon"
        ))

    for i in range(-4, 5):
        
        if page_number + i < 1 or page_number + i > num_pages:
            continue
        if i == 0:
            pagination_links.append(PaginationLink(
                link_number = page_number,
                link_type = "curr"
            ))
        elif i == -1:  
            pagination_links.append(PaginationLink(
                link_number = page_number + i,
                link_type = "prev"
            ))
        elif i == 1:
            pagination_links.append(PaginationLink(
                link_number = page_number + i,
                link_type = "next"            
            ))
        else:
            pagination_links.append(PaginationLink(
                link_number = page_number + i,
                link_type = "basic"
            ))
    if page_number <= num_pages - 5:
        pagination_links.append(PaginationLink(
            link_number = None,
            link_type = "epsilon"
        ))
    if page_number < num_pages:
        pagination_links.append(PaginationLink(
            link_number = page_number + 1,
            link_type = "nav_next"
        ))
        pagination_links.append(PaginationLink(
            link_number = num_pages,
            link_type = "nav_last"
        ))
            
    return pagination_links