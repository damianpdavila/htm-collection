#GET a specific contact by passing in id
class GetContact():

    def __init__(self, contactId):
        # INFUSIONSOFT API CALL
        # import infusinosoft module
        from infusionsoft import Infusionsoft
        # apiname and key
        infusionsoft = Infusionsoft('education', 'APIKEYHERE')
        # Table to call
        table = 'Contact'
        # returnFields = ['Contact.Address1Type','Contact.Address2Street1','Contact.Address2Street2','Contact.Address2Type','Contact.Address3Street1','Contact.Address3Street2','Contact.Address3Type','Contact.Anniversary','Contact.AssistantName','Contact.AssistantPhone','Contact.BillingInformation','Contact.Birthday','Contact.City','Contact.City2','Contact.City3','Contact.Company','Contact.CompanyID','Contact.ContactNotes','Contact.ContactType','Contact.Country','Contact.Country2','Contact.Country3','Contact.CreatedBy','Contact.DateCreated','Contact.Email','Contact.EmailAddress2','Contact.EmailAddress3','Contact.Fax1','Contact.Fax1Type','Contact.Fax2','Contact.Fax2Type','Contact.FirstName','Contact.Groups','Contact.Id','Contact.JobTitle','Contact.LastName','Contact.LastUpdated','Contact.LastUpdatedBy','Contact.Leadsource','Contact.MiddleName','Contact.Nickname','Contact.OwnerID','Contact.Phone1','Contact.Phone1Ext','Contact.Phone1Type','Contact.Phone2','Contact.Phone2Ext','Contact.Phone2Type','Contact.Phone3','Contact.Phone3Ext','Contact.Phone3Type','Contact.Phone4','Contact.Phone4Ext','Contact.Phone4Type','Contact.Phone5','Contact.Phone5Ext','Contact.Phone5Type','Contact.PostalCode','Contact.PostalCode2','Contact.PostalCode3','Contact.ReferralCode','Contact.SpouseName','Contact.State','Contact.State2','Contact.State3','Contact.StreetAddress1','Contact.StreetAddress2','Contact.Suffix','Contact.Title','Contact.Website','Contact.ZipFour1','Contact.ZipFour2','Contact.ZipFour3','ContactGroup','ContactId','DateCreated','GroupId']
        # returnFields = ['Id', 'ContactId', 'Contact.FirstName', 'Contact.LastName', 'Contact.Email']
        returnFields = ['Id', 'FirstName', 'LastName', 'Email', 'BillingInformation', 'Phone1', 'Username', 'Website',
                        'StreetAddress1', 'StreetAddress2', 'City', 'State', 'PostalCode', '_MP', '_CFO', '_COO',
                        '_MonthlyFee0', '_SubscriptionBillDate', '_ExpirationDate0', '_StartDate0',
                        'Groups', '_Program']  # note: custom fields begin with '_' then field name '_fieldName'
        query = {'Id': contactId}  # 1480 All Paying Members
        limit = 1000
        page = 0
        contact_result = infusionsoft.DataService('query', table, limit, page, query, returnFields)

        self.contact_result = contact_result

        # print contact_result
        # print len(contact_result)

    # [{
    #      'Username': 'mark@astorlawfirm.com',
    #      'City': 'Boca Raton',
    #      'StreetAddress1': '5030 Champion Blvd.',
    #      '_MP': 'Kristen David',
    #      'FirstName': 'Mark',
    #      'StreetAddress2': 'Suite G11-114',
    #      '_StartDate0': < DateTime '20160417T00:00:00'
    #  at 7 f68759e9908 >,
#           'LastName': 'Astor',
#            '_MonthlyFee0': 1500.0,
#            'Phone1': '(561) 212-8956',
    #        '_SubscriptionBillDate': < DateTime'20160515T00:00:00' at 7f68759ed170 >,
    #        'Id': 97966,
    #       'State': 'FL',
#           '_ExpirationDate0': < DateTime
    # '20171115T00:00:00'
    # at
    # 7
    # f68759e9ab8 >,
    # 'Groups': '91,103,176,894,1018,1289,1480,1651,1695,1753,1755,1822,1914,2412,2594,3082,3086,3108,3116,3118,3348,3608,3638,3666,3688,3700,3860,3862,3866,3886,3972,4000,4042,4202,4230,4252,4254,4262,4326,4328,4330,4390,4392,4444,4468,4534,4536,4582,4616,4684,4706,4816,4826,5058,5138,5142',
#            'PostalCode': '33496',
#            'Email': 'mark@astorlawfirm.com'
    # }]