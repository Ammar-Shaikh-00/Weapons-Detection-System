from alertupload_rest.serializers import UploadAlertSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from threading import Thread
from django.core.mail import send_mail
import re
from twilio.rest import Client
from django.conf import settings

def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = Thread(target = function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator

@api_view(['POST'])
def post_alert(request):
    serializer = UploadAlertSerializer(data = request.data)

    if serializer.is_valid():
        serializer.save()
        identify_email_sms(serializer)
    else:
        return JsonResponse({'error': 'Unable to process data!'}, status=400)
    return Response(request.META.get('HTTP_AUTHORIZATION'))

def identify_email_sms(serializer):
    alert_receiver = serializer.data['alert_receiver']

    # Email validation
    if re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', alert_receiver):  
        print("Valid Email")
        send_email(serializer)

    # Pakistan Mobile Number validation (+92XXXXXXXXXX)
    elif re.compile(r"^\+92\d{10}$").match(alert_receiver):
        # 1) Begins with +92
        # 2) Then contains 10 digits 
        print("Valid Mobile Number")
        send_sms(serializer)
    
    else:
        print("Invalid Email or Mobile number")

@start_new_thread
def send_email(serializer):
    # Start a new thread to send the email
    Thread(target=_send_email_thread, args=(serializer,)).start()

def _send_email_thread(serializer):
    send_mail(
        'Weapon Detected!', 
        prepare_alert_message(serializer), 
        'm.ammarshaikh31@gmail.com',
        [serializer.data['alert_receiver']],
        fail_silently=False,
    )

@start_new_thread
def send_sms(serializer):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(body=prepare_alert_message(serializer),
                                    from_=settings.TWILIO_NUMBER,
                                    to=serializer.data['alert_receiver'])
    
def prepare_alert_message(serializer):
    uuid_with_slashes = split(serializer.data['image'], ".")
    print(serializer.data['image'])
    print(uuid_with_slashes)

    # Check if there are enough elements in the list
    if len(uuid_with_slashes) > 1:
        uuid = split(uuid_with_slashes[0], "/")
        print(uuid)
        # Check if uuid has enough elements after splitting
        if len(uuid) >= 2:
            #url = 'https://domjur-weapon-detection.herokuapp.com/alert/' + uuid[2]
            url = '127.0.0.1:8000/alert/' + uuid[1]
            return 'Weapon Detected! View alert at ' + url
        else:
            print("Error: 'uuid' does not have enough elements. Contents:", uuid)
            return "Error: Unable to generate alert URL."
    else:
        print("Error: 'uuid_with_slashes' does not have enough elements. Contents:", uuid_with_slashes)
        return "Error: Unable to generate alert URL."

def split(value, key):
    return str(value).split(key)