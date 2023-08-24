from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Listing
from .serializers import ListingSerializer
from django.contrib.postgres.search import SearchVector, SearchQuery

class ManageListingView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user

            if not user.is_hr:
                return Response(
                    {'error': 'User does not have necessary permissions for getting this listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )

            slug = request.query_params.get('slug')

            if not slug:
                listing = Listing.objects.order_by('-date_created').filter(
                    hr=user.email
                )
                listing = ListingSerializer(listing, many=True)
                
                return Response(
                    {'listings': listing.data},
                    status=status.HTTP_200_OK
                )

            if not Listing.objects.filter(
                hr=user.email,
                slug=slug
            ).exists():
                return Response(
                    {'error': 'Listing not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            listing = Listing.objects.get(hr=user.email, slug=slug)
            listing = ListingSerializer(listing)

            return Response(
                {'listing': listing.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving listing or listing detail'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve_values(self, data):
        title = data['title']
        slug = data['slug']
        company_name = data['company_name']
        city = data['city']
        state = data['state']
        description = data['description']
        

        salary = data['salary']
        try:
            salary = int(salary)
        except:
            return -1

        job_type = data['job_type']
        
        if job_type == 'FULL_TIME':
            job_type = 'Full Time'
        else:
            job_type = 'Part Time'

        is_available = data['is_available']

        if is_available == 'True':
            is_available = True
        else:
            is_available = False

        data = {
            'title' : title,
            'slug' : slug,
            'company_name' : company_name,
            'city' : city,
            'state' : state,
            'description' : description,
            'salary' : salary,
            'job_type' : job_type,
            'is_available' : is_available
        }

        return data

    def post(self, request):
        try:
            user = request.user

            if not user.is_hr:
                return Response(
                    {'error': 'You don\'t have neccessary permission to create listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )
            data = request.data

            title = data['title']
            slug = data['slug']

            if Listing.objects.filter(slug=slug).exists():
                return Response(
                    {'error': 'Slug already exists'},
                    status= status.HTTP_400_BAD_REQUEST
                )

            company_name = data['company_name']
            city = data['city']
            state = data['state']
            description = data['description']
            
            salary = data['salary']
            try:
                salary = int(salary)
            except:
                return Response(
                    {'error': 'Salary must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            job_type = data['job_type']
            if job_type == 'FULL_TIME':
                job_type = 'Full Time'
            else:
                job_type = 'Part Time'

            is_available = data['is_available']

            if is_available == 'True':
                is_available = True
            else:
                is_available = False

            Listing.objects.create(
                hr = user.email,
                title = title,
                slug = slug,
                company_name = company_name,
                city = city,
                state = state,
                description = description,
                salary = salary,
                job_type = job_type,
                is_available = is_available
            )

            return Response(
                {'success':'Job listing created successfully'},
                status=status.HTTP_201_CREATED
            )

        except:
            return Response(
                {'error': 'Something when wrong when creating job listing'},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def put(self, request):
        try:
            user = request.user

            if not user.is_hr:
                return Response(
                    {'error': 'User does not have necessary permissions for updating this listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )

            data = request.data

            data = self.retrieve_values(data)

            if data == -1:
                return Response(
                    {'error': 'Salary must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            title = data['title']
            slug = data['slug']
            company_name = data['company_name']
            city = data['city']
            state = data['state']
            description = data['description']
            salary = data['salary']
            job_type = data['job_type']
            is_available = data['is_available']

            if not Listing.objects.filter(hr=user.email, slug=slug).exists():
                return Response(
                    {'error': 'Listing does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            Listing.objects.filter(hr=user.email, slug=slug).update(
                title = title,
                slug = slug,
                company_name = company_name,
                city = city,
                state = state,
                description = description,
                salary = salary,
                job_type = job_type,
                is_available = is_available
            )

            return Response(
                {'success': 'Listing updated successfully'},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when updating listing'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def patch(self, request):
        try:
            user = request.user

            if not user.is_hr:
                return Response(
                    {'error': 'User does not have necessary permissions for updating this listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )

            data = request.data

            slug = data['slug']

            is_available = data['is_available']
            if is_available == 'True':
                is_available = True
            else:
                is_available = False

            if not Listing.objects.filter(hr=user.email, slug=slug).exists():
                return Response(
                    {'error': 'Listing does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            Listing.objects.filter(hr=user.email, slug=slug).update(
                is_available=is_available
            )

            return Response(
                {'success': 'Listing available status updated successfully'},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when updating listing'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def delete(self, request):
        try:
            user = request.user

            if not user.is_hr:
                return Response(
                    {'error': 'User does not have necessary permissions for deleting this listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )

            data = request.data

            try:
                slug = data['slug']
            except:
                return Response(
                    {'error': 'Slug was not provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not Listing.objects.filter(hr=user.email, slug=slug).exists():
                return Response(
                    {'error': 'Listing you are trying to delete does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            deleted_count, _ = Listing.objects.filter(hr=user.email, slug=slug).delete()

            if deleted_count > 0:
                return Response(
                    {'success': 'Listing deleted successfully'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Failed to delete listing'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'Something went wrong when deleting listing'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class ListingDetailView(APIView):
    def get(self, request, format=None):
        try:
            slug = request.query_params.get('slug')

            if not slug:
                return Response(
                    {'error': 'Must provide slug'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not Listing.objects.filter(slug=slug, is_available=True).exists():
                return Response(
                    {'error': 'Available job listing with this slug does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            listing = Listing.objects.get(slug=slug, is_available=True)
            listing = ListingSerializer(listing)

            return Response(
                {'listing': listing.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving listing detail'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ListingsView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        try:
            if not Listing.objects.filter(is_available=True).exists():
                return Response(
                    {'error': 'No available listings in the database'},
                    status=status.HTTP_404_NOT_FOUND
                )

            listings = Listing.objects.order_by('-date_created').filter(is_available=True)
            listings = ListingSerializer(listings, many=True)

            return Response(
                {'listings': listings.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving listings'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )