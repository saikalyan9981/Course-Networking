from django import template

register = template.Library()

@register.assignment_tag
##
# \brief give user's vote for a given post
# @param user
#  the user whose rating for the given post we desire
# @param addr
#  	current ip address
# @returns 1 if user upvoted, -1 if downvoted , else 'None'
def had_voted(user, addr, post):
	return post.rating.get_rating_for_user(user, addr)