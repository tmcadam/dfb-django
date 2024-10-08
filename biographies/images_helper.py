from itertools import cycle
from bs4 import BeautifulSoup
from django.template import loader

def generate_image_tags(images):
    tags = []
    after_para = 1
    class_right = "float-sm-right ml-sm-3"
    class_left = "float-sm-left mr-sm-3"
    class_toggle = cycle([class_right, class_left])
    template = loader.get_template("images/_tag.html")
    for image in images:
        pos_class = next(class_toggle)
        tag = template.render({"img": image, "class": pos_class})
        tags.append( {"tag":tag, "after_para":after_para} )
        after_para += 2
    return tags

def insert_image(p, images):
    for img in images:
        if img["after_para"] == p:
            return img["tag"]
    return ""

def get_body_elements(body):
    soup = BeautifulSoup(body, "html.parser")
    return soup.find_all(True, recursive=False)

def interlace_images(biography):
    output = ""
    images = biography.images.all().order_by("id")
    image_tags = generate_image_tags(images)
    p_counter = 0
    for element in get_body_elements(biography.body):
        output += str(element)
        if len(element.text) > 200:
            p_counter += 1
            output += insert_image(p_counter, image_tags)
    return output
