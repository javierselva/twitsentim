from django.contrib import admin

from .models import Query, Query_data, Summary_tweet, Test_tweet

'''
This file is used to custom the Admin panel of the aplication.
The different classes are used in order to change the visualization of
these tables of the database.
'''

class QueryDisplay(admin.ModelAdmin):
    #Just selecting the order the fields will be shown
    list_display = ['query_text','id']

class TweetDisplay(admin.ModelAdmin):
    list_display = ['id','getQueryText','tweet_text','tweet_pol']
    #Si señor, así es como se accede al objeto Query que se presenta como clave ajena... Ô_Ô
    def getQueryText(self,obj):
        return obj.query_id.query_id.query_text

class Query_dataDisplay(admin.ModelAdmin):
    list_display = ['query_id','query_date',]
    #~ def getQueryText(self,obj):
        #~ return obj.query_id.query_text

class Test_feedbackDisplay(admin.ModelAdmin):
    list_display = ['id','tweet_text','tweet_pol']
# Add the tables to the admin site with the correspondign style (classes)
admin.site.register(Query, QueryDisplay)
admin.site.register(Summary_tweet, TweetDisplay)
admin.site.register(Query_data, Query_dataDisplay)
admin.site.register(Test_tweet, Test_feedbackDisplay)
