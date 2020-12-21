import csv

import requests
from django.shortcuts import render

from .models import Element, Source, Repositorie, Author, Topic
from base.exercise import get_vars

API_KEY = "ocmhB4lIsNdQW7TVZyXLOPkUn8bFEupv"


def create_file(sources):
    """

    :param sources: Articulos
    :return:
    """
    with open('static/data.csv', mode='w', encoding='utf-8') as csv_file:
        fieldnames = ['title', 'authors', 'groups', 'keywords', 'topics', 'abstract']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for source in sources:
            topics = ", ".join([record.name for record in source.topics_m2m.all()])
            groups = ", ".join([record.name for record in source.repositories_m2m.all()])
            authors = ", ".join([record.name for record in source.authors_m2m.all()])
            if isinstance(source, Source):
                writer.writerow({
                    'title': source.title,
                    'authors': authors,
                    'groups': groups,
                    'keywords': topics,
                    'topics': topics,
                    'abstract': source.description,
                })


# Create your views here.
def home(request):
    # id de los objeto Source
    source_ids = []
    page_number = int(request.GET.get('page', 1))
    page_has_previous, page_has_next = False, False
    totalHits = 0
    num_pages = 0
    query = request.GET.get('q', '')
    if query:
        page_has_previous = page_number > 1
        URL = "https://core.ac.uk:443/api-v2/search/%s" % query
        pageSize = 10
        payload = {
            'page': page_number,
            'pageSize': pageSize,
            'apiKey': API_KEY,
        }
        try:
            r = requests.get(url=URL, params=payload)

            response = r.json()

            if 'totalHits' in response:
                totalHits = response['totalHits']
                num_pages = totalHits / pageSize
                if (pageSize * page_number) < totalHits:
                    num_pages += 1
                page_has_next = totalHits > (pageSize * page_number)

            if 'data' in response:
                data = response['data']
                for record in data:
                    if '_id' in record:
                        _id = record['_id']
                        fields_element = {
                            '_score': record['_score']
                        }
                        if '_index' in record:
                            fields_element['_index'] = record['_index']
                        if '_type' in record:
                            fields_element['_type'] = record['_type']
                        elements = Element.objects.filter(_id=_id)
                        # Select * from tabla where _id=5; Element.objects.filter(_id=5)
                        # Select * from tabla; = Element.objects.all()

                        if elements.exists():
                            elements.update(**fields_element)
                            element = elements.first()
                        else:
                            fields_element['_id'] = _id
                            element = Element.objects.create(**fields_element)  # SQL insert

                        if isinstance(element, Element):
                            if '_source' in record:
                                _source = record['_source']
                                if 'id' in _source:
                                    source_id = _source['id']
                                    source_ids.append(source_id)
                                    kwargs_source = {}
                                    for key, value in _source.items():
                                        """Verifico si el atributo key existe en la clase Source"""
                                        if hasattr(Source, key):
                                            kwargs_source[key] = value

                                    sources = element.source_set.filter(id=source_id)
                                    if sources.exists():
                                        element.source_set.update(**kwargs_source)
                                        source = sources.first()
                                    else:
                                        source = Source.objects.create(element=element, **kwargs_source)

                                    if 'repositories' in _source:
                                        fields_repositorie = {}
                                        repositories = _source['repositories']

                                        for repository in repositories:
                                            for key, value in repository.items():
                                                if hasattr(Repositorie, key):
                                                    fields_repositorie[key] = value

                                            repositories = Repositorie.objects.filter(id=repository['id'])

                                            if repositories.exists():
                                                repositorie = Repositorie.objects.get(id=repository['id'])
                                            else:
                                                # Si repositorio no existe lo creo
                                                repositorie = Repositorie.objects.create(**fields_repositorie)

                                            # Añadir los repositorios al articulo
                                            source.repositories_m2m.add(repositorie)

                                    if 'authors' in _source:
                                        authors = _source['authors']

                                        for name_author in authors:
                                            author, created = Author.objects.get_or_create(name=name_author)
                                            # Añado al autor actual
                                            source.authors_m2m.add(author)

                                    if 'topics' in _source:
                                        topics = _source['topics']

                                        for topic in topics:
                                            obj, created = Topic.objects.get_or_create(name=topic)
                                            source.topics_m2m.add(obj)
        except ConnectionError as e:
            # Cuando hay un error en la conexión
            pass
        except TimeoutError as e:
            pass
        except Exception as e:
            return article_search(request)

        sources = Source.objects.filter(id__in=source_ids)
        create_file(sources)
        my_data = get_vars()
        return render(request, 'base/result.html', context={
            'query': query,
            'sources': sources,
            'totalHits': totalHits,
            'page_number': page_number,
            'num_pages': num_pages,
            'page_has_previous': page_has_previous,
            'page_has_next': page_has_next,
            'my_data': my_data,
        })
    return render(request, 'base/index.html')


def article_search(request):
    # id de los objeto Source
    source_ids = []

    query = request.GET.get('q', '')
    if query:
        URL = "https://core.ac.uk:443/api-v2/articles/search/%s" % query
        payload = {
            'page': 1,
            'pageSize': 10,
            'metadata': True,
            'fulltext': False,
            'citations': False,
            'similar': True,
            'duplicate': False,
            'urls': False,
            'faithfulMetadata': False,
            'apiKey': API_KEY,
        }
        try:
            r = requests.get(url=URL, params=payload)

            response = r.json()
            if 'status' in response:
                pass

            if 'totalHits' in response:
                totalHits = response['totalHits']

            if 'data' in response:
                data = response['data']
                for _source in data:
                    if 'id' in _source:
                        source_id = _source['id']
                        source_ids.append(source_id)
                        kwargs_source = {}
                        for key, value in _source.items():
                            """Verifico si el atributo key existe en la clase Source"""
                            if hasattr(Source, key):
                                kwargs_source[key] = value

                        sources = Source.objects.filter(id=source_id)
                        if sources.exists():
                            sources.update(**kwargs_source)
                            source = sources.first()
                        else:
                            source = Source.objects.create(**kwargs_source)

                        if 'repositories' in _source:
                            fields_repositorie = {}
                            repositories = _source['repositories']

                            for repository in repositories:
                                for key, value in repository.items():
                                    if hasattr(Repositorie, key):
                                        fields_repositorie[key] = value

                                repositories = Repositorie.objects.filter(id=repository['id'])

                                if repositories.exists():
                                    repositorie = Repositorie.objects.get(id=repository['id'])
                                else:
                                    # Si repositorio no existe lo creo
                                    repositorie = Repositorie.objects.create(**fields_repositorie)

                                source.repositories_m2m.add(repositorie)

                        if 'authors' in _source:
                            authors = _source['authors']

                            for author in authors:
                                obj, created = Author.objects.get_or_create(name=author)
                                source.authors_m2m.add(obj)

                        if 'topics' in _source:
                            topics = _source['topics']

                            for topic in topics:
                                obj, created = Topic.objects.get_or_create(name=topic)
                                source.topics_m2m.add(obj)
        except ConnectionError as e:
            # Cuando hay un error en la conexión
            pass
        except TimeoutError as e:
            pass
        except Exception as e:
            pass

        sources = Source.objects.filter(id__in=source_ids)
        create_file(sources)
        my_data = get_vars()
        return render(request, 'base/result.html', context={
            'query': query,
            'sources': sources,
            'my_data': my_data,
        })
    return render(request, 'base/index.html')


def detail_info(request, id):
    """
    GET /articles/get/{coreId}
    """
    source = Source.objects.get(id=id)
    source_ids = []

    # Obteniendo articulos similares al actual
    URL = "https://core.ac.uk:443/api-v2/articles/get/%s" % source.id
    payload = {
        'similar': True,
        'apiKey': API_KEY,
    }

    try:
        r = requests.get(url=URL, params=payload)

        response = r.json()
        if 'data' in response:
            data = response['data']

            if 'similarities' in data:
                similarities = data['similarities']
                for record in similarities:
                    kwargs_source = {}
                    for key, value in record.items():
                        """Verifico si el atributo key existe en la clase Source"""
                        if hasattr(Source, key):
                            kwargs_source[key] = value

                    sources = Source.objects.filter(id=record['id'])
                    # Agregando a la lista ids de diccionarios
                    source_ids.append(record['id'])
                    if sources.exists():
                        sources.update(**kwargs_source)
                        _source = sources.first()
                    else:
                        _source = Source.objects.create(**kwargs_source)

                    if 'authors' in record:
                        authors = record['authors']

                        for author in authors:
                            obj, created = Author.objects.get_or_create(name=author)
                            _source.authors_m2m.add(obj)
    except Exception as e:
        pass
    sources = Source.objects.filter(id__in=source_ids)
    create_file(sources)
    return render(request, 'base/detail_view.html', context={
        'source': source,
        'sources': sources,
    })
