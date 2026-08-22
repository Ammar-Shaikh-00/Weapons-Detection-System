from alertupload_rest.serializers import UploadAlertSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from threading import Thread
from django.core.mail import send_mail
import os
import re
from twilio.rest import Client
from django.conf import settings

def start_new_thread(function):
    def decorator(*args, **kwargs):
        thread = Thread(target=function, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
    return decorator

@api_view(['POST'])
def post_alert(request):
    serializer = UploadAlertSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        identify_email_sms(serializer)
        return Response(request.META.get('HTTP_AUTHORIZATION'))
    return JsonResponse({'error': 'Unable to process data!'}, status=400)

def identify_email_sms(serializer):
    alert_receiver = serializer.data['alert_receiver']
    if re.search(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', alert_receiver):
        send_email(serializer)
    elif re.compile(r'^\+92\d{10}$').match(alert_receiver):
        send_sms(serializer)
    else:
        print("Invalid Email or Mobile number")

@start_new_thread
def send_email(serializer):
    send_mail(
        'Weapon Detected!',
        prepare_alert_message(serializer),
        os.environ.get('EMAIL_HOST_USER', ''),
        [serializer.data['alert_receiver']],
        fail_silently=False,
    )

@start_new_thread
def send_sms(serializer):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=prepare_alert_message(serializer),
        from_=settings.TWILIO_NUMBER,
        to=serializer.data['alert_receiver'],
    )

def prepare_alert_message(serializer):
    image_name = os.path.basename(str(serializer.data['image']))
    alert_id = os.path.splitext(image_name)[0]
    return f'Weapon Detected! View alert at http://127.0.0.1:8000/alert/{alert_id}/'
