from django.db import models


# Create your models here.
class TimeStampModel(models.Model):
    """
    Permite a todos los objetos llevar un historico de los registros en la fecha que han sido creados y actualizados de
    manera invisible al usuario.
    """

    create_date = models.DateTimeField(auto_now_add=True)
    write_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        if hasattr(self, 'name'):
            return '%s' % self.name
        return ''

    class Meta:
        abstract = True


class Element(TimeStampModel):
    _id = models.AutoField(primary_key=True, unique=True)
    _index = models.CharField(max_length=150, blank=True, null=True)
    _type = models.CharField(max_length=75, blank=True, null=True)
    _score = models.FloatField()

    def __str__(self):
        return '%s' % self._id


class Author(TimeStampModel):
    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    # source = models.ForeignKey(Source, on_delete=models.CASCADE)
    name = models.CharField(max_length=350)

    def __str__(self):
        return '%s' % self.name


class Repositorie(TimeStampModel):
    class Meta:
        verbose_name = 'Repositorio'
        verbose_name_plural = 'Repositorios'

    # parent_source = models.ForeignKey(Source, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True, unique=True)
    openDoarId = models.IntegerField()
    name = models.CharField(max_length=350)
    urlHomepage = models.URLField(blank=True, null=True)
    urlOaipmh = models.URLField(blank=True, null=True)
    uriJournals = models.URLField(blank=True, null=True)
    physicalName = models.CharField(max_length=250, blank=True, null=True)
    source = models.CharField(max_length=250, blank=True, null=True)
    software = models.CharField(max_length=250, blank=True, null=True)
    metadataFormat = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    journal = models.CharField(max_length=250, blank=True, null=True)
    roarId = models.IntegerField()
    baseId = models.IntegerField(blank=True, null=True)
    pdfStatus = models.CharField(max_length=250, blank=True, null=True)
    nrUpdates = models.IntegerField()
    disabled = models.BooleanField()
    lastUpdateTime = models.DateTimeField(blank=True, null=True)
    repositoryLocation = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return '%s' % self.name


class Topic(TimeStampModel):
    # source = models.ForeignKey(Source, on_delete=models.CASCADE)
    name = models.CharField(max_length=350)


class Source(TimeStampModel):
    """
    Articulo
    """
    class Meta:
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'

    element = models.ForeignKey(Element, on_delete=models.SET_NULL, blank=True, null=True)
    id = models.AutoField(primary_key=True, unique=True)

    datePublished = models.CharField(max_length=30, blank=True, null=True)
    deleted = models.CharField(max_length=75)
    journals = models.CharField(max_length=350, blank=True, null=True)
    language = models.CharField(max_length=75, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    fullText = models.TextField(blank=True, null=True)
    fullTextIdentifier = models.URLField(blank=True, null=True)
    # identifiers =
    duplicateId = models.CharField(max_length=75, blank=True, null=True)
    publisher = models.CharField(max_length=250, blank=True, null=True)
    rawRecordXml = models.TextField()
    similarities = models.CharField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=750)
    year = models.PositiveIntegerField(blank=True, null=True)
    doi = models.CharField(max_length=75, blank=True, null=True)
    oai = models.CharField(max_length=75, blank=True, null=True)
    downloadUrl = models.URLField(blank=True, null=True)
    pdfHashValue = models.CharField(max_length=350, blank=True, null=True)
    documentType = models.CharField(max_length=350, blank=True, null=True)
    documentTypeConfidence = models.CharField(max_length=350, blank=True, null=True)
    citationCount = models.CharField(max_length=350, blank=True, null=True)
    estimatedCitationCount = models.CharField(max_length=350, blank=True, null=True)
    acceptedDate = models.CharField(max_length=350, blank=True, null=True)
    depositedDate = models.IntegerField(blank=True, null=True)
    publishedDate = models.IntegerField(blank=True, null=True)
    issn = models.CharField(max_length=350, blank=True, null=True)
    attachmentCount = models.IntegerField(blank=True, null=True)
    repositoryPublicReleaseDate = models.CharField(max_length=350, blank=True, null=True)
    extendedMetadataAttributes = models.CharField(max_length=350, blank=True, null=True)
    crossrefDocument = models.CharField(max_length=350, blank=True, null=True)
    magDocument = models.CharField(max_length=350, blank=True, null=True)
    orcidAuthors = models.CharField(max_length=350, blank=True, null=True)

    # extra info
    repositoryName = models.CharField(max_length=550, blank=True, null=True)
    repositoryId = models.IntegerField(blank=True, null=True)

    #
    authors_m2m = models.ManyToManyField(Author, verbose_name=Author._meta.verbose_name_plural)
    repositories_m2m = models.ManyToManyField(Repositorie, verbose_name=Repositorie._meta.verbose_name_plural, related_name="repositories_rel")
    topics_m2m = models.ManyToManyField(Topic, verbose_name=Topic._meta.verbose_name_plural, related_name="topics_rel")

    def __str__(self):
        return '%s' % self.title


class Language(TimeStampModel):
    id = models.IntegerField(primary_key=True, unique=True)
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=75)


class Relation(TimeStampModel):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)


class RepositoryDocument(TimeStampModel):
    pdfStatus = models.PositiveIntegerField()
    textStatus = models.PositiveIntegerField()
    metadataAdded = models.BigIntegerField()
    metadataUpdated = models.BigIntegerField()
    timestamp = models.BigIntegerField()
    depositedDate = models.BigIntegerField()
    indexed = models.PositiveIntegerField
    deletedStatus = models.CharField(max_length=5, blank=True, null=True)
    pdfSize = models.IntegerField()
    tdmOnly = models.BooleanField()
    pdfOrigin = models.URLField(blank=True, null=True)


class Subject(TimeStampModel):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    name = models.CharField(max_length=350)


class Url(TimeStampModel):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    url = models.URLField(max_length=350)


# class Similar:
#     id = ""
#     title = ""
#     url = ""
#     repositoryName = ""
#     repositoryId = ""
#     publisher = ""
#     year = ""
#     authors = ""
#     publisher = ""