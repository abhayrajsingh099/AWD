from django.shortcuts import render, redirect
from .forms import EmailForm
from django.contrib import messages
# Create your views here.
from dataentry.utils import send_email_notification
from .models import Subscribers
from .tasks import send_email_task

def send_email(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)

        if email_form.is_valid():
            email_object = email_form.save() # eg. we get developers in email_object 

            # Send an email without attachements Rn
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            email_list = request.POST.get('email_list')
            #Access the selected email list
            email_list = email_object.email_list #list of emails in developers
            
            #Extract email addresses from the subscriber model in the selected email list
            subscribers = Subscribers.objects.filter(email_list=email_list) #stored emails of (developers list only) using filter in subscribers
            
            to_email = [email.email_address for email in subscribers]

            
            attachment = None
            if email_object.attachment:
                attachment = email_object.attachment.path
            

            #handover email sending tasks to celery
            send_email_task.delay(mail_subject, message, to_email, attachment)

            #display success message
            messages.success(request, "Email sent Successfully")
            return redirect('send_email')
    else:
        email_form = EmailForm()
        return render(request, 'emails/send-email.html', {'email_form':email_form})
