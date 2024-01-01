from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import FileModel
from .serializers import FileSerializer
import os
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def signup_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    user = User.objects.create_user(username=username, password=password, email=email)

    login(request, user)

    token_generator = EmailVerificationTokenGenerator()
    token = token_generator.make_token(user)
    verification_link = request.build_absolute_uri(
        reverse('verify-email', kwargs={'user_id': user.id, 'token': token})
    )
    send_mail(
        'Verify your email',
        f'Click the link to verify your email: {verification_link}',
        'amitak0707@gmail.com',
        [user.email],
    )

    return Response({"message": "User created successfully. Please check your email to verify your account."}, status=201)

@api_view(['POST'])
def email_verify(request):
    user_id = request.data.get('user_id')
    token = request.data.get('token')
    user = get_object_or_404(User, id=user_id)
    token_generator = EmailVerificationTokenGenerator()

    if token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        return Response({"message": "Email verified successfully"}, status=200)
    else:
        return Response({"message": "Invalid token"}, status=400)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({"message": "Logged in successfully"}, status=200)
    else:
        return Response({"message": "Invalid username or password"}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    # Ensure the user is an Ops User
    if not request.user.is_ops_user:
        return Response({"message": "Permission Denied"}, status=403)

    file = request.FILES.get('file')
    if not file:
        return Response({"message": "File not provided"}, status=400)

    allowed_extensions = ['.pptx', '.docx', '.xlsx']
    _, file_extension = os.path.splitext(file.name)
    if file_extension.lower() not in allowed_extensions:
        return Response({"message": "Invalid file type"}, status=400)

    # Save the file and create an entry in the database
    uploaded_file = FileModel(user=request.user, file=file)
    uploaded_file.save()

    return Response({"message": "File uploaded successfully"}, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_files(request):
    if request.method == 'GET':
        files = FileModel.objects.filter(user=request.user)
        serializer = FileSerializer(files, many=True)
        return JsonResponse(serializer.data, safe=False)






