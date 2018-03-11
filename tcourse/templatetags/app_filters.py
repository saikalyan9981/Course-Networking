from django import template

register = template.Library()

@register.filter
##
# \brief gievs the corresp value of a key
# @param dict
#   a dictionry
# @param key
#   the key for whose value is desired
# @returns corresponding value if there is one else returns ''
def keyvalue(dict, key):
    try:
        return dict[key]
    except KeyError:
        return ''