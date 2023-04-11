from django.contrib.auth.models import User
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post, Author, ResponsePost
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import Group
from django.db.models.signals import m2m_changed, post_save
from mmorpg.settings import DEFAULT_FROM_EMAIL
from django.core.mail import EmailMultiAlternatives


@receiver(user_signed_up)
def set_user_author(sender=User, **kwargs):
    user = kwargs['user']
    a1_group = Group.objects.get(name='a1')
    a1_group.user_set.add(user.id)
    Author.objects.create(author_user=User.objects.get(pk=user.id))


@receiver(post_save, sender=ResponsePost)
def add_res(instance, created, *args, **kwargs):
    if created:
        post_ = instance.post
        author_posts_id = post_.author_post.id
        author_email = User.objects.get(pk=Author.objects.get(pk=author_posts_id).id).email

        html_context = render_to_string(
            'email/add_responses.html', {
                'text': instance.text,
                'title': post_.title,
                'date': instance.date_created,
                'user_sender': instance.user_sender,
                'link': f'http://127.0.0.1:8000/{post_.id}'
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Новый отклик на объявление "{post_.title}"',
            body='',
            from_email=None,
            to=[author_email]
        )

        msg.attach_alternative(html_context, 'text/html')
        msg.send()


@receiver(post_save, sender=ResponsePost)
def accept_responses(instance, created, *args, **kwargs):
    if not created:

        if instance.status == 'A':

            email_s = User.objects.get(pk=instance.user_sender.id).email

            html_context = render_to_string(
                'email/accept_responses.html',
                {
                    'user_a': instance.user_sender,
                    'link': f'http://127.0.0.1:8000/{instance.post.id}',
                    'title': instance.post.title,
                    'u_a': User.objects.get(pk=instance.post.author_post.id).email,
                }
            )

            msg = EmailMultiAlternatives(
                subject='Ответ по отклику',
                body='',
                from_email=None,
                to=[email_s]
            )

            msg.attach_alternative(html_context, 'text/html')
            msg.send()

        elif instance.status == 'D':

            email_s = User.objects.get(pk=instance.user_sender.id).email

            html_context = render_to_string(
                'email/denied_responses.html',
                {
                    'user_a': instance.user_sender,
                    'link': f'http://127.0.0.1:8000/{instance.post.id}',
                    'title': instance.post.title,
                }
            )

            msg = EmailMultiAlternatives(
                subject='Ответ по отклику',
                body='',
                from_email=None,
                to=[email_s]
            )

            msg.attach_alternative(html_context, 'text/html')
            msg.send()
        else:
            pass







