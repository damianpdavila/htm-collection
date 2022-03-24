# class to get a list of tags that belong to a specific categry
class TagsOfCategory():

    def __init__(self, categoryId):
        # INFUSIONSOFT API
        # import infusinosoft module
        from infusionsoft import Infusionsoft
        # apiname and key
        infusionsoft = Infusionsoft('education', 'APIKEYHERE')
        # API CALL
        #list to append desire tag and group relationship
        tag_list = []
        for x in range(10):
            # query for tag to get category they fall under 'GroupCategoryId'
            table = 'ContactGroup'
            returnFields = ['GroupCategoryId', 'GroupDescription', 'GroupName', 'Id']
            query = {'Id' : '%'} # using place holder to get all tag Id
            limit = 1000
            page = x
            query_result =  infusionsoft.DataService('query', table, limit, page, query, returnFields)

            # print len(query_result)
            # filter tags that belong to category 182
            # print query_result
            for item in query_result:
                if(item['GroupCategoryId'] == categoryId):  # saving 182 category
                    tag_list.append(item)

            self.category_Id = categoryId
            self.tag_list = tag_list


import re

test = TagsOfCategory(232)

# print test.tag_list

regex_1 = r"\d\d\d\d\s\d\d"
regex_2 = r"\d\d\d\d\-\d\d"


x = 0

from datetime import datetime,timedelta
current_date=datetime.now()
currQuarter = (current_date.month - 1) / 3 + 1
dtFirstDay = datetime(current_date.year, 3 * currQuarter - 2, 1)
dtLastDay = datetime(current_date.year, 3 * currQuarter + 1, 1) + timedelta(days=-1)

current_quarter_first_date = dtFirstDay
current_date.replace(month=current_date.month + 3)
next_quarter_first_date = datetime(current_date.year, 3 * 2 - 2, 1)
next_quarter_first_date.replace(month=current_date.month + 3)
quarter_after_next = datetime(next_quarter_first_date.year, 3 * 3 - 2, 1)


#

print current_quarter_first_date
print next_quarter_first_date
print quarter_after_next
# print dtLastDay


#
# for item in test.tag_list:
#     # print item['GroupName'].find("[ORIENTATION]")
#
#     if((item['GroupName'].find("[ORIENTATION]") != -1) and (item['GroupName'].find("PAID") != -1)):
#         # print item
#         # x+=1
#
#         date2 = re.search(regex_2, item['GroupName'])
#         date1 = re.search(regex_1, item['GroupName'])
#         if(date2 != None):
#             print date2.group(0)
#         if(date1 != None):
#             print date1.group(0)
#
#
#
#
#
#
#     # print item
#
#
# print len(test.tag_list)
# print x