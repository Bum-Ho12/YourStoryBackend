'''
this file contains definition of models
that are to be used for the blog website
'''
from django.db import models
from django.conf import  settings
from  django.dispatch import  receiver
from  django.db.models.signals import post_save
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.validators import MinValueValidator
from  rest_framework.authtoken.models import Token
# Create your models here.

class MyAccountManager(BaseUserManager):
    '''
    model class that inherits from BaseUserManager model
    to differentiate from super user from a normal user.
    '''
    def create_user(self,email, username, password):
        '''
        overrides the create_user method in BaseUserManager to
        for categorization of super users and normal users.
        It makes sure the email and password fields are required.
        '''

        if not email:
            raise  ValueError('user must have an email address.')
        if not username:
            raise  ValueError('user must have a username.')
        user =self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        '''
        method overrides the create_superuser method to make sure
        the required fields are email and password.
        '''
        user = self.create_user(
            email = self.normalize_email(email),
            username=username,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser, PermissionsMixin):
    '''
    Account defines the fields in the database. important fields are:
        - email, username,description, last_login.
    '''
    email               = models.EmailField(max_length=60, verbose_name='email',unique=True)
    username            = models.CharField(max_length=30, unique=True)
    description         = models.CharField(blank=True,null = True,
                                        max_length=400,default='')
    date_joined         = models.DateTimeField(verbose_name='date joined',
                                        auto_now_add=True)
    last_login          = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin            = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=True)
    is_superuser        = models.BooleanField(default=False)
    hide_email          = models.BooleanField(default=True)

    objects = MyAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return f"{self.username}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

#pylint: disable = W0613:unused-argument
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created = False, **kwargs):
    '''
    this creates an authentication for the Account created.
    '''
    if created:
        # pylint: disable = E1101:no-member
        Token.objects.create(user=instance)


class Subscriber(models.Model):
    '''
    model that handles the registration of subscribers to the
    YourStory Blog.
    '''
    name = models.TextField(max_length= 50)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        '''
        Meta class.
        '''
        verbose_name_plural = 'Subscribers'

    def __str__(self):
        return f"{self.name}"

class ImageFile(models.Model):
    '''
    class that handles Image data
    '''
    index = models.IntegerField(validators=[MinValueValidator(1000)], null=True)
    media = models.ImageField()

    def __str__(self):
        # pylint: disable = E1101:no-member
        return f"{self.media.url}"

class ContentSection(models.Model):
    '''
    handles the content of the story.
    '''
    index = models.IntegerField(validators=[MinValueValidator(1000)],null=True)
    story = models.TextField(max_length=21845)
    def __str__(self):
        return f"{self.story}"

class Blog(models.Model):
    '''
    model that defines the fields required for a story:
    - title, frontImage, contentImage, ImageCopyRight,owner,story,
    story,likes, dislikes, views, created_at,commission.
    '''
    title = models.TextField(max_length=200)
    frontImage  = models.ImageField(blank=True)
    contentImage   = models.ManyToManyField(ImageFile,blank=True)
    topic          = models.CharField(default='General',max_length=50)
    imageCopyRight = models.TextField(max_length= 100)
    owner       = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    story       = models.ManyToManyField(ContentSection,blank=True)
    likes       = models.IntegerField(default=0)
    dislikes    = models.IntegerField(default=0)
    views       = models.IntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    commission  = models.BooleanField(default= True)

    class Meta:
        '''meta class sets the plural for the model'''
        verbose_name_plural = 'Blogs'

    def __str__(self):
        return f"{self.title}"
