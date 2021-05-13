from django.db import models

# Crie seus modelos aqui.

from django.urls import reverse # Usado para gerar URLs revertendo os padrões de URL

class Genre(models.Model):
    "" "Modelo que representa um gênero de livro." ""
    name = models.CharField(max_length=200, help_text='Digite um gênero de livro (por exemplo, ficção científica)')

    def __str__(self):
        "" "String para representar o objeto Model." ""
        return self.name


class Book(models.Model):
    "" "Modelo que representa um livro (mas não uma cópia específica de um livro)." ""
    title = models.CharField(max_length=200)

    # Chave estrangeira usada porque o livro pode ter apenas um autor, mas os autores podem ter vários livros
     # Autor como string em vez de objeto porque ainda não foi declarado no arquivo
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Digite uma breve descrição do livro')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # ManyToManyField usado porque o gênero pode conter muitos livros. Os livros podem abranger muitos gêneros.
     # A classe de gênero já foi definida para que possamos especificar o objeto acima.
    genre = models.ManyToManyField(Genre, help_text='Selecione um gênero para este livro')

    def __str__(self):
        "" "String para representar o objeto Model." ""
        return self.title

    def get_absolute_url(self):
        "" "Retorna o url para acessar um registro de detalhes para este livro." ""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

import uuid # Obrigatório para instâncias de livro exclusivas
from datetime import date
from django.contrib.auth.models import User

class BookInstance(models.Model):
    "" "Modelo que representa uma cópia específica de um livro (ou seja, que pode ser emprestado da biblioteca)." ""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID exclusivo para este livro específico em toda a biblioteca')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        "" "String para representar o objeto Model." ""
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    "" "Modelo que representa um autor." ""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        "" "Retorna o url para acessar uma instância particular do autor." ""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        "" "String para representar o objeto Model." ""
        return f'{self.last_name}, {self.first_name}'
        