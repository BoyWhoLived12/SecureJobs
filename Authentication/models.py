from django.db import models


class Company(models.Model):
    company_id = models.CharField(primary_key=True, max_length=150)
    comp_name = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    date_inco = models.DateField()
    interest = models.TextField()
    about = models.TextField()
    logo = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        db_table = 'company'


class CompanyContact(models.Model):
    company = models.ForeignKey(Company, models.CASCADE, primary_key=True, default=None)
    contact_email = models.CharField(max_length=40)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=60, blank=True, null=True)
    reach = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'company_contact'


class JobPost(models.Model):
    company = models.ForeignKey(Company, models.CASCADE, default=None)
    job_id = models.IntegerField(primary_key=True)
    job_date = models.DateField()
    job_title = models.CharField(max_length=40)
    job_desc = models.TextField()
    jd_pdf = models.CharField(max_length=150,null=True, blank=True)
    job_type = models.CharField(max_length=30, blank=True, null=True)
    job_location = models.CharField(max_length=50, blank=True, null=True)
    link = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        db_table = 'job_post'


class FollowerPersonal(models.Model):
    follower_id = models.CharField(primary_key=True, max_length=150)
    full_name = models.CharField(max_length=40)
    gender = models.CharField(max_length=1, blank=True, null=True)
    date_of_birth = models.DateField()

    class Meta:
        db_table = 'follower_personal'


class FollowerProf(models.Model):
    follower = models.ForeignKey(FollowerPersonal, models.CASCADE, primary_key=True, default=None)
    header = models.CharField(max_length=80, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    git_website = models.CharField(max_length=40, blank=True, null=True)
    work_exp = models.TextField(blank=True, null=True)
    photo = models.CharField(max_length=150, blank=True, null=True, default=None)

    class Meta:
        db_table = 'follower_prof'

