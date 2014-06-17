from django.db import models
from django.contrib.auth.models import User
from social_auth.models import UserSocialAuth
from datetime import datetime 


# Extension of User class to add some properties (does not have any columns)
class Profile(models.Model):
    user = models.OneToOneField(User) 
    def __unicode__(self):
        return str(self.id)
    @property
    def shortname(self):
        return self.user.first_name.encode('utf-8')+' '+self.user.last_name[:1].encode('utf-8')+'.'
    @property
    def fullname(self):
        return self.user.first_name.encode('utf-8')+' '+self.user.last_name.encode('utf-8')

    @property
    def connectedSocialNetworks(self):
        return UserSocialAuth.objects.filter(user=self.user).all()
    @property
    def avatar(self):
        if len(self.connectedSocialNetworks)>0:
            return "http://avatars.io/"+self.connectedSocialNetworks.reverse()[0].provider+"/"+str(self.connectedSocialNetworks.reverse()[0].uid)+"?size=medium"    
        else:
            return 'http://www.gravatar.com/' + hashlib.md5(self.user.email.lower()).hexdigest() 

# Class for grouping several users to one billing account. Can be useful - if there is an organization, or a research team, which consists of 3 people working together.
class Account(models.Model):
    users = models.ManyToManyField(User, through = 'Membership')
    title = models.CharField(max_length=256)
    personal = models.BooleanField(default = False)
    creator =  models.ForeignKey(User, related_name = 'Creator') 
    total_earnings = models.DecimalField(max_digits=8, decimal_places=2) #sum of all fundtransfer amounts, where to_account = self (we keep it as a column to do less calls to aggregation of FundTransfer table)
    total_spendings = models.DecimalField(max_digits=8, decimal_places=2) #sum of all fundtransfer amounts, where from_account = self (we keep it as a column to do less calls to aggregation of FundTransfer table)
    deleted = models.DateTimeField(blank = True, null = True) 
    def recalculate(self, total_type): # 'earnings', 'spendings'
        if (total_type == 'earnings'):
            self.total_earning = FundTransfer.objects.filter(to_account = self).aggregate(Sum('amount'))['amount__sum']
        elif (total_type == 'spendings'):
            self.total_spendings = FundTransfer.objects.filter(from_account = self).aggregate(Sum('amount'))['amount__sum']
        self.save()
    # show current balance of an account (saldo)
    @property
    def balance(self):
        return self.total_earning - self.total_spending

MEMBERSHIP_TYPE = (('AN','Admin'),('MR','Member'))

class Membership(models.Model):
    user = models.ForeignKey(User)
    account = models.ForeignKey(Account)
    permission = models.CharField(max_length=2, choices=MEMBERSHIP_TYPE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

CURRENCY_TYPE = (('RM','Real Money'),('VM','Virtual Money'))
# when a worker earns money - they go from requestor to a worker
# when a worker/requestor wants to send money to another user - they do it via fundtransfer
class FundTransfer(models.Model):
    from_account = models.ForeignKey(Account, related_name = 'from_account', blank = True, null = True)
    to_account = models.ForeignKey(Account, related_name = 'to_account', blank = True, null = True)
    currency = models.CharField(max_length=2, choices=CURRENCY_TYPE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False) 
    description = models.CharField(max_length=1000, blank = True) # when we generate transfers we might add here a description - what this transfer is for.