from django import template
from django.utils import timezone


register = template.Library()

def get_file_name(file_path):
    return  file_path.split('/')[-1]

def get_file_type(file_path):
    return file_path.split('/')[-2]

def get_local_uploded_at(uploaded_at):
    local_uploaded_at = timezone.localtime(uploaded_at)
    return local_uploaded_at.strftime('%Y.%m.%d')

register.filter('get_file_name', get_file_name)
register.filter('get_file_type', get_file_type)
register.filter('get_local_uploded_at', get_local_uploded_at)
