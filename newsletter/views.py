import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
# Create your views here.


active_campaign_url = settings.ACTIVE_CAMPAIGN_URL
active_campaign_key = settings.ACTIVE_CAMPAIGN_KEY

class NewsletterView(APIView):
    def post(self, request, format=None):
        data = self.request.data
        email = data['email']

        url = active_campaign_url  + '/api/3/contact/sync'
        data = {
            'contact': {
                'email': email
            }
        }
        headers = {
            'Accept': 'Application/json',
            'Content-Type': 'application/json',
            'Api-Token': active_campaign_key
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 201 and response.status_code != 200:
            return Response(
                {'error': 'Something went wrong when creating contact'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        contact = response.json()

        try:
            contact_id = contact['contact']['id']
        except:
            return Response(
                {'error': 'Something went wrong when creating contact ID'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        url = active_campaign_key + '/api/3/contactTags'
        data = {
                'contactTag': contact_id,
                'tag': '1'
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 201 and response.status_code != 200:
            return Response(
                {'error': 'Something went wrong when tag to contact'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        url = active_campaign_key + '/api/3/contactLists'

        data = {
            'contactList': {
                'list': '1',
                'contact': contact_id,
                'status': '1'
            }
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 201 and response.status_code != 200:
            return Response(
                {'error': 'Something went wrong when adding contact to list'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        data = {
            'contactList': {
                'list': '2',
                'contact': contact_id,
                'status': '1'
            }
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 201 and response.status_code != 200:
            return Response(
                {'error': 'Something went wrong when adding contact to clano email list'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        else:
            return Response(
            {'success': 'Email added successfully'},
            status=status.HTTP_200_OK
        )

        