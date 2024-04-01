from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField       #pip install "django-phonenumber-field[phonenumbers]"
from django.core.mail import send_mail


class CustomUser(AbstractUser):
    username=models.CharField(max_length=100, null=True, blank=True, unique=True)
    email=models.EmailField(unique=True)
    phone_no = PhoneNumberField(null=True, unique=False)
    address=models.TextField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=["username"]


class NewsLetterSubscribers(models.Model):
    email=models.EmailField(unique=True)


    def __str__(self) -> str:
        return self.email


class NewsLetters(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.FileField(upload_to='newsletters/')

    def __str__(self):
        # return self.subject + " " + self.created_at.strftime("%B %d, %Y")
        return self.subject
    
    def send(self, request):
        contents = self.contents.read().decode('utf-8')
        # subscribers = NewsLetterSubscribers.objects.filter(confirmed=True)
        subscribers = NewsLetterSubscribers.objects.all()
        for sub in subscribers:
            send_mail(
                subject=self.subject,
                message=None,
                html_message=contents+ (
                            '<br><a href="{}?email={}">Unsubscribe</a>.').format(
                                request.build_absolute_uri('/user/unsubscribe-newsletter/'),
                                sub.email),
                                
                from_email=None,
                recipient_list=[sub.email],  
            )




