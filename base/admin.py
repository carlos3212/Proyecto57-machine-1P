from django.contrib import admin
from .models import Element, Source, Repositorie, Author


# Register your models here.
def get_list_display(model, field_exclude=[]):
    # if field_exclude is None:
    #     field_exclude = ['id']

    return [field.name for field in model._meta.fields if field.attname not in field_exclude]


class ElementModelAdmin(admin.ModelAdmin):
    list_display = get_list_display(Element)
    search_fields = ['_id', '_index', '_type']


class SourceModelAdmin(admin.ModelAdmin):
    list_display = get_list_display(Source, field_exclude=['description', 'fullText', 'rawRecordXml', 'similarities'])
    filter_horizontal = ['authors_m2m', 'repositories_m2m', 'topics_m2m']
    search_fields = ['title']
    list_filter = ['repositories_m2m', 'authors_m2m', 'topics_m2m']


class RepositorieModelAdmin(admin.ModelAdmin):
    list_display = get_list_display(Repositorie)


class AuthorModelAdmin(admin.ModelAdmin):
    list_display = get_list_display(Author)
    # search_fields = ['_id', '_index', '_type']


# admin.site.register(Element, ElementModelAdmin)
admin.site.register(Source, SourceModelAdmin)
admin.site.register(Repositorie, RepositorieModelAdmin)
admin.site.register(Author, AuthorModelAdmin)
