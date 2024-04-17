from django.core.management.base import BaseCommand
from schedule import every
import time
from leads.models import Leads
from account.models import UserAccount


class Command(BaseCommand):
    help = 'Runs a continuous task'

    def handle(self, *args, **options):
        # Run the task continuously
        while True:
            # Call your function here
            self.my_continuous_function()
            # Sleep for a specific interval (e.g., 1 minute)
            time.sleep(30)

    def my_continuous_function(self):
        # Your continuous task logic here
        # leadsData = Leads.objects.all()
        # users = UserAccount.objects.filter(department__title='business_development', designation__title='team_member')
        # print('users',len(users))
        # for u in users:
            # print('u',u.segment)
        leadsData = Leads.objects.select_related().filter(associate=None, visibility=True).all()
        # print(Leads.objects.select_related().filter(associate=None, visibility=True).count())
        for l in leadsData:
            for s in l.service_category_all.all():

                user = UserAccount.objects.filter(designation__title='team_member', segment=s.service.segment.id, service__service=s.service.service, marketplace__marketplace=s.service.marketplace, program__program=s.service.program)
                print('user', len(user))
                # print('user', s.service.service)
                # print('user', s.service.marketplace)
            # print([ s.service.segment.segment  for s in l.service_category_all.all()])
        # leadsData = Leads.objects.select_related().filter(
        #     service_category_all__service__segment__segment= user.segment, 
        #     service_category_all__service__service__in= user.service.all(), 
        #     service_category_all__service__marketplace__in= user.marketplace.all(),  
        #     service_category_all__service__program__in= user.program.all(),
        #     visibility = True
        #     ).all()
        

        # print('leadsData',leadsData)