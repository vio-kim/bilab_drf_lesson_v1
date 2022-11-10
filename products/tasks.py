from celery import shared_task

from django.core.mail import send_mail

@shared_task
# def send_email_celery():
#     send_mail(
#         subject='Hi',
#         message='This is my first letter',
#         from_email='odaulet99@gmail.com',
#         recipient_list=['odaulet99@gmail.com'],
#         fail_silently=True,
#         )
def adding_task(x, y):
    print("===== ADDing TASK =====")
    print(x+y)
    print("===== ===== =====")
    return x + y
