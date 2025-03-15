from django import template

register = template.Library()

def get_file_name(file_path):
    return  file_path.split('/')[-1]

register.filter('get_file_name', get_file_name)