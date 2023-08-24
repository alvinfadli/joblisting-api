from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

User = get_user_model()

class RegisterView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        try:
            data = request.data

            name = data['name']
            email = data['email']
            email = email.lower()
            password = data['password']
            re_password = data['re_password']
            is_hr = data['is_hr']

            if is_hr == 'True':
                is_hr = True
            else:
                is_hr = False

            if password == re_password:
                if len(password) >= 8:
                    if not User.objects.filter(email=email).exists():
                        if not is_hr:
                            User.objects.create_user(name=name, email=email, password=password)

                            return Response(
                                {'success': 'User created successfully'},
                                status=status.HTTP_201_CREATED
                            )
                        else:
                            User.objects.create_hr(name=name, email=email, password=password)

                            return Response(
                                {'success': 'HR account created successfully'},
                                status=status.HTTP_201_CREATED
                            )
                    else:
                        return Response(
                            {'error': 'User with this email already exists'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {'error': 'Password must be at least 8 characters in length'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'error': 'Passwords do not match'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:  # Capture and display the exception
            return Response(
                {'error': f'Something went wrong when registering an account: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RetrieveUserView(APIView):

    def get(self, request, format=None):
        try:
            user = User.objects.get(id=request.user.id)
            user_data = UserSerializer(user).data

            return Response(
                {'user': user_data},
                status=status.HTTP_200_OK
            )
        except Exception as e:  # Capture and display the exception
            return Response(
                {'error': f'Something went wrong when retrieving user details: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
