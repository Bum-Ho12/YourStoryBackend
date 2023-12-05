'''
contains serializer classes that convert models to JSON format.
'''
from rest_framework import serializers
from .models import Blog, Subscriber,Account

class AccountSerializer(serializers.ModelSerializer):
    '''
    serializes the Account model.
    '''
    class  Meta:
        '''meta class'''
        model = Account
        fields =    '__all__'
        extra_kwargs = {
            'password': {'write_only':True},
        }
        def save(self,validated_data):
            ''' overrides the save method.'''
            # pylint: disable = E1120:no-value-for-parameter
            account = Account.objects.create_user(
                validated_data['email'],
                validated_data['username'],
            )

            account.set_password(validated_data['password'])
            account.save()
            return account


class SubscriberSerializer(serializers.ModelSerializer):
    '''
    serializes the Subscriber Model
    '''
    class Meta:
        '''meta class'''
        model = Subscriber
        fields = '__all__'
        extra_kwargs = {
            'created_at':{
                'required': False
            }
        }

class BlogSerializer(serializers.ModelSerializer):
    '''
    serializes the Blog model
    '''
    owner = serializers.SerializerMethodField('get_blog')
    class Meta:
        ''' meta class'''
        model = Blog
        fields = ['id', 'title','owner','created_at','updated_at','likes','dislikes','contentImage',
                    'imageCopyRight','story','frontImage','views','commission','topic']
        extra_kwargs = {
            'frontImage': {
                'required': False,
            },
            'contentImage':{
                'required': False,
            },
            'story':{
                'required': False,
            },
            'created_at':{
                'required': False
            }
        }
        depth=1
    def get_blog(self, blog):
        '''
        method handles content of user to be added in the blog story.
        '''
        blog = {
                'owner_name':blog.owner.username,
                'owner_description': blog.owner.description,
            }
        return blog
