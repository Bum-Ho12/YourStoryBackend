'''
handles the views part of the backend.
'''
import datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from  rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from  rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes,parser_classes
from django.shortcuts import render
from .models import Blog, Subscriber,Account,ImageFile,ContentSection
from .serializers import BlogSerializer,SubscriberSerializer,AccountSerializer

# Create your views here.

TOPICS = ['General',
    'Technology','Mobile','Laptops','Music',
    'Animation','Art','Movies','Sports',
    'Cousine','Travel','Lifestyle','Politics',
    'Education','Clothing','Brand','War','Games',
    'Renovation','Philanthropy','Wealth','Business',
    'Aviation','Automobiles','Trading and Economics',
    'Religion and Faith','Health','Development',
    'Beauty and Fashion','Physique','Culture',
    'Exploration','Nature','Climate and Ecology',
    'Space','Transport','Vacation'
    ]



def index(request):
    '''host main templates'''
    return render(request, 'index.html')

@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def registration_view(request):
    ''' handles the registration of a Blogger'''
    if request.method == 'POST':
        serialized = AccountSerializer(data=request.data)
        data = {}
        if serialized.is_valid():
            account = serialized.save()
            obj = Account.objects.get(email=account.email)
            obj.save()
            data['response'] = "successfully registered a new user"
            data['email'] = account.email
            data['username'] = account.username
            data['description']=account.description
            # pylint: disable = E1101:no-member
            token = Token.objects.get(user=account).key
            data['token'] = token
            return Response(data, status= status.HTTP_201_CREATED)
        else :
            data = serialized.errors
            return Response(data, status= status.HTTP_501_NOT_IMPLEMENTED)

#logs user in the system
@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def custom_login(request):
    '''
    handles the verification and assignment of token to an Account.
    '''
    data = request.data
    try:
        email = data['email']
        password = data['password']
        # pylint: disable = W0702:bare-except
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        user = Account.objects.get(email=email, password=password)
        # pylint: disable = W0702:bare-except
    except:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        user_token = user.auth_token.key
    # pylint: disable = W0702:bare-except
    except:
        # pylint: disable = E1101:no-member
        user_token = Token.objects.create(user=user)
    data = {'token': user_token}
    data['email'] = user.email
    data['username'] = user.username
    data['description']=user.description
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
# pylint: disable = W0613:unused-argument
def all_blogs(request):
    '''fetches all blogs that have been published'''
    # pylint: disable = E1101:no-member
    blogs = Blog.objects.all()
    sr= BlogSerializer(blogs, many = True)
    data = sr.data
    return Response(data = data, status = status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_blogs(request):
    '''method returns the blogs created by a certain author'''
    # pylint: disable = E1101:no-member
    blogs = Blog.objects.filter(owner=request.user)
    sr= BlogSerializer(blogs, many = True)
    data = sr.data
    return Response(data = data, status = status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
# pylint: disable = W0613:unused-argument
def all_subscribers(request):
    # pylint: disable = E1101:no-member
    '''fetches all subscribers'''
    subscriber = Subscriber.objects.all()
    sr= SubscriberSerializer(subscriber, many = True)
    data = sr.data
    return Response(data = data, status = status.HTTP_200_OK)

#logs user out of the  system
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    '''handles Account logout'''
    request.user.auth_token.delete()
    data={}
    data['success'] = 'successfully signed out'
    return Response(data=data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_blog(request):
    '''fetches a blog by id'''
    # pylint: disable = W0622:redefined-builtin
    id = request.data.get('id')
    # pylint: disable = E1101:no-member
    blog = Blog.objects.get(id = id)
    try:
        sr = BlogSerializer(blog)
        data = sr.data
        return Response(data,status = status.HTTP_200_OK)
    except blog.DoesNotExist:
        data = 'Blog does not exist'
        return Response(data, status= status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def register_subscriber(request):
    '''handles subscriber registration'''
    subscriber_reg = SubscriberSerializer(data= request.data)
    if subscriber_reg.is_valid():
        subscriber_reg.save()
        # pylint: disable = E1101:no-member
        sr_data = Subscriber.objects.get(email =request.data.get('email'))
        sr = SubscriberSerializer(sr_data)
        data = sr.data
        return Response(data=data, status= status.HTTP_201_CREATED)
    else:
        data = 'User already exist!'
        return Response(data,status= status.HTTP_409_CONFLICT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def post_blog(request):
    '''handles blog publishing'''
    blog_sr = BlogSerializer(data= request.data)
    files = request.FILES.get('frontImage')
    content_files = request.FILES.getlist('contentImages')
    stories = request.data.getlist('story')
    if files or content_files:
        request.data.pop('frontImage')
        request.data.pop('contentImages')
        request.data.pop('story')
        if blog_sr.is_valid():
            blog_sr.save(owner = request.user)
            # pylint: disable = E1101:no-member
            obj =  Blog.objects.get(id = blog_sr.data['id'])
            context = blog_sr.data
            obj.frontImage = request.FILES.get('frontImage')
            obj.save()
            uploaded_images = []
            for content_file in content_files:
                # pylint: disable = E1101:no-member
                content = ImageFile.objects.create(media = content_file)
                uploaded_images.append(content)
            obj.contentImage.add(*uploaded_images)
            content_sections = []
            for story in stories:
                content_section = ContentSection.objects.create(story=story)
                content_sections.append(content_section)
            obj.story.add(*content_sections)
            context['frontImage'] = obj.frontImage.url
            context['contentImages'] = [file.media.url for file in uploaded_images]
            context['story'] = [section.story for section in content_sections]
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(blog_sr.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        if blog_sr.is_valid():
            blog_sr.save()
            context = blog_sr.data
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(blog_sr.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_blog(request):
    '''handles delete of a published blog'''
    # pylint: disable = W0622:redefined-builtin
    id = request.data.get('id')
    # pylint: disable = E1101:no-member
    obj = Blog.objects.get(id = id)
    try:
        operation = obj.delete()
        if operation:
            data = 'deleted successfully'
            return Response(data, status= status.HTTP_202_ACCEPTED)
        else:
            data = 'Seems an error occurred'
            return Response(data, status = status.HTTP_204_NO_CONTENT)
    except obj.DoesNotExist:
        return Response(data='Blog does not exist',status= status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
# pylint: disable = W0613:unused-argument
def get_latest_blogs(request):
    '''gets recently published blogs'''
    # pylint: disable = E1101:no-member
    objs = Blog.objects.all()
    if len(objs) <6:
        sr_data = BlogSerializer(objs, many = True)
        return Response(data=sr_data.data,status=status.HTTP_302_FOUND)
    elif len(objs)>=6:
        # pylint: disable = E1101:no-member
        blogs = Blog.objects.order_by('-id')[:6]
        sr_data = BlogSerializer(blogs, many = True)
        return Response(data=sr_data.data,status=status.HTTP_302_FOUND)
    else:
        data = 'No stories uploaded yet!'
        return Response(data = data, status = status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([AllowAny])
# pylint: disable = W0613:unused-argument
def get_latest_blog(request):
    '''gets the latest blog(recently published)'''
    # pylint: disable = E1101:no-member
    blog = Blog.objects.last()
    sr_data = BlogSerializer(blog)
    return Response(sr_data.data, status= status.HTTP_302_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
# pylint: disable = W0613:unused-argument
def get_statistics(request):
    '''gets stats of the mentioned blog'''
    today = datetime.datetime.now()
    # pylint: disable = E1101:no-member
    blogs = Blog.objects.all()
    subscribers = Subscriber.objects.all()
    monthly_subscribers = subscribers.filter(created_at__month__gte= today.month).count()
    total_likes = 0
    total_dislikes = 0
    total_views = 0
    for blog in blogs:
        total_dislikes+=blog.dislikes
        total_likes += blog.likes
        total_views +=blog.views
    context = {
        'monthly_subscribers': monthly_subscribers,
        'likes': total_likes,
        'dislikes': total_dislikes,
        'blogs': blogs.count(),
        'total_subscribers': subscribers.count(),
        'total_views': total_views
    }
    return Response(data = context, status = status.HTTP_302_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def count_views(request):
    '''returns the number of viewers that have read the blog'''
    # pylint: disable = E1101:no-member
    blog = Blog.objects.get(id = request.data.get('id'))
    if blog:
        blog.views +=1
        blog.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response('no content', status = status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def count_likes(request):
    '''counts the number of likes a blog has gained'''
    # pylint: disable = E1101:no-member
    blog = Blog.objects.get(id = request.data.get('id'))
    if blog:
        blog.likes +=1
        blog.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response('no content', status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
#pylint: disable= W0613
def get_topics(request):
    '''get all topics'''
    return Response(data = TOPICS,status = status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def count_dislikes(request):
    '''counts the number of dislikes a blog has received'''
    # pylint: disable = E1101:no-member
    blog = Blog.objects.get(id = request.data.get('id'))
    if blog:
        blog.dislikes +=1
        blog.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response('no content', status = status.HTTP_404_NOT_FOUND)
