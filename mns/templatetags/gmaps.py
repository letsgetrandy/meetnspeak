from django import template
import urllib

register = template.Library()


@register.simple_tag()
def static_map(lat, lon):
    #
    domain = "maps.googleapis.com"
    path = "/maps/api/staticmap"
    latlon = '%s,%s' % (round(lat, 4), round(lon, 4))
    params = (
                ('maptype', 'roadmap', ),
                ('zoom', '10', ),
                ('size', '370x220', ),
                ('center', latlon, ),
                ('markers', latlon, ),
            )
    return '//%s%s?%s' % (domain, path, urllib.urlencode(params))
