from models import Profile, Account
import time
import logging


def get_user_addinfo(backend, details, response, social_user, uid,\
                    user, *args, **kwargs):
    log = logging.getLogger(__name__)
    log.debug('here we are')
    #load profile, defaults when creation empty
    #it returns a touple, profile is the object, created is the boolean if it's created or exists
    profile, created = Profile.objects.get_or_create(user=user)

    if created:
        log.debug('created')
        #create a new personal account and add this user to this account
        account = Account()
        account.save()
        account.add()
        account.users.add(user)
        account.save()
    
    else:
        log.debug('name: %s' %(user.username))
    profile.save()
    account = Account.objects.get_or_create(user=user)