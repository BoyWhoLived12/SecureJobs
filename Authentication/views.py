from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth.models import Group
from .models import *
from django.contrib.auth.decorators import login_required
from .decorators import *
from datetime import date
import numpy as np

# Create your views here.


@unauthenticated_user
def login_user(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        print(password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'User not found Incorrect username or password.')

    return render(request, 'login.html', context)


@unauthenticated_user
def register_user(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            account = form.cleaned_data.get('accType')
            print(account)
            if account == 'p':
                group = Group.objects.get(name='personal')
                user.groups.add(group)

            else:
                group = Group.objects.get(name='company')
                user.groups.add(group)
            login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, f"Congrats {username}, your account is successfully created.")
            if account == 'p':
                return redirect('p_account')

            else:
                return redirect('c_account')

    context = {'form': form}
    return render(request, 'register.html', context)


@login_required(login_url='login')
def home(request):
    context = {}
    username = request.user.username
    if request.user.groups.all()[0].name == 'company':
        companies = Company.objects.all()
        contacts = CompanyContact.objects.all()
        company = None
        contact = None
        for x in companies:
            if x.company_id == username:
                company = x
                break

        if company is None:
            return redirect('c_account')

        for x in contacts:
            if x.company == company:
                contact = x
                break
        jobs = []
        listJobs = JobPost.objects.all()
        for x in listJobs:
            if x.company == company:
                jobs.append(x)

        context['jobs'] = jobs
        context['company'] = company
        context['contact'] = contact
        context['owner'] = True
        return render(request, 'company_profile.html', context)

    else:
        followers = FollowerPersonal.objects.all()
        follower_profs = FollowerProf.objects.all()
        follower_prof = None
        follower = None
        for x in followers:
            if x.follower_id == username:
                follower = x
                break

        if follower is None:
            return redirect('p_account')
        for x in follower_profs:
            if x.follower == follower:
                follower_prof = x
                break

        context['follower'] = follower
        context['follower_prof'] = follower_prof
        print(follower_prof.photo)
        return render(request, 'personal_profile.html', context)
    # return render(request, 'personal_profile.html', context)


def account_company(request):
    context = {}
    if request.method == 'POST':
        user = request.user
        username = user.username
        name = request.POST['name']
        date = request.POST['date']
        category = request.POST['category']
        about = request.POST['about']
        interest = request.POST['interest']
        address = request.POST['address']
        mail_id = request.POST['email']
        phone = request.POST['phone']
        website = request.POST['website']
        reach = request.POST['reach']
        logo = request.POST['logo']
        print(name, date)
        ins1 = Company(company_id=username,
                       comp_name=name,
                       category=category,
                       date_inco=date,
                       interest=interest,
                       about=about,
                       logo=logo)
        ins1.save()
        ins = CompanyContact(company=ins1,
                             contact_email=mail_id,
                             contact_phone=phone,
                             address=address,
                             website=website,
                             reach=reach)
        ins.save()
        return redirect('home')

    return render(request, 'account_company.html', context)


def account_personal(request):
    context = {}
    if request.method == 'POST':
        username = request.user.username
        name = request.POST['name']
        dob = request.POST['date']
        gender = request.POST['gender']
        header = request.POST['header']
        interest = request.POST['interest']
        works = request.POST['work_exp']
        education = request.POST['education']
        website = request.POST['website']
        photo = request.POST['photo']
        print(photo)
        ins1 = FollowerPersonal(follower_id=username,
                                full_name=name,
                                gender=gender,
                                date_of_birth=dob)
        ins1.save()
        ins = FollowerProf(follower=ins1,
                           header=header,
                           interests=interest,
                           education=education,
                           git_website=website,
                           work_exp=works,
                           photo=photo)
        ins.save()
        return redirect('home')

    return render(request, 'account_personal.html', context)


@login_required(login_url='login')
def job_post(request):
    context = {}
    if request.method == 'POST':
        user = request.user.username
        company = None
        companies = Company.objects.all()
        for x in companies:
            if x.company_id == user:
                company = x
                break
        jobs = JobPost.objects.all()
        l = len(jobs)
        dateToday = date.today()
        title = request.POST['title']
        desc = request.POST['desc']
        job_type = request.POST['type']
        location = request.POST['location']
        link = request.POST['link']
        desc_pdf = request.POST['desc_pdf']
        ins = JobPost(company=company,
                      job_id=l+1,
                      job_date=dateToday,
                      job_title=title,
                      job_desc=desc,
                      jd_pdf=desc_pdf,
                      job_type=job_type,
                      job_location=location,
                      link=link)
        ins.save()
        return redirect('home')
    else:
        user = request.user
    return render(request, 'job_post.html', context)


@login_required(login_url='login')
def job_list(request):
    context = {}
    jobs = JobPost.objects.all()
    context['jobs'] = jobs
    return render(request, 'job_list.html', context)


@login_required(login_url='login')
def job_detail(request, slug):
    context = {}
    slug = int(slug)
    jobs = JobPost.objects.all()
    for x in jobs:
        if x.job_id == slug:
            job = x
            break

    company = job.company
    contacts = CompanyContact.objects.all()
    for x in contacts:
        if x.company == company:
            context['contact'] = x
            break
    context['company'] = company
    context['JobPost'] = job

    return render(request, 'job_detail.html', context)


@login_required(login_url='login')
def company_list(request):
    context = {}
    companies = Company.objects.all()
    context['companies'] = companies
    return render(request, 'company_list.html', context)


@login_required(login_url='login')
def company_detail(request, slug):
    context = {}

    companies = Company.objects.all()
    contacts = CompanyContact.objects.all()
    company = None
    contact = None
    for x in companies:
        if x.company_id == slug:
            company = x
            break

    if company is None:
        return redirect('c_account')

    for x in contacts:
        if x.company == company:
            contact = x
            break
    jobs = []
    listJobs = JobPost.objects.all()
    for x in listJobs:
        if x.company == company:
            jobs.append(x)

    context['jobs'] = jobs
    context['company'] = company
    context['contact'] = contact
    context['owner'] = False
    return render(request, 'company_profile.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')

