import urllib2, base64
import json
import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# GET ALL DATES########################

NEXT_LQM = 0
LAST_LQM = -1
LAST_LAST_LQM = -2

def getLqmDate(current_datetime, index=0):
	"""
	Get LQM date based upon current/target date, and a relative index
	index:  0=next LQM, -1=prev LQM, -2=prev prev LQM

	Parameters: target date (Datetime), index (int)
  	"""
	#  Add dates in ascending order MM/DD/YYYY.  Need minimum 3 dates: next LQM from today, plus 2 previous ones
	LQM_DATES = ("10/23/2020", "01/22/2021", "04/23/2021", "07/23/2021", "10/22/2021", "01/21/2022", "04/22/2022", "07/15/2022", "10/14/2022")

	if (index < -2 or index > 0):
		raise ValueError('ERROR: index parameter must be 0, -1, or -2')

	# find the current/next LQM
	lqm_date = ''
	for lqm_idx, lqm_date_str in enumerate(LQM_DATES):
		lqm_date = datetime.datetime.strptime(lqm_date_str, "%m/%d/%Y")
		# 
		if (current_datetime <= lqm_date):
			break

	# Ensure the LQM date list is updated
	if (current_datetime > lqm_date):
		raise ValueError("ERROR: the LQM date list in this bot must be updated.")

	# get the requested LQM per the requested index
	lqm_idx += index

	lqm_month, lqm_day, lqm_year = LQM_DATES[lqm_idx].split("/")

	return datetime.date(int(lqm_year), int(lqm_month), int(lqm_day))


def getMonthInQuarter(current_datetime):
	"""
	Return start date and end date of month in quarter, based on date argument.
	Quarter is defined as period between LQMs.
	"""
	lqm_date_last = getLqmDate(current_datetime, LAST_LQM)
	lqm_date_next = getLqmDate(current_datetime, NEXT_LQM)

	month_duration = (lqm_date_next - lqm_date_last) // 3
	month_1_start = lqm_date_last + datetime.timedelta(days = 1)
	month_2_start = month_1_start + month_duration
	month_3_start = month_2_start + month_duration
	month_1_end = month_2_start - datetime.timedelta(days = 1)
	month_2_end = month_3_start - datetime.timedelta(days = 1)
	month_3_end = lqm_date_next

	if (current_datetime.date() < month_2_start):
		month_number = 1
		month_start_date = month_1_start
		month_end_date = month_1_end
	elif (current_datetime.date() < month_3_start):
		month_number = 2
		month_start_date = month_2_start
		month_end_date = month_2_end
	else:
		month_number = 3
		month_start_date = month_3_start
		month_end_date = month_3_end

	return (month_number, month_start_date, month_end_date)

# Testing only
#today_date = datetime.datetime(2020, 5, 13)
today_date = datetime.datetime.today()
today_date_string = "" + str(today_date.year) + "-" + str(today_date.month) + "-" + str(today_date.day)

yesterday_date = today_date - datetime.timedelta(hours = 24)
yesterday_date_string = "" + str(yesterday_date.year) + "-" + str(yesterday_date.month) + "-" + str(yesterday_date.day)
# print yesterday_date_string

# Now using set LQM dates instead of calculated
last_lqm_date = getLqmDate(today_date, LAST_LQM)
next_lqm_date = getLqmDate(today_date, NEXT_LQM)

next_lqm_date_string = datetime.datetime.strftime(next_lqm_date, "%b %d, %Y")

# print "Old calculated start of quarter: ", start_current_quarter_date
# print "Old calculated end of quarter: ", end_current_quarter_date
print "last LQM date", last_lqm_date # PRINTING AFTER CONDITION CHECK
print "next LQM date", next_lqm_date
# TODO add to metero application

# #year date range
# year_start_date = period(today_date, 'year')[0]
# year_start_date_string = ""+str(year_start_date.year) + "-" + str(year_start_date.month) + "-" + str(year_start_date.day)
# year_end_date = period(today_date, 'year')[1]
# year_end_date_string = ""+str(year_end_date.year) + "-" + str(year_end_date.month) + "-" + str(year_end_date.day)

# print "year start", year_start_date, "year end date", year_end_date

date_two_weeks_from_today = datetime.date(today_date.year, today_date.month, today_date.day) + datetime.timedelta(days=14)
print "Two weeks from today: ", date_two_weeks_from_today

current_month_number, current_month_start_date, current_month_end_date = getMonthInQuarter(today_date)
print "Current month number: ", current_month_number
print "Current month start date: ", current_month_start_date
print "Current month end date: ", current_month_end_date

current_month_start_date_str = datetime.datetime.strftime(current_month_start_date, "%b %d")
current_month_end_date_str = datetime.datetime.strftime(current_month_end_date, "%b %d")

report_date_str = datetime.datetime.strftime(today_date, "%b %d, %Y")

# GET ALL DATES###########################

def getAppointments(start_date, end_date, is_cancelled = False):
	"""
	Get all active appointments from Acuity calendar that are between two dates.
	Optionally, get only cancelled appointments.

	Parameters: start date (Date), end date (Date), get cancelled appts only (Bool)
  """
	
	acuity_user_id = 11403102
	api_key = "APIKEYHERE"

	str_is_cancelled = "&canceled=true" if is_cancelled else ""

	# request = urllib2.Request("https://acuityscheduling.com/api/v1/appointments?max=1000&calendarID=140955&minDate=" + last_lqm_date_string + "&maxDate=" + next_lqm_date_string)
	request = urllib2.Request("https://acuityscheduling.com/api/v1/appointments?max=1000&minDate=" + start_date + "&maxDate=" + end_date + str_is_cancelled)
	base64string = base64.encodestring('%s:%s' % (acuity_user_id, api_key)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)
	result = urllib2.urlopen(request)

	response_string =  result.read()

	return json.loads(response_string)

# Appointment type IDs from Acuity; find the ID by looking at the direct scheduling link in Acuity for that appt type
follow_up_type = 730342
new_member_onboarding_call_type = 711181
vip_appointment_type = 8127764

test_type = 12027976                       # Damian test appointment
test_future_planning_call_type = 23935512  # Damian TEST Future Planning Call 
test_appointment_types = [test_type, test_future_planning_call_type]

# Find and remove test accounts; use the test accounts identified by tag in ActiveCampaign
test_tag_id = 724                           # tag name "Test account to exclude from reports and leads"
from ac_contact_by_tag import AcContactByTag
test_email_accounts = AcContactByTag([test_tag_id]).contact_result
test_emails = [test_account['email'].lower() for test_account in test_email_accounts]
#test_emails = ['testerfpclost@moventisusa.com', 'testerz@moventisusa.com', 'testerfpcwon@moventisusa.com', 'test@test.com', 'Test123@test.com']

print "Total test accounts: " + str(len(test_emails))
# QUERY FOR SCHEDULED CALLS BETWEEN LQM AND LQM 

response_object = getAppointments(str(last_lqm_date), str(next_lqm_date))

# TOTAL SCHEDULEED APPOINTMETS BETWEEN LQMs (Not counting 'follow up' and 'New Member Onboarding Call')
total_schedule_appointments_lqm_to_lqm = 0
total_schedule_follow_ups_lqm_to_lqm = 0
total_schedule_vip_appointments_lqm_to_lqm = 0

for item in response_object:
    if ( item['appointmentTypeID'] in test_appointment_types or item['email'].lower() in test_emails):
        print "Test appointment:  (type ID)" + str(item['appointmentTypeID']) + ' (type)' + item['type'] + ' (email)' + item['email'] 
        continue
    if(item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
        total_schedule_appointments_lqm_to_lqm += 1
    if(item['appointmentTypeID'] == follow_up_type):
		total_schedule_follow_ups_lqm_to_lqm += 1
    if(item['appointmentTypeID'] == vip_appointment_type):
        total_schedule_vip_appointments_lqm_to_lqm += 1

print "total LQM to LQM: ", total_schedule_appointments_lqm_to_lqm
print "total Folow Ups LQM to LQM: ", total_schedule_follow_ups_lqm_to_lqm


# QUERY FOR SCHEDULED CALLS BETWEEN last LQM and yesterday

response_object = getAppointments(str(last_lqm_date), yesterday_date_string)

# TOTAL SCHEDULEED APPOINTMETS BETWEEN last LQM and yesterday(Not counting 'follow up' and 'New Member Onboarding Call')
total_schedule_appointments_lqm_to_yesterday = 0
total_schedule_follow_ups_lqm_to_yesterday = 0
total_schedule_vip_appointment_lqm_to_yesterday = 0

for item in response_object:
    if ( item['appointmentTypeID'] in test_appointment_types or item['email'].lower() in test_emails):
        continue

    if(item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
        total_schedule_appointments_lqm_to_yesterday += 1

    if(item['appointmentTypeID'] == follow_up_type):
		total_schedule_follow_ups_lqm_to_yesterday += 1

    if(item['appointmentTypeID'] == vip_appointment_type):
        total_schedule_vip_appointment_lqm_to_yesterday += 1

print "total LQM to yesterday: ", total_schedule_appointments_lqm_to_yesterday
print "total Follow Ups LQM to yesterday: ", total_schedule_follow_ups_lqm_to_yesterday


# QUERY FOR SCHEDULED CALLS BETWEEN Today and next LQM

response_object = getAppointments(today_date_string, str(next_lqm_date))

# TOTAL SCHEDULEED APPOINTMETS BETWEEN LQMs (Not counting 'follow up' and 'New Member Onboarding Call')
total_schedule_appointments_today_to_LQM = 0
total_schedule_follow_ups_today_to_LQM = 0
total_schedule_vip_appointments_today_to_LQM = 0

for item in response_object:
    if ( item['appointmentTypeID'] in test_appointment_types or item['email'].lower() in test_emails):
        continue

    if(item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
        total_schedule_appointments_today_to_LQM += 1

    if(item['appointmentTypeID'] == follow_up_type):
		total_schedule_follow_ups_today_to_LQM += 1

    if(item['appointmentTypeID'] == vip_appointment_type):
        total_schedule_vip_appointments_today_to_LQM += 1

print "total Today to LQM: ", total_schedule_appointments_today_to_LQM
print "total FOLLOW UPS Today to LQM: ", total_schedule_follow_ups_today_to_LQM


# QUERY FOR SCHEDULED CALLS BETWEEN TODAY AND NEXT 2 WEEKS

response_object = getAppointments(today_date_string, str(date_two_weeks_from_today))

# TOTAL SCHEDULEED APPOINTMETS BETWEEN TODAY AND NEXT 2 WEEKS (Not counting 'follow up' and 'New Member Onboarding Call')
total_schedule_appointments_next_two_weeks = 0
total_schedule_follow_ups_next_two_weeks = 0
total_schedule_vip_appointments_next_two_weeks = 0

for item in response_object:
    if ( item['appointmentTypeID'] in test_appointment_types or item['email'].lower() in test_emails):
        continue

    if(item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
        total_schedule_appointments_next_two_weeks += 1

    if(item['appointmentTypeID'] == follow_up_type):
		total_schedule_follow_ups_next_two_weeks += 1

    if(item['appointmentTypeID'] == vip_appointment_type):
        total_schedule_vip_appointments_next_two_weeks += 1

print "total appointments from today to next 2 weeks: ", total_schedule_appointments_next_two_weeks
print "total FOLLOW UPS Today to next 2 weeks: ", total_schedule_follow_ups_next_two_weeks


# QUERY FOR SCHEDULED CALLS MONTH TO DATE

response_object = getAppointments(str(current_month_start_date), yesterday_date_string)

# TOTAL SCHEDULED APPOINTMENTS MTD (Not counting 'follow up' and 'New Member Onboarding Call')
total_schedule_appointments_month_to_date = 0
total_schedule_follow_ups_month_to_date = 0
total_schedule_vip_appointments_month_to_date = 0

for item in response_object:
    if ( item['appointmentTypeID'] in test_appointment_types or item['email'].lower() in test_emails):
        continue

    if(item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
        total_schedule_appointments_month_to_date += 1

    if(item['appointmentTypeID'] == follow_up_type):
		total_schedule_follow_ups_month_to_date += 1

    if(item['appointmentTypeID'] == vip_appointment_type):
        total_schedule_vip_appointments_month_to_date += 1

print "total appointments month_to_date: ", total_schedule_appointments_month_to_date
print "total FOLLOW UPS MTD: ", total_schedule_follow_ups_month_to_date


# QUERY FOR SCHEDULED CALLS BETWEEN Today and END OF MONTH

response_object = getAppointments(today_date_string, str(current_month_end_date))

# TOTAL SCHEDULEED APPOINTMETS BETWEEN TODAY AND END OF MONTH (Not counting 'follow up' and 'New Member Onboarding Call')
total_schedule_appointments_today_to_EOM = 0
total_schedule_follow_ups_today_to_EOM = 0
total_schedule_vip_appointments_today_to_EOM = 0

for item in response_object:
    if ( item['appointmentTypeID'] in test_appointment_types or item['email'].lower() in test_emails):
        continue

    if(item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
        total_schedule_appointments_today_to_EOM += 1

    if(item['appointmentTypeID'] == follow_up_type):
		total_schedule_follow_ups_today_to_EOM += 1

    if(item['appointmentTypeID'] == vip_appointment_type):
        total_schedule_vip_appointments_today_to_EOM += 1

print "total Today to LQM: ", total_schedule_appointments_today_to_EOM
print "total FOLLOW UPS Today to LQM: ", total_schedule_follow_ups_today_to_EOM



# Making API CALL for cancellations and no shows LQM to LQM

response_object = getAppointments(str(last_lqm_date), str(next_lqm_date), is_cancelled = True)

# Total Sales Calls cancelations between LQM to LQM
total_sales_cancelations_LQM_to_LQM = 0
total_sales_no_shows_LQM_to_LQM = 0
total_follow_ups_cancelations_LQM_to_LQM = 0
total_follow_ups_no_shows_LQM_to_LQM = 0

for item in response_object:
    if ( item['appointmentTypeID'] in test_appointment_types or item['email'].lower() in test_emails):
        continue
	# print item
	if(item['noShow'] == False and item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
		total_sales_cancelations_LQM_to_LQM += 1
	if(item['noShow'] == True and item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
		total_sales_no_shows_LQM_to_LQM += 1
	if(item['noShow'] == False and item['appointmentTypeID'] == follow_up_type):
		total_follow_ups_cancelations_LQM_to_LQM += 1
	if(item['noShow'] == True and item['appointmentTypeID'] == follow_up_type):
		total_follow_ups_no_shows_LQM_to_LQM += 1

print "Total Sales Cancelations LQM to LQM: ", total_sales_cancelations_LQM_to_LQM
print "Total No-SHows LQM to LQM: ", total_sales_no_shows_LQM_to_LQM
print "Total follow ups cancelations LQM to LQM: ", total_follow_ups_cancelations_LQM_to_LQM
print "Total follow ups no shows LQM to LQM: ", total_follow_ups_no_shows_LQM_to_LQM


# Making API CALL for cancellations and no shows LQM to yesterday

response_object = getAppointments(str(last_lqm_date), yesterday_date_string, is_cancelled = True)

# Total Sales Calls cancelations between LQM to LQM
total_sales_cancelations_LQM_to_yesterday = 0
total_sales_no_shows_LQM_to_yesterday = 0
total_follow_ups_cancelations_LQM_to_yesterday = 0
total_follow_ups_no_shows_LQM_to_yesterday = 0

for item in response_object:
    if ( item['appointmentTypeID'] in test_appointment_types or item['email'].lower() in test_emails):
        continue
	# print item
	if(item['noShow'] == False and item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
		total_sales_cancelations_LQM_to_yesterday += 1
	if(item['noShow'] == True and item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
		total_sales_no_shows_LQM_to_yesterday += 1
	if(item['noShow'] == False and item['appointmentTypeID'] == follow_up_type):
		total_follow_ups_cancelations_LQM_to_yesterday += 1
	if(item['noShow'] == True and item['appointmentTypeID'] == follow_up_type):
		total_follow_ups_no_shows_LQM_to_yesterday += 1

print "Total Sales Cancelations LQM to yesterday: ", total_sales_cancelations_LQM_to_yesterday
print "Total No-SHows LQM to yesterday: ", total_sales_no_shows_LQM_to_yesterday
print "Total follow ups cancelations LQM to yesterday: ", total_follow_ups_cancelations_LQM_to_yesterday
print "Total follow ups no shows LQM to yesterday: ", total_follow_ups_no_shows_LQM_to_yesterday


# Making API CALL for cancellations and no shows today to next LQM

response_object = getAppointments(today_date_string, str(next_lqm_date), is_cancelled = True)

# Total Sales Calls cancelations between today to LQM
total_sales_cancelations_Today_to_LQM = 0
total_sales_no_shows_Today_to_LQM = 0
total_follow_ups_cancelations_Today_to_LQM = 0
total_follow_ups_no_shows_Today_to_LQM = 0

for item in response_object:
    if ( item['appointmentTypeID'] in test_appointment_types or item['email'].lower() in test_emails):
        continue
	# print item
	if(item['noShow'] == False and item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
		total_sales_cancelations_Today_to_LQM += 1
	if(item['noShow'] == True and item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
		total_sales_no_shows_Today_to_LQM += 1
	if(item['noShow'] == False and item['appointmentTypeID'] == follow_up_type):
		total_follow_ups_cancelations_Today_to_LQM += 1
	if(item['noShow'] == True and item['appointmentTypeID'] == follow_up_type):
		total_follow_ups_no_shows_Today_to_LQM += 1

print "Total Sales Cancelations today to LQM: ", total_sales_cancelations_Today_to_LQM
print "Total No-SHows today to LQM: ", total_sales_no_shows_Today_to_LQM
print "Total follow ups cancelations today to LQM: ", total_follow_ups_cancelations_Today_to_LQM
print "Total follow ups no shows today to LQM: ", total_follow_ups_no_shows_Today_to_LQM


# Making API CALL for cancellations and no shows today to next 2 weeks

response_object = getAppointments(today_date_string, str(date_two_weeks_from_today), is_cancelled = True)

# Total Sales Calls cancelations between today and next 2 weeks
total_sales_cancelations_next_two_weeks = 0
total_sales_no_shows_next_two_weeks = 0
total_follow_ups_cancelations_next_two_weeks = 0
total_follow_ups_no_shows_next_two_weeks = 0

for item in response_object:
    if ( item['appointmentTypeID'] in test_appointment_types or item['email'].lower() in test_emails):
        continue
	# print item
	if(item['noShow'] == False and item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
		total_sales_cancelations_next_two_weeks += 1
	if(item['noShow'] == True and item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
		total_sales_no_shows_next_two_weeks += 1
	if(item['noShow'] == False and item['appointmentTypeID'] == follow_up_type):
		total_follow_ups_cancelations_next_two_weeks += 1
	if(item['noShow'] == True and item['appointmentTypeID'] == follow_up_type):
		total_follow_ups_no_shows_next_two_weeks += 1

print "Total Sales Cancelations today to next 2 weeks: ", total_sales_cancelations_next_two_weeks
print "Total No-SHows today to next 2 weeks: ", total_sales_no_shows_next_two_weeks
print "Total follow ups cancelations today to next 2 weeks: ", total_follow_ups_cancelations_next_two_weeks
print "Total follow ups no shows today to next 2 weeks: ", total_follow_ups_no_shows_next_two_weeks


# Making API CALL for cancellations and no shows MTD

response_object = getAppointments(str(current_month_start_date), yesterday_date_string, is_cancelled = True)

# Total Sales Calls cancelations MTD
total_sales_cancelations_month_to_date = 0
total_sales_no_shows_month_to_date = 0
total_follow_ups_cancelations_month_to_date = 0
total_follow_ups_no_shows_month_to_date = 0

for item in response_object:
    if ( item['appointmentTypeID'] in test_appointment_types or item['email'].lower() in test_emails):
        continue
	# print item
	if(item['noShow'] == False and item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
		total_sales_cancelations_month_to_date += 1
	if(item['noShow'] == True and item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
		total_sales_no_shows_month_to_date += 1
	if(item['noShow'] == False and item['appointmentTypeID'] == follow_up_type):
		total_follow_ups_cancelations_month_to_date += 1
	if(item['noShow'] == True and item['appointmentTypeID'] == follow_up_type):
		total_follow_ups_no_shows_month_to_date += 1

print "Total Sales Cancelations MTD: ", total_sales_cancelations_month_to_date
print "Total No-SHows MTD: ", total_sales_no_shows_month_to_date
print "Total follow ups cancelations MTD: ", total_follow_ups_cancelations_month_to_date
print "Total follow ups no shows MTD: ", total_follow_ups_no_shows_month_to_date


# Making API CALL for cancellations and no shows today to End of Month

response_object = getAppointments(today_date_string, str(current_month_end_date), is_cancelled = True)

# Total Sales Calls cancelations between today to End of Month
total_sales_cancelations_Today_to_EOM = 0
total_sales_no_shows_Today_to_EOM = 0
total_follow_ups_cancelations_Today_to_EOM = 0
total_follow_ups_no_shows_Today_to_EOM = 0

for item in response_object:
    if ( item['appointmentTypeID'] in test_appointment_types or item['email'].lower() in test_emails):
        continue
	# print item
	if(item['noShow'] == False and item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
		total_sales_cancelations_Today_to_EOM += 1
	if(item['noShow'] == True and item['appointmentTypeID'] != follow_up_type and item['appointmentTypeID'] != new_member_onboarding_call_type):
		total_sales_no_shows_Today_to_EOM += 1
	if(item['noShow'] == False and item['appointmentTypeID'] == follow_up_type):
		total_follow_ups_cancelations_Today_to_EOM += 1
	if(item['noShow'] == True and item['appointmentTypeID'] == follow_up_type):
		total_follow_ups_no_shows_Today_to_EOM += 1

print "Total Sales Cancelations today to LQM: ", total_sales_cancelations_Today_to_EOM
print "Total No-SHows today to LQM: ", total_sales_no_shows_Today_to_EOM
print "Total follow ups cancelations today to LQM: ", total_follow_ups_cancelations_Today_to_EOM
print "Total follow ups no shows today to LQM: ", total_follow_ups_no_shows_Today_to_EOM



#GET SALES FROM INFUSIONSOFT

def validate_tag(current_date, tag_and_expiry):
	"""
	Validate whether Infusionsoft tag is still valid to use.
	Uses the LQM date for the tag (passed in the tuple) to determine if still valid.
	Param: (datetime) current_date
			tag_and_expiry(tag id, tag expiration date)
	"""
	if (current_date.date() > datetime.datetime.strptime(tag_and_expiry[1], "%m/%d/%Y").date()):
		return -1
	else:
		return tag_and_expiry[0]

#import contact_by_tag class
from contact_by_tag import ContactByTag
# from get_contact_by_id import GetContact

#LQM orientation paid tag
# 5176  [ORIENTATION] 2017-04 Palm Springs PAID
#5228	[ORIENTATION] 2017-07 NAPLES PAID	LIVE EVENT PROGRAM
# 7350	[ORIENTATION] 2018-07 Orlando FL PAID	LIVE EVENT - [prospect]
# 7660	[ORIENTATION] 2018-10 Lake Las Vegas NV PAID	LIVE EVENT - [prospect]
# 8701	[ORIENTATION-DISCOVERY] 2019-01 - San Antonio - PAID
# 8713	[ORIENTATION-DISCOVERY] 2019-04 - Atlanta - PAID
# 9261  [ORIENTATION-DISCOVERY] 2019-07 - Orlando - PAID
# 9829  [ORIENTATION-DISCOVERY] 2019-10- Vegas - PAID
# 10813 [ORIENTATION-DISCOVERY] 2020-01- Phoenix - PAID
# 10825 [ORIENTATION-DISCOVERY] 2020-04- Braselton - PAID     LIVE EVENT - [prospect]
# 11811	[ORIENTATION-DISCOVERY] 2020-07 - Dallas - PAID
# (covid)
# 14256	LQM 2021-07 - Nashville DISCOVERY Day - PAID	LIVE EVENT - [ORIENTATION-DISCOVERY]	
# 15105 LQM 2021-10 - Seattle DISCOVERY DAY - PAID
tag_and_expiration = (15105, "10/26/2021")
PAID_ORIENTATION_TAG = validate_tag(today_date, tag_and_expiration)


# Bootcamp sales
# 10385	2019-10-Business Plan Bootcamp - PAID
# 10945 2020-01 - Business Plan Bootcamp - PAID
# 11419 2020-04 - Business Plan Bootcamp - PAID
# 11617	2020-04-15 - Business Plan Bootcamp - PAID	LIVE EVENT - [prospect]
# 11777	2020-05 - Business Plan Bootcamp - PAID	LIVE EVENT - [prospect]
# 11940	2020-06 - Business Plan Bootcamp - PAID	LIVE EVENT - [prospect]
# 12182	2020-07 - Business Plan Bootcamp - PAID	LIVE EVENT - [prospect]
# 12370	2020-09 - Business Plan Bootcamp - PAID	LIVE EVENT - [prospect]
# 12676	2020-11 - Business Plan Bootcamp - PAID
# 12692	2021-01 - Business Plan Bootcamp - PAID

""" 
26Jan2021: Now reporting all bootcamps in the quarter (LQM to LQM)
Each bootcamp paid sales reported separately.
Each bootcamp participants by group reported separately.
No need to expire the tag any longer because want to continue to report it until we move to next quarter.
"""

# 13141	2021-02 - Business Plan Bootcamp - PAID
# 13143	2021-02 - Business Plan Bootcamp - Group A
# 13145	2021-02 - Business Plan Bootcamp - Group B
# -
# 13155	2021-03 - Business Plan Bootcamp - PAID
# 13147	2021-03 - Business Plan Bootcamp - Group A
# 13149	2021-03 - Business Plan Bootcamp - Group B
# ---------------
# 13599 2021-05 - Business Plan Bootcamp - PAID
# 13607 2021-05 - Business Plan Bootcamp - Group A
# 13609 2021-05 - Business Plan Bootcamp - Group B
# 13611 2021-05 - Business Plan Bootcamp - Group C
# -
# 13601 2021-06 - Business Plan Bootcamp - PAID
# 13613 2021-06 - Business Plan Bootcamp - Group A
# 13615 2021-06 - Business Plan Bootcamp - Group B
# 13617 2021-06 - Business Plan Bootcamp - Group C
# 14026	2021-06 - Business Plan Bootcamp - Group D
# 14028	2021-06 - Business Plan Bootcamp - Group E
# ---------------
# 14674	2021-09 - Business Plan Bootcamp - PAID
# 14666	2021-09 - Business Plan Bootcamp - Group A
# 14668	2021-09 - Business Plan Bootcamp - Group B

PAID_BOOTCAMP_1_TAG = 14674
NEXT_BOOTCAMP_1_DATE = "09/2021"

BOOTCAMP_1_GROUP_A_TAG = 14666
NEXT_BOOTCAMP_1_DATE_GROUP_A = "09/09/2021"

BOOTCAMP_1_GROUP_B_TAG = 14668
NEXT_BOOTCAMP_1_DATE_GROUP_B = "09/21/2021"

BOOTCAMP_1_GROUP_C_TAG = -1
NEXT_BOOTCAMP_1_DATE_GROUP_C = "TBD"

# -- Q4 2021: No bootcamp in August, only September

PAID_BOOTCAMP_2_TAG = -1
NEXT_BOOTCAMP_2_DATE = "06/2021"

BOOTCAMP_2_GROUP_A_TAG = -1
NEXT_BOOTCAMP_2_DATE_GROUP_A = "06/15/2021"

BOOTCAMP_2_GROUP_B_TAG = -1
NEXT_BOOTCAMP_2_DATE_GROUP_B = "06/15/2021"

BOOTCAMP_2_GROUP_C_TAG = -1
NEXT_BOOTCAMP_2_DATE_GROUP_C = "06/17/2021"

BOOTCAMP_2_GROUP_D_TAG = -1
NEXT_BOOTCAMP_2_DATE_GROUP_D = "06/17/2021"

BOOTCAMP_2_GROUP_E_TAG = -1
NEXT_BOOTCAMP_2_DATE_GROUP_E = "06/17/2021"

# Bootcamp RSVP to Discovery Day
# i.e., bootcampers that RSVP to final session at the LQM
# 14196	LQM 2021-07 - Nashville LIVE - Bootcamp RSVP
# 15048	LQM 2021-10 - Seattle LIVE - Bootcamp - RSVP
tag_and_expiration = (15048, "10/26/2021")
BOOTCAMP_RSVP_TAG = validate_tag(today_date, tag_and_expiration)

# Law Firm 500 general admission sales
# 10013	2019-10 - LF500 - General Seating (PAID)
# 12656	2020-12 - LF500 Awards Live Stream - PAID
tag_and_expiration = (12656, "12/05/2020")
PAID_LF500_GENERAL_TAG = validate_tag(today_date, tag_and_expiration)

# Law Firm 500 VIP sales
# 10017	2019-10 - LF500 - VIP Seating (PAID)
tag_and_expiration = (10017, "10/11/2019")
PAID_LF500_VIP_TAG = validate_tag(today_date, tag_and_expiration)

# Law Firm 500 gala-only sales
# 10021	2019-10 - LF500 - Gala Only (PAID)
tag_and_expiration = (10021, "10/11/2019")
PAID_LF500_GALA_ONLY_TAG = validate_tag(today_date, tag_and_expiration)

"""
14May2020:  Adding '6 month program' into summary section of report.
These are new members that joined from a bootcamp rather than from a Discovery Day.
Since we now can do multiple bootcamps per quarter, need to accumulate all relevant tags.

23Nov2020:  Six Month program was temporary and has ended.  Now it is SLFU and of course Create (C-suite).
For convenience, leaving the variable names unchanged.  Only changing the printed labels/text.

26Jan2021:  Group member programs under Member Sales umbrella and reporting each type of sale individually

"""
# Six Month Program sales
# 11405 2020-04 - Business Plan Bootcamp - IN   LIVE EVENT PROGRAM    
# 11403 2020-05 - Business Plan Bootcamp - IN   LIVE EVENT PROGRAM
# 11962	2020-07 - Business Plan Bootcamp - IN	LIVE EVENT PROGRAM
# 11966	2020-08 - Business Plan Bootcamp - IN	LIVE EVENT PROGRAM
# 12608 2020-10 - NEW Member Signed - IN
# 12612 2020-11 - NEW Member Signed - IN
# 12887	2021-01 - NEW Member Signed - IN

### PAID_SIXMONTH_TAGS = []
### 
### tag_and_expiration = (12887, "01/22/2021") #  use next LQM date
### PAID_SIXMONTH_TAGS.append(validate_tag(today_date, tag_and_expiration))
### # For multiple tags, simply append additional tag entry
### #tag_and_expiration = (12612, "01/22/2021") #  use next LQM date
### #PAID_SIXMONTH_TAGS.append(validate_tag(today_date, tag_and_expiration))
### 
### if (PAID_SIXMONTH_TAGS[0] == -1):
###     NEXT_MEMBER_COHORT_DATE = "TBD"
### else:
###     NEXT_MEMBER_COHORT_DATE = "2021-01"

# Member program sales - Paid and signed the contract
# 13163    2021-01 - NEW Member Signed - IN - [C-Suite 18mo]
# 13161    2021-01 - NEW Member Signed - IN - [C-Suite 6mo]    
# 13159    2021-01 - NEW Member Signed - IN - [SLFU] 
# --
# 13309    2021-02- NEW Member Signed - IN - [C-Suite 18mo]
# 13307    2021-02 - NEW Member Signed - IN - [C-Suite 6mo]
# 13255    2021-02 - NEW Member Signed - IN - [SLFU]
# --
# 13501: 2021-04 - NEW Member Signed - IN - [SLFU]
# 14184	2021-07 - NEW Member Signed - IN
# 14978	2021-10 - NEW Member Signed - IN


CURRENT_MEMBER_COHORT = "10/2021"
NEXT_MEMBER_COHORT_EXPIRATION = "01/22/2022"   # use next LQM date?

MEMBER_SALES_META = [
	{
		'label':'C-Suite 18mo',
		'tag':-1,
		'count':0
	},
	{
		'label':'C-Suite 6mo',
		'tag':-1,
		'count':0
	},
	{
		'label':'SLFU paid and signed',
		'tag':14978,
		'count':0
	}
]
# Currently all programs are grouped by same cohort so using a common expiration.  Tomorrow that may change.
for program_idx, program in enumerate(MEMBER_SALES_META):
    if (validate_tag(today_date, (program['tag'], NEXT_MEMBER_COHORT_EXPIRATION)) == -1):
        program['tag'] = -1

if (MEMBER_SALES_META[0]['tag'] == -1 & MEMBER_SALES_META[1]['tag'] == -1 & MEMBER_SALES_META[2]['tag'] == -1):
    NEXT_MEMBER_COHORT_DATE = "TBD"
else:
    NEXT_MEMBER_COHORT_DATE = CURRENT_MEMBER_COHORT


# Member program sales - Paid only, NOT signed contract yet
# 14194	2021-07 - NEW Member - On the Fence	LIVE EVENT - [ORIENTATION-DISCOVERY]
# 14982	2021-10 - NEW Member Signed - On the Fence

tag_and_expiration = (14982, "01/22/2022")   # use next LQM date?
PAID_MEMBER_NO_CONTRACT_TAG = validate_tag(today_date, tag_and_expiration)

#--------------------------------------
# Orientations aka Discovery Day sales
#--------------------------------------
orientations_sold_contacts = ContactByTag([PAID_ORIENTATION_TAG]).contact_result 

print "HERE: ", len(orientations_sold_contacts)
# for x in orientations_sold_contacts:
# 	print x

# 5060 Test account employee TAG
test_acount_members = ContactByTag([5060]).contact_result
print "test ACCOUNTS TO BE REMOVED", len(test_acount_members)

# remove test acounts
orientations_sold_contacts = [member for member in orientations_sold_contacts if member not in test_acount_members]
orientations_sold = len(orientations_sold_contacts)

print "total orientations sold for the current tag (" + str(PAID_ORIENTATION_TAG) +  "): " + str(orientations_sold)  #TODO update string for the correct tag


#--------------------------------------
# Bootcamp sales
#--------------------------------------
bootcamp_sold_contacts_1 = ContactByTag([PAID_BOOTCAMP_1_TAG]).contact_result 
bootcamp_sold_contacts_1 = [member for member in bootcamp_sold_contacts_1 if member not in test_acount_members]
bootcamps_sold_1 = len(bootcamp_sold_contacts_1)
print "total bootcamps sold for the current tag 1 (" + str(PAID_BOOTCAMP_1_TAG) +  "): " + str(bootcamps_sold_1)  #TODO update string for the correct tag

bootcamp_sold_contacts_2 = ContactByTag([PAID_BOOTCAMP_2_TAG]).contact_result 
bootcamp_sold_contacts_2 = [member for member in bootcamp_sold_contacts_2 if member not in test_acount_members]
bootcamps_sold_2 = len(bootcamp_sold_contacts_2)
print "total bootcamps sold for the current tag 2 (" + str(PAID_BOOTCAMP_2_TAG) +  "): " + str(bootcamps_sold_2)  #TODO update string for the correct tag


#--------------------------------------
# Bootcamp participant counts
#--------------------------------------
bootcamp_participant_contacts_total = []

bootcamp_participant_contacts = ContactByTag([BOOTCAMP_1_GROUP_A_TAG]).contact_result 
bootcamp_participant_contacts = [member for member in bootcamp_participant_contacts if member not in test_acount_members]
bootcamp_participants_1_A = len(bootcamp_participant_contacts)
bootcamp_participant_contacts_total += bootcamp_participant_contacts
# ----- Identify any rollovers; customers who registered and paid for a previous bootcamp but could not attend so have re-scheduled to current one.
bootcamp_rollovers_1_A = len([member for member in bootcamp_participant_contacts if member not in bootcamp_sold_contacts_1])

bootcamp_participant_contacts = ContactByTag([BOOTCAMP_1_GROUP_B_TAG]).contact_result 
bootcamp_participant_contacts = [member for member in bootcamp_participant_contacts if member not in test_acount_members]
bootcamp_participants_1_B = len(bootcamp_participant_contacts)
bootcamp_participant_contacts_total += bootcamp_participant_contacts
# ----- Identify any rollovers; customers who registered and paid for a previous bootcamp but could not attend so have re-scheduled to current one.
bootcamp_rollovers_1_B = len([member for member in bootcamp_participant_contacts if member not in bootcamp_sold_contacts_1])

bootcamp_participant_contacts = ContactByTag([BOOTCAMP_1_GROUP_C_TAG]).contact_result 
bootcamp_participant_contacts = [member for member in bootcamp_participant_contacts if member not in test_acount_members]
bootcamp_participants_1_C = len(bootcamp_participant_contacts)
bootcamp_participant_contacts_total += bootcamp_participant_contacts
# ----- Identify any rollovers; customers who registered and paid for a previous bootcamp but could not attend so have re-scheduled to current one.
bootcamp_rollovers_1_C = len([member for member in bootcamp_participant_contacts if member not in bootcamp_sold_contacts_1])

# Find any purchasers that rescheduled for later date
# As of May 2021, all sales made into month 1 only.  Therefore, postponed changes to "paid month 1, but not participant in month 1 and not in month 2"
#bootcamps_postponed_1 = len([member for member in bootcamp_sold_contacts_1 if member not in bootcamp_participant_contacts_total])
bootcamp_participant_contacts_total_1_2 = bootcamp_participant_contacts_total

bootcamp_participant_contacts_total = []

bootcamp_participant_contacts = ContactByTag([BOOTCAMP_2_GROUP_A_TAG]).contact_result 
bootcamp_participant_contacts = [member for member in bootcamp_participant_contacts if member not in test_acount_members]
bootcamp_participants_2_A = len(bootcamp_participant_contacts)
bootcamp_participant_contacts_total += bootcamp_participant_contacts
# ----- Identify any rollovers; customers who registered and paid for a previous bootcamp but could not attend so have re-scheduled to current one.
# As of June 2021 bootcamp, all sales are made into the first month only. Therefore rollovers should be calculated against first month.
# bootcamp_rollovers_2_A = len([member for member in bootcamp_participant_contacts if member not in bootcamp_sold_contacts_2])
bootcamp_rollovers_2_A = len([member for member in bootcamp_participant_contacts if member not in bootcamp_sold_contacts_1])

bootcamp_participant_contacts = ContactByTag([BOOTCAMP_2_GROUP_B_TAG]).contact_result 
bootcamp_participant_contacts = [member for member in bootcamp_participant_contacts if member not in test_acount_members]
bootcamp_participants_2_B = len(bootcamp_participant_contacts)
bootcamp_participant_contacts_total += bootcamp_participant_contacts
# ----- Identify any rollovers; customers who registered and paid for a previous bootcamp but could not attend so have re-scheduled to current one.
# As of June 2021 bootcamp, all sales are made into the first month only. Therefore rollovers should be calculated against first month.
# bootcamp_rollovers_2_B = len([member for member in bootcamp_participant_contacts if member not in bootcamp_sold_contacts_2])
bootcamp_rollovers_2_B = len([member for member in bootcamp_participant_contacts if member not in bootcamp_sold_contacts_1])

bootcamp_participant_contacts = ContactByTag([BOOTCAMP_2_GROUP_C_TAG]).contact_result 
bootcamp_participant_contacts = [member for member in bootcamp_participant_contacts if member not in test_acount_members]
bootcamp_participants_2_C = len(bootcamp_participant_contacts)
bootcamp_participant_contacts_total += bootcamp_participant_contacts
# ----- Identify any rollovers; customers who registered and paid for a previous bootcamp but could not attend so have re-scheduled to current one.
# As of June 2021 bootcamp, all sales are made into the first month only. Therefore rollovers should be calculated against first month.
# bootcamp_rollovers_2_C = len([member for member in bootcamp_participant_contacts if member not in bootcamp_sold_contacts_2])
bootcamp_rollovers_2_C = len([member for member in bootcamp_participant_contacts if member not in bootcamp_sold_contacts_1])

bootcamp_participant_contacts = ContactByTag([BOOTCAMP_2_GROUP_D_TAG]).contact_result 
bootcamp_participant_contacts = [member for member in bootcamp_participant_contacts if member not in test_acount_members]
bootcamp_participants_2_D = len(bootcamp_participant_contacts)
bootcamp_participant_contacts_total += bootcamp_participant_contacts
# ----- Identify any rollovers; customers who registered and paid for a previous bootcamp but could not attend so have re-scheduled to current one.
# As of June 2021 bootcamp, all sales are made into the first month only. Therefore rollovers should be calculated against first month.
# bootcamp_rollovers_2_D = len([member for member in bootcamp_participant_contacts if member not in bootcamp_sold_contacts_2])
bootcamp_rollovers_2_D = len([member for member in bootcamp_participant_contacts if member not in bootcamp_sold_contacts_1])

bootcamp_participant_contacts = ContactByTag([BOOTCAMP_2_GROUP_E_TAG]).contact_result 
bootcamp_participant_contacts = [member for member in bootcamp_participant_contacts if member not in test_acount_members]
bootcamp_participants_2_E = len(bootcamp_participant_contacts)
bootcamp_participant_contacts_total += bootcamp_participant_contacts
# ----- Identify any rollovers; customers who registered and paid for a previous bootcamp but could not attend so have re-scheduled to current one.
# As of June 2021 bootcamp, all sales are made into the first month only. Therefore rollovers should be calculated against first month.
# bootcamp_rollovers_2_E = len([member for member in bootcamp_participant_contacts if member not in bootcamp_sold_contacts_2])
bootcamp_rollovers_2_E = len([member for member in bootcamp_participant_contacts if member not in bootcamp_sold_contacts_1])

# Find any purchasers that rescheduled for later date
# As of May 2021, all sales made into month 1 only.  Therefore, postponed changes to "paid month 1, but not participant in month 1 and not in month 2"
#bootcamps_postponed_2 = len([member for member in bootcamp_sold_contacts_2 if member not in bootcamp_participant_contacts_total])
bootcamp_participant_contacts_total_1_2 += bootcamp_participant_contacts_total
bootcamps_postponed_1 = len([member for member in bootcamp_sold_contacts_1 if member not in bootcamp_participant_contacts_total_1_2])


#--------------------------------------
# Bootcamp RSVPs to LQM/Discovery Day
#--------------------------------------
bootcamp_rsvp_contacts = ContactByTag([BOOTCAMP_RSVP_TAG]).contact_result 
bootcamp_rsvp_contacts = [member for member in bootcamp_rsvp_contacts if member not in test_acount_members]
bootcamp_rsvp = len(bootcamp_rsvp_contacts)
print "total bootcamp RSVPs for the current tag (" + str(BOOTCAMP_RSVP_TAG) +  "): " + str(bootcamp_rsvp)


#--------------------------------------
# Law Firm 500 general admission sales
#--------------------------------------
lf500_general_sold_contacts = ContactByTag([PAID_LF500_GENERAL_TAG]).contact_result 
lf500_general_sold_contacts = [member for member in lf500_general_sold_contacts if member not in test_acount_members]
lf500_general_sold = len(lf500_general_sold_contacts)
print "total LF500 general sold for the current tag (" + str(PAID_LF500_GENERAL_TAG) +  "): " + str(lf500_general_sold)  #TODO update string for the correct tag


#--------------------------------------
# Law Firm 500 vip sales
#--------------------------------------
lf500_vip_sold_contacts = ContactByTag([PAID_LF500_VIP_TAG]).contact_result 
lf500_vip_sold_contacts = [member for member in lf500_vip_sold_contacts if member not in test_acount_members]
lf500_vip_sold = len(lf500_vip_sold_contacts)
print "total LF500 VIP sold for the current tag (" + str(PAID_LF500_VIP_TAG) +  "): " + str(lf500_vip_sold)  #TODO update string for the correct tag


#--------------------------------------
# Law Firm 500 gala-only sales
#--------------------------------------
lf500_gala_only_sold_contacts = ContactByTag([PAID_LF500_GALA_ONLY_TAG]).contact_result 
lf500_gala_only_sold_contacts = [member for member in lf500_gala_only_sold_contacts if member not in test_acount_members]
lf500_gala_only_sold = len(lf500_gala_only_sold_contacts)
print "total LF500 gala-only sold for the current tag (" + str(PAID_LF500_GALA_ONLY_TAG) +  "): " + str(lf500_gala_only_sold)  #TODO update string for the correct tag


#--------------------------------------
# Member program sales
#--------------------------------------
###for sixmo_idx, SIXMONTH_COHORT_TAG in enumerate(PAID_SIXMONTH_TAGS):
###
###	sixmonth_program_sold_contacts_all = ContactByTag([SIXMONTH_COHORT_TAG]).contact_result 
###
###	sixmonth_program_sold_contacts = [member for member in sixmonth_program_sold_contacts_all if member not in test_acount_members]
###
###	print "total six month program sold for the current tag (" + str(SIXMONTH_COHORT_TAG) +  "): " + str(len(sixmonth_program_sold_contacts))  #TODO update string for the correct tag
###
###	sixmonth_program_sold += len(sixmonth_program_sold_contacts)


member_program_sold = 0

for program_idx, program in enumerate(MEMBER_SALES_META):

	member_program_sold_contacts_all = ContactByTag([program['tag']]).contact_result 

	member_program_sold_contacts = [member for member in member_program_sold_contacts_all if member not in test_acount_members]

	print "total member program sold for the current tag (" + str(program['tag']) +  "): " + str(len(member_program_sold_contacts))  #TODO update string for the correct tag

	program['count'] = len(member_program_sold_contacts)

	member_program_sold += len(member_program_sold_contacts)

	# Save off SLFU memberships for next section
	if ("SLFU" in program['label']):
		member_program_slfu_contacts =  member_program_sold_contacts

#--------------------------------------
# Paid for Membership but not signed contract yet
#--------------------------------------
member_program_paid_contacts = ContactByTag([PAID_MEMBER_NO_CONTRACT_TAG]).contact_result 
member_program_paid_contacts = [member for member in member_program_paid_contacts if member not in test_acount_members]
member_program_paid_contacts = [member for member in member_program_paid_contacts if member not in member_program_slfu_contacts]
member_program_paid = len(member_program_paid_contacts)
print "total member program paid for the current tag (" + str(PAID_MEMBER_NO_CONTRACT_TAG) +  "): " + str(member_program_paid)


#--------------------------------------
# Orientations aka Discovery Day sales breakdown by dates
#--------------------------------------
from contact_by_tag_applied_after_specific_date import ContactByTagAppliedAfterSpecificDate

# oritentations sold after last LQM; actually after the last, last LQM to account for future-scheduled sales (purchase ticket but skipping next one and attending one after that)
orientations_sold_contacts_after_last_lqm =  ContactByTagAppliedAfterSpecificDate([PAID_ORIENTATION_TAG], getLqmDate(today_date, LAST_LAST_LQM)).contact_result # todo make sure to update tag of orientation sold (2 different places)
# remove test accounts
orientations_sold_contacts_after_last_lqm = [member for member in orientations_sold_contacts_after_last_lqm if member not in test_acount_members]
# orientations sold after LQM to make better calculations
orientations_sold_after_last_lqm = len(orientations_sold_contacts_after_last_lqm)

print "Number of Members that paid after last LQM(Orinetations Sold After last LQM):   ", orientations_sold_after_last_lqm
# print orientations_sold_contacts_after_last_lqm


# orientations sold since beginning of month
orientations_sold_contacts_after_month_start =  ContactByTagAppliedAfterSpecificDate([PAID_ORIENTATION_TAG], current_month_start_date).contact_result # todo make sure to update tag of orientation sold (2 different places)
# remove test accounts
orientations_sold_contacts_after_month_start = [member for member in orientations_sold_contacts_after_month_start if member not in test_acount_members]
# orientations sold after LQM to make better calculations
orientations_sold_after_month_start = len(orientations_sold_contacts_after_month_start)

print "Number of Members that paid after start of month(Orinetations Sold After start of month):   ", orientations_sold_after_month_start
print orientations_sold_contacts_after_month_start




# Get the number of members using paying member tags and removing test accounts tag
#1480 current paying members with test accounts
current_members = ContactByTag([1480]).contact_result



# remove test members
current_members_no_tests = [member for member in current_members if member not in test_acount_members]


current_number_of_members = len(current_members_no_tests)
print "current number of members: ", current_number_of_members




# # TODO ITERATE THROUGH CURRENT MEMBERS and get how many are on each program (API takes to lonng)
# #iterate through members to find how many members of each program
# for member in current_members_no_tests:
# 	# query for member information
# 	current_member_info = GetContact(member['ContactId'])
# 	print current_member_info.contact_result
# # TODO ITERATE THROUGH CURRENT MEMBERS and get how many are on each program (API takes to lonng)