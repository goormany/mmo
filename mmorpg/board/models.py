from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.author_user.username

    class Meta:
        verbose_name = ('Автор')
        verbose_name_plural = ('Авторы')


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, blank=False, null=False)
    is_published = models.BooleanField(default=True)
    text = models.TextField(max_length=2048)
    category = models.ManyToManyField(Category)
    date_created = models.DateTimeField(auto_now_add=True)
    respond = models.ManyToManyField(User, through='ResponsePost', related_name='post_responses')

    def __str__(self):
        return f'id: {self.id}'

    def previous_text(self):
        return str(self.text[:128])

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class ResponsePost(models.Model):
    accept = 'A'
    denied = 'D'
    no_answer = 'N'
    POSITION = [
        (accept, 'Принята'),
        (denied, 'Отклонена'),
        (no_answer, 'Ожидание')
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_sender = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, default=no_answer, choices=POSITION)
    text = models.TextField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    def __str__(self):
        return f'от {self.user_sender} на пост {self.post}. ID = {self.id}'
