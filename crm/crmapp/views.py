from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Agent,Clients,Campaign,Clientcampaign
from django.contrib.auth.models import User,auth
import re,os
import random
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required




def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def agent(request):
    return render(request,'agent.html')

def loginfn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')  
            else:
                request.session['user'] = user.id  
                return redirect('agent')  
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('loginfn')
    return render(request, 'login.html')


def add_agent(request):
    if request.method == 'POST':
        firstName = request.POST.get('fname')
        lastName = request.POST.get('lname')
        userName = request.POST.get('uname')
        email = request.POST.get('mail')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')
        address = request.POST.get('address')
        location = request.POST.get('location')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pin_code = request.POST.get('pin_code')
        password = str(random.randint(100000, 999999))
        user = User.objects.create_user(username=userName, email=email, first_name=firstName, last_name=lastName, password=password)
        user.save()
        Agent.objects.create(address=address,phone=phone,profileimage=image,user=user,location=location,age=age,gender=gender,state=state,country=country,pin_code=pin_code)
        subject = 'Agent Account Created'
        message = (
            f"Hello {userName},\n\n"
            f"Your agent account has been created by the admin.\n"
            f"Login credentials:\n"
            f"Username: {userName}\n"
            f"Password: {password}\n\n"
            f"Please log in and change your password."
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
        messages.success(request, 'Agent has been added successfully by the admin.')
        return redirect('add_agent')
    return render(request, 'agent_reg.html')



def validate(request):
    field = request.GET.get('field')
    value = request.GET.get('value')

    if not field or not value:
        return JsonResponse({'available': False, 'error': 'Missing field or value'}, status=400)

    if field == 'username':
        exists = User.objects.filter(username=value).exists()
    elif field == 'email':
        exists = User.objects.filter(email=value).exists()
    elif field == 'phone':
        exists = Agent.objects.filter(phone=value).exists()
    else:
        return JsonResponse({'available': False, 'error': 'Invalid field'}, status=400)

    return JsonResponse({'available': not exists})



def agent_list(request):
    agents = Agent.objects.all()
    return render(request, 'agent_list.html', {'agents': agents})

def agent_detail(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    return render(request, 'agent_detail.html', {'agent': agent})

def agent_edit(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    user = agent.user

    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('uname')
        email = request.POST.get('mail')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pin_code = request.POST.get('pin_code')
        location = request.POST.get('location')
        image_uploaded = request.FILES.get('image')

        errors = []

        if username and User.objects.filter(username=username).exclude(id=user.id).exists():
            errors.append("Username already taken")


        if not email.endswith('.com'):
            errors.append("Email must end with '.com'")
        if email and User.objects.filter(email=email).exclude(id=user.id).exists():
            errors.append("Email already taken")

        if phone and (not phone.isdigit() or len(phone) != 10):
            errors.append("Phone number must be exactly 10 digits.")
        elif Agent.objects.filter(phone=phone).exclude(id=agent.id).exists():
            errors.append("Phone number already taken")

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('agent_edit', agent_id=agent.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if username:
            user.username = username
        user.save()

        agent.phone = phone
        agent.address = address
        agent.age = age
        agent.gender = gender
        agent.state = state
        agent.country = country
        agent.pin_code = pin_code
        agent.location = location

        if image_uploaded:
            if agent.profileimage and os.path.isfile(agent.profileimage.path):
                os.remove(agent.profileimage.path)
            agent.profileimage = image_uploaded

        agent.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('agent_edit', agent_id=agent.id)

    return render(request, 'agent_edit.html', {'agent': agent})

def delete_agent(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    agent.delete()
    return redirect('agent_list')



@login_required
def add_client(request):
    if request.method == 'POST':
        Clients.objects.create(
            agent=request.user,
            name=request.POST['name'],
            phone=request.POST['phone'],
            address=request.POST['address'],
            age=request.POST['age'],
            dob=request.POST['dob'],
            profession=request.POST.get('profession', ''),
            qualification=request.POST.get('qualification', ''),
            annual_income=request.POST.get('annual_income') or None,
            adhar_card=request.POST['adhar_card'],
            pan_card=request.POST['pan_card'],
            has_kids=request.POST.get('has_kids') == 'true',
            source_of_information=request.POST.get('source_of_information', ''),
            customer_service_satisfaction=request.POST.get('customer_service_satisfaction', ''),
            claim_satisfaction=request.POST.get('claim_satisfaction', ''),
            insurance_markup_area=request.POST.get('insurance_markup_area', ''),
            agent_visited_policy=request.POST.get('agent_visited_policy', ''),
            willingness_to_purchase=request.POST.get('willingness_to_purchase') == 'true',
            customer_preferences=request.POST.get('customer_preferences', ''),
            willingness_to_switch=request.POST.get('willingness_to_switch') == 'true',
            existing_company_name=request.POST.get('existing_company_name', ''),
            existing_insurance_name=request.POST.get('existing_insurance_name', ''),
            existing_claim_status=request.POST.get('existing_claim_status', ''),
        )
        messages.success(request, 'Client added successfully!')
        return redirect('add_client')  
    return render(request, 'add_client.html')

def validate_customer_field(request):
    field = request.GET.get('field')
    value = request.GET.get('value')
    response = {'is_valid': True, 'message': ''}
    if field == 'phone':
        if not re.fullmatch(r'\d{10}', value):
            response = {'is_valid': False, 'message': 'Phone must be exactly 10 digits.'}
        elif Clients.objects.filter(phone=value).exists():
            response = {'is_valid': False, 'message': 'Phone number already exists.'}

    elif field == 'adhar_card':
        if not re.fullmatch(r'\d{12}', value):
            response = {'is_valid': False, 'message': 'Aadhaar must be exactly 12 digits.'}
        elif Clients.objects.filter(adhar_card=value).exists():
            response = {'is_valid': False, 'message': 'Aadhaar already exists.'}

    elif field == 'pan_card':
        if not re.fullmatch(r'[A-Z]{5}[0-9]{4}[A-Z]', value):
            response = {'is_valid': False, 'message': 'Invalid PAN format (ABCDE1234F).'}
        elif Clients.objects.filter(pan_card=value).exists():
            response = {'is_valid': False, 'message': 'PAN already exists.'}
    return JsonResponse(response)

def list_clients(request):
    clients = Clients.objects.filter(agent=request.user)
    return render(request, 'list_clients.html', {'clients': clients})

def client_detail(request, client_id):
    client = get_object_or_404(Clients, id=client_id, agent=request.user)
    return render(request, 'client_detail.html', {'client': client})



def add_campaign(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        poster = request.FILES.get('poster')
        start_date = request.POST.get('start_date')
        location = request.POST.get('location')
        time = request.POST.get('time')  
        agent_user_id = request.POST.get('agent')
        agent_user = User.objects.get(id=agent_user_id) if agent_user_id else None
        Campaign.objects.create(title=title,description=description,poster=poster,start_date=start_date,location=location,time=time, agent=agent_user)
        return redirect('campaign_list')  
    agents = Agent.objects.select_related('user').all()
    return render(request, 'add_camp.html', {'agents': agents})


def campaign_list(request):
    campaigns = Campaign.objects.all()
    return render(request, 'campaign.html', {'campaigns': campaigns})

def agent_camp_view(request):
    agent = request.user
    campaigns = Campaign.objects.filter(agent=agent)
    print(campaigns)
    return render(request, 'agent_camp.html', {'campaigns': campaigns})

def agent_camp(request,id):
    campaigns = Campaign.objects.get(id=id)
    agent = request.user
    if request.method == 'POST':
      client = Clients.objects.create(
          agent=request.user,
          name=request.POST['name'],
          phone=request.POST['phone'],
          address=request.POST['address'],
          age=request.POST['age'],
          dob=request.POST['dob'],
          profession=request.POST.get('profession', ''),
          qualification=request.POST.get('qualification', ''),
          annual_income=request.POST.get('annual_income') or None,
          adhar_card=request.POST['adhar_card'],
          pan_card=request.POST['pan_card'],
          has_kids=request.POST.get('has_kids') == 'true',
          source_of_information=request.POST.get('source_of_information', ''),
          customer_service_satisfaction=request.POST.get('customer_service_satisfaction', ''),
          claim_satisfaction=request.POST.get('claim_satisfaction', ''),
          insurance_markup_area=request.POST.get('insurance_markup_area', ''),
          agent_visited_policy=request.POST.get('agent_visited_policy', ''),
          willingness_to_purchase=request.POST.get('willingness_to_purchase') == 'true',
          customer_preferences=request.POST.get('customer_preferences', ''),
          willingness_to_switch=request.POST.get('willingness_to_switch') == 'true',
          existing_company_name=request.POST.get('existing_company_name', ''),
          existing_insurance_name=request.POST.get('existing_insurance_name', ''),
          existing_claim_status=request.POST.get('existing_claim_status', ''),
          )
      client.save()
      assignment = Clientcampaign(
            agent=agent,
            client=client,
            campaign=campaigns
        )
      assignment.save()
      messages.success(request, 'Client added successfully!') 
    return render(request, 'add_client.html')


def edit_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        poster = request.FILES.get('poster')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        location = request.POST.get('location')
        time = request.POST.get('time')
        agent_user_id = request.POST.get('agent')
        agent_user = User.objects.get(id=agent_user_id) if agent_user_id else None
        
        campaign.title = title
        campaign.description = description
        if poster:  
            if campaign.poster and os.path.isfile(campaign.poster.path):
                os.remove(campaign.poster.path)
            campaign.poster = poster
        campaign.start_date = start_date
        campaign.end_date = end_date
        campaign.location = location
        campaign.time = time
        campaign.agent = agent_user
        campaign.save()
        return redirect('campaign_list') 
    agents = Agent.objects.select_related('user').all()
    return render(request, 'camp_edit.html', {'campaign': campaign, 'agents': agents})

def delete_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    campaign.delete()
    return redirect('campaign_list')

def admin_dashboard(request):
    total_agents = Agent.objects.count()
    total_clients = Clients.objects.count()
    total_campaigns = Campaign.objects.count()
    context = {
        'total_agents': total_agents,
        'total_clients': total_clients,
        'total_campaigns': total_campaigns,
    }
    return render(request, 'admin.html', context)


@login_required(login_url = 'index')
def resetpw(request):
    if request.method == 'POST':
        current_password = request.POST['currentpass']
        new_password = request.POST['newpass']
        confirm_password = request.POST['confirmpass']
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('resetpw')
        if new_password == confirm_password:
            if len(new_password) < 8 or not any(char.isupper() for char in new_password) \
                or not any(char.isdigit() for char in new_password) \
                or not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/~' for char in new_password):
                messages.error(request, 'Password must be at least 8 characters long and contain at least one uppercase letter, one digit, and one special character.')
                return redirect('resetpw')
            else:
                user = User.objects.get(id=request.user.id)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successfully.')
                return redirect('loginfn')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('resetpw')
    return render(request, 'password.html')


def agent_location(request):
    return render(request,'agent_location.html')

def camp_location(request):
    return render(request,'camp_location.html')


def logoutfn(request):
    auth.logout(request)
    return redirect('home')


def view_campaign_clients(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    clients = Clients.objects.filter(clientcampaign__campaign=campaign).distinct()
    return render(request, 'campaign/view_clients.html', {
        'campaign': campaign,
        'clients': clients
    })

def agent_clients_view(request, id):
    agent = User.objects.get(id=id)
    client_ids_in_campaigns = Clientcampaign.objects.filter(
        agent=agent, client__isnull=False
    ).values_list('client_id', flat=True).distinct()
    clients_through_campaign = Clients.objects.filter(id__in=client_ids_in_campaigns)
    for client in clients_through_campaign:
        client.campaign_status = "Through Campaign"
    clients_without_campaign = Clients.objects.filter(agent=agent).exclude(id__in=client_ids_in_campaigns)
    for client in clients_without_campaign:
        client.campaign_status = "Without Campaign"
    all_clients = list(clients_through_campaign) + list(clients_without_campaign)
    return render(request, 'camp_agent.html', {
        'all_clients': all_clients
    })
