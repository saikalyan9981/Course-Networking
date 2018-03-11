from django import template

register = template.Library()

@register.assignment_tag
##
# \brief concatenates a string and a number
# @param string
#	the given string
# @param num
# 	the given number
# @returns string concatenated with number
def apend(string,num):
	string+=str(num)
	return string