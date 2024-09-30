import random
from biographies.models import Biography

def set_featured(bios):
    bios.update(featured=True)

def clear_featured():
    Biography.objects.all().update(featured=False)

def with_images(bios):
    return bios.filter(images__isnull=False)

def with_lifespan_author(bios):
    return bios.filter(lifespan__isnull=False).filter(authors__isnull=False)

def with_first_image_orientated(bios, orientation):
    orientated_bios = []
    for bio in bios:
        if bio.images.order_by("id").first().orientation == orientation:
            orientated_bios.append(bio)
    return orientated_bios

def get_random_from_list(bios, count):
    return random.sample(bios, count)

def get_queryset_from_list(bios_list):
    bio_ids = [bio.id for bio in bios_list]
    return Biography.objects.filter(id__in=bio_ids)

def reset_featured_bios():
    clear_featured()
    bios = with_images(Biography.objects.all())
    bios = with_lifespan_author(bios)
    bios_list = with_first_image_orientated(bios, "portrait")
    bios_list = get_random_from_list(bios_list, 6)
    bios = get_queryset_from_list(bios_list)
    set_featured(bios)
    return bios
