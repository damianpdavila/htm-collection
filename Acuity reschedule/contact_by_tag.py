#GET ALL CONTACTS THAT CONTAIN A SPECIFIC TAG using GroupId parameter passing tha tag Id
class ContactByTag():

    def __init__(self, tagIdList):
        # INFUSIONSOFT API CALL
        # import infusinosoft module
        from infusionsoft import Infusionsoft
        # apiname and key
        infusionsoft = Infusionsoft('education', 'APIKEYHERE')
        # Table to call
        table = 'ContactGroupAssign'
        # returnFields = ['Contact.Address1Type','Contact.Address2Street1','Contact.Address2Street2','Contact.Address2Type','Contact.Address3Street1','Contact.Address3Street2','Contact.Address3Type','Contact.Anniversary','Contact.AssistantName','Contact.AssistantPhone','Contact.BillingInformation','Contact.Birthday','Contact.City','Contact.City2','Contact.City3','Contact.Company','Contact.CompanyID','Contact.ContactNotes','Contact.ContactType','Contact.Country','Contact.Country2','Contact.Country3','Contact.CreatedBy','Contact.DateCreated','Contact.Email','Contact.EmailAddress2','Contact.EmailAddress3','Contact.Fax1','Contact.Fax1Type','Contact.Fax2','Contact.Fax2Type','Contact.FirstName','Contact.Groups','Contact.Id','Contact.JobTitle','Contact.LastName','Contact.LastUpdated','Contact.LastUpdatedBy','Contact.Leadsource','Contact.MiddleName','Contact.Nickname','Contact.OwnerID','Contact.Phone1','Contact.Phone1Ext','Contact.Phone1Type','Contact.Phone2','Contact.Phone2Ext','Contact.Phone2Type','Contact.Phone3','Contact.Phone3Ext','Contact.Phone3Type','Contact.Phone4','Contact.Phone4Ext','Contact.Phone4Type','Contact.Phone5','Contact.Phone5Ext','Contact.Phone5Type','Contact.PostalCode','Contact.PostalCode2','Contact.PostalCode3','Contact.ReferralCode','Contact.SpouseName','Contact.State','Contact.State2','Contact.State3','Contact.StreetAddress1','Contact.StreetAddress2','Contact.Suffix','Contact.Title','Contact.Website','Contact.ZipFour1','Contact.ZipFour2','Contact.ZipFour3','ContactGroup','ContactId','DateCreated','GroupId']
        # returnFields = ['Contact.Id', 'ContactId', 'Contact.FirstName', 'Contact.LastName', 'Contact.Email', 'DateCreated'] # removed (DateCreated is not date created in infusionsoft)
        returnFields = ['Contact.Id', 'ContactId', 'Contact.FirstName', 'Contact.LastName', 'Contact.Email']
        query = {'GroupId': tagIdList[0]}  # 1480 All Paying Members
        limit = 1000
        page = 0
        contact_result = infusionsoft.DataService('query', table, limit, page, query, returnFields)

        self.contact_result = contact_result
        # print len(contact_result)

