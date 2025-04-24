from django.urls import path
from .import views

urlpatterns = [
   path('',views.home,name='home'),
   path('about',views.about,name='about'),
   path('admin_dashboard/',views.admin_dashboard, name='admin_dashboard'),
   path('agent',views.agent,name='agent'),

   path('loginfn',views.loginfn,name='loginfn'),
    path('resetpw',views.resetpw,name='resetpw'),
   

   path('add_agent',views.add_agent,name='add_agent'),
   path('validate/', views.validate, name='validate'),
   path('agents/', views.agent_list, name='agent_list'),
   path('agents/<int:agent_id>/', views.agent_detail, name='agent_detail'),
   path('agent_edit/<int:agent_id>/', views.agent_edit, name='agent_edit'),
   path('delete_agent/<int:agent_id>/', views.delete_agent, name='delete_agent'),


   path('add_client/', views.add_client, name='add_client'),
   path('validate-customer-field/', views.validate_customer_field, name='validate_customer_field'),
   path('clients/', views.list_clients, name='list_clients'),
   path('clients/<int:client_id>/', views.client_detail, name='client_detail'),


   path('add_campaign/', views.add_campaign, name='add_campaign'),
   path('campaign_list/', views.campaign_list, name='campaign_list'),
   path('edit_campaign/<int:campaign_id>/', views.edit_campaign, name='edit_campaign'),
   path('delete_campaign/<int:campaign_id>/', views.delete_campaign, name='delete_campaign'),

   path('agent_camp_view',views.agent_camp_view,name='agent_camp_view'),
   path('agent_camp/<int:id>/',views.agent_camp,name='agent_camp'),
   path('campaign/<int:campaign_id>/clients/', views.view_campaign_clients, name='view_campaign_clients'),
   path('agent_clients_view/<int:id>/', views.agent_clients_view, name='agent_clients_view'),

   path('agent_location',views.agent_location,name="agent_location"),
   path('camp_location',views.camp_location,name="camp_location"),

   path('logoutfn',views.logoutfn,name='logoutfn'),
  
]
