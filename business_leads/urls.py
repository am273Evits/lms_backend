# from django.contrib import admin
from django.urls import path, include, re_path
from .views import * 

urlpatterns = [
    # path('/api', home_VF)

        # lead_manager:
            path('upload', uploadBusLdAmzSPNC.as_view()), #file upload
            path('view_all_leads/<int:page>', viewAllLeads.as_view()), #view_all_leads
            path('view_lead/<str:table>/<str:lead_id>', viewLeadsAllIdentifiers.as_view()), #view_all_leads
            path('get_table_fields/<str:table>', getTableFields.as_view()), #file upload
            path('forms_submit/<str:table>/<str:lead_id>', formsSubmit.as_view()), #all tables submit

            path('assign_associate', assignAssociate.as_view()), #all tables submit



            # path('view_lead_business_identifiers/<str:lead_id>', viewLeadBusinessIdentifiers.as_view()), #view_all_leads
            # path('view_lead_comment/<str:lead_id>', viewLeadComment.as_view()), #view_all_leads
            # path('view_lead_contact_preference/<str:lead_id>', viewLeadContactPreference.as_view()), #view_all_leads
            # path('view_lead_followup/<str:lead_id>', viewLeadFollowup.as_view()), #view_all_leads
            # path('view_lead_seller_address/<str:lead_id>', viewLeadSellerAddress.as_view()), #view_all_leads
            # path('view_lead_service/<str:lead_id>', viewLeadService.as_view()), #view_all_leads
            # path('view_lead_website_store/<str:lead_id>', viewLeadWebsiteStore.as_view()), #view_all_leads


            # path('dashboard', dbTableAddData), #view_all_leads


            #email proposal fields
            path('field_email_proposal', apiFieldEmailProposal.as_view()),
            path('field_email_proposal/<str:country>', apiFieldEmailProposalCountry.as_view()),
            path('field_email_proposal/<str:country>/<str:marketplace>', apiFieldEmailProposalMarkeplace.as_view()),
            path('field_email_proposal/<str:country>/<str:marketplace>/<str:services>', apiFieldEmailProposalService.as_view()),

            path('email_proposal_submit/<str:lead_id>', apiSubmitEmailProposal.as_view()),

            

            
]
