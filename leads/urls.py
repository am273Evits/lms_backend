# from django.contrib import admin
from django.urls import path, include, re_path
from .views import * 

urlpatterns = [
    # path('/api', home_VF)

        # lead_manager:

            # path('upload', uploadBusinessLeads.as_view()), #file upload
            # path('update', updateBusinessLeads.as_view()), #file upload
            # path('create_lead_manual', createLeadManual.as_view()), #file upload

            path('dashboard', dashboard.as_view()), #file upload

            path('view_lead_search/<str:lead_id>', viewAllLeadsSearch.as_view()), #view_all_leads
            path('view_all_leads/<int:page>', viewAllLeads.as_view()), #view_all_leads
            path('view_lead/<str:lead_id>', viewLeadsAllIdentifiers.as_view()), #view_all_leads

            #services
            path('create_country', Createcountry.as_view()),
            path('update_country/<int:id>', Updatecountry.as_view()),
            # path('delete_country/<int:id>', Deletecountry.as_view()),
            path('view_country', Viewcountry.as_view()),
            path('search_country/<str:id>', Searchcountry.as_view()),




            path('create_segment', CreateSegment.as_view()),
            path('view_segment', ViewSegment.as_view()),
            path('edit_segment/<int:id>', EditSegment.as_view()),
            path('archive_segment/<int:id>', ArchiveSegment.as_view()),
            path('view_archive_segment', ViewArchiveSegment.as_view()),
            path('unarchive_segment/<int:id>', UnarchiveSegment.as_view()),
            

            path('create_service', CreateService.as_view()),
            path('view_service', ViewService.as_view()),
            path('edit_service/<int:id>', EditService.as_view()),
            path('archive_service/<int:id>', ArchiveService.as_view()),
            path('view_archive_service', ViewArchiveService.as_view()),
            path('unarchive_service/<int:id>', UnarchiveService.as_view()),

            
            path('create_marketplace', CreateMarketplace.as_view()),
            path('view_marketplace', ViewMarketplace.as_view()),
            path('edit_marketplace/<int:id>', EditMarketplace.as_view()),
            path('archive_marketplace/<int:id>', ArchiveMarketplace.as_view()),
            path('view_archive_marketplace', ViewArchiveMarketplace.as_view()),
            path('unarchive_marketplace/<int:id>', UnarchiveMarketplace.as_view()),


            path('create_program', CreateProgram.as_view()),
            path('view_program', ViewProgram.as_view()),
            path('edit_program/<int:id>', EditProgram.as_view()),
            path('archive_program/<int:id>', ArchiveProgram.as_view()),
            path('view_archive_program', ViewArchiveProgram.as_view()),
            path('unarchive_program/<int:id>', UnarchiveProgram.as_view()),


            path('create_sub_program', CreateSubProgram.as_view()),
            path('view_sub_program', ViewSubProgram.as_view()),
            path('edit_sub_program/<int:id>', EditSubProgram.as_view()),
            path('archive_sub_program/<int:id>', ArchiveSubProgram.as_view()),
            path('view_archive_sub_program', ViewArchiveSubProgram.as_view()),
            path('unarchive_sub_program/<int:id>', UnarchiveSubProgram.as_view()),


            # path('create_commercials', CreateServiceAndCommercials.as_view()),
            # path('view_commercials/<int:page>', ViewServiceAndCommercials.as_view()),
            # path('edit_commercials/<int:id>', EditServiceCommercials.as_view()),
            # path('archive_commercials/<int:id>', ArchiveServiceCommercials.as_view()),
            # path('view_archive_commercials/<int:page>', ViewArchivedServiceAndCommercials.as_view()),
            # path('unarchive_commercials/<int:id>', UnarchiveServiceCommercials.as_view()),



            # path('update_marketplace/<int:id>', UpdateMarketplace.as_view()),
            # path('delete_marketplace/<int:id>', DeleteMarketplace.as_view()),
            # path('view_marketplace', ViewMarketplace.as_view()),
            # path('search_marketplace/<str:id>', SearchMarketplace.as_view()),

            # path('create_service', CreateServices.as_view()),
            # path('update_service', UpdateServices.as_view()),
            # path('delete_service/<int:id>', DeleteServices.as_view()),
            # path('view_service/<int:page>', ViewServices.as_view()),
            # path('search_service/<str:searchAtr>/<str:id>', SearchService.as_view()),

            # path('view_commercials/<int:id>', ViewCommercials.as_view()),
            # path('delete_commercials/<int:service_id>/<int:commercial_id>', DeleteCommercials.as_view()),


            #dropdown
            path('dropdown_department', dropdown_department.as_view()),
            path('dropdown_designation/<int:id>', dropdown_designation.as_view()),
            path('dropdown_program/<int:id>', dropdown_program.as_view()),
            path('dropdown_employee_status', dropdown_employee_status.as_view()),
            
        


            

            # path('get_table_fields/<str:table>', getTableFields.as_view()), #file upload
            # path('forms_submit/<str:table>/<str:lead_id>', formsSubmit.as_view()), #all tables submit

            # path('business_leads_all_tables', businessLeadsAllTables.as_view()), #all tables submit

            # path('assign_associate', assignAssociate.as_view()), #all tables submit
            # path('email_ask_for_details/<str:lead_id>', apiSubmitEmailAskForDetails.as_view()),
            # path('generate_mou/<str:lead_id>', mouFun.as_view()),
            # path('email_mou/<str:lead_id>', emailMouFun.as_view()), 

            # path('add_lead_delete_approval/<str:lead_id>', deleteLeadApprovalWrite.as_view()),


            # path('dashboard', dashboard.as_view()),


            # path('status_update/<str:lead_id>', statusUpdate.as_view()), #all tables submit

            # path('view_lead_business_identifiers/<str:lead_id>', viewLeadBusinessIdentifiers.as_view()), #view_all_leads
            # path('view_lead_comment/<str:lead_id>', viewLeadComment.as_view()), #view_all_leads
            # path('view_lead_contact_preference/<str:lead_id>', viewLeadContactPreference.as_view()), #view_all_leads
            # path('view_lead_followup/<str:lead_id>', viewLeadFollowup.as_view()), #view_all_leads
            # path('view_lead_seller_address/<str:lead_id>', viewLeadSellerAddress.as_view()), #view_all_leads
            # path('view_lead_service/<str:lead_id>', viewLeadService.as_view()), #view_all_leads
            # path('view_lead_website_store/<str:lead_id>', viewLeadWebsiteStore.as_view()), #view_all_leads

            # path('dashboard', dbTableAddData), #view_all_leads

            # path('field_email_proposal/<str:country>/<str:marketplace>', apiFieldEmailProposalMarkeplace.as_view()),
            # path('field_email_proposal/<str:country>/<str:marketplace>/<str:services>', apiFieldEmailProposalService.as_view()),

            #email proposal fields
            # path('field_email_proposal', apiFieldEmailProposal.as_view()),
            # path('field_email_proposal/<str:country>', apiFieldEmailProposalCountry.as_view()),
            # path('field_email_proposal/<str:country>/<str:marketplace>', apiFieldEmailProposalMarkeplace.as_view()),
            # path('field_email_proposal/<str:country>/<str:marketplace>/<str:services>', apiFieldEmailProposalService.as_view()),

            # path('email_proposal/<str:lead_id>', apiSubmitEmailProposal.as_view()),


            # path('field_add_new_service', fieldsAddNewServiceCountry.as_view()),
            # path('field_add_new_service/<str:country>', fieldsAddNewServiceMarketplace.as_view()),
            # path('field_add_new_service/<str:country>/<str:marketplace>', fieldsAddNewServiceServices.as_view()),
            # path('field_add_new_service/<str:country>/<str:marketplace>/<str:services>', fieldsAddNewServiceTeamLeader.as_view()),

            # path('add_new_service/<str:lead_id>', addNewService.as_view()),


            

            
]
