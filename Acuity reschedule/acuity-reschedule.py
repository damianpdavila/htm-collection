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
	#  Add dates in ascending order.  Need minimum 3 dates: next LQM from today, plus 2 previous ones
	LQM_DATES = ("10/19/2018", "1/18/2019", "4/12/2019", "7/19/2019", "10/11/2019", "01/24/2020", "4/24/2020", "7/24/2020", "10/23/2020")

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
#today_date = datetime.datetime(2019, 3, 16)
today_date = datetime.datetime.today()
today_date_string = "" + str(today_date.year) + "-" + str(today_date.month) + "-" + str(today_date.day)

yesterday_date = today_date - datetime.timedelta(hours = 24)
yesterday_date_string = "" + str(yesterday_date.year) + "-" + str(yesterday_date.month) + "-" + str(yesterday_date.day)
# print yesterday_date_string

# # Calculate Sunday this week
# week_start = datetime.datetime(today_date.year, today_date.month, today_date.day, 0, 0, 0) - datetime.timedelta(days=today_date.isoweekday() % 7)
# week_start_string = "" + str(week_start.year) + "-" + str(week_start.month) + "-" + str(week_start.day)
# # week_start_string = "" + str(week_start.year) + "-" + str(week_start.month) + "-9"
# 
# from datetime_periods import period
# import calendar
# 
# 
# 
# start_current_quarter_date = period(today_date, 'quarter')[0]
# end_current_quarter_date = period(today_date, 'quarter')[1]
# 
# # LAST LQM DATE (getting friday when orientation starts)
# last_lqm_date =  calendar.Calendar(4).monthdatescalendar(start_current_quarter_date.year, start_current_quarter_date.month)[3][0]
# # print "last LQM date", last_lqm_date # PRINTING AFTER CONDITION CHECK
# 
# start_next_quarter_date = end_current_quarter_date + datetime.timedelta(seconds = 1)
# # NEXT LQM DATE (getting friday when orientations starts)
# next_lqm_date = calendar.Calendar(4).monthdatescalendar(start_next_quarter_date.year, start_next_quarter_date.month)[3][0]
# # print "next LQM date", next_lqm_date
# 
# 
# # if lastLQMDate is greater than today_date subtract month and recalculate last lqm date and next lqm date TODO
# # print "test comparison", last_lqm_date, start_current_quarter_date
# # print "comparison", last_lqm_date > start_current_quarter_date.date()
# 
# # TODO uncomment below when in month of LQM
# # if last_lqm_date is greater than start_current_quarter_date TODO add to meteor application
# if(last_lqm_date > start_current_quarter_date.date()):
# 	# recalculate last lqm date and start_current_quarter date subtracting a month to start_current_quarter_date
# 	start_current_quarter_date = period((today_date - datetime.timedelta(days = 31)), 'quarter')[0] # subtract 31 days to today date to get the last Lqm Date from previous quarter
# 	end_current_quarter_date = period((today_date - datetime.timedelta(days=31)), 'quarter')[1]  # subtract 31 days to today date to get the last Lqm Date from previous quarter
# 	# print "test quarter ranges: ", start_current_quarter_date, end_current_quarter_date
# 
# 	#  get last_lqm_date (overrite if condition above is met)
# 	last_lqm_date =  calendar.Calendar(4).monthdatescalendar(start_current_quarter_date.year, start_current_quarter_date.month)[3][0]
# 	start_next_quarter_date = end_current_quarter_date + datetime.timedelta(seconds=1)
# 	next_lqm_date = calendar.Calendar(4).monthdatescalendar(start_next_quarter_date.year, start_next_quarter_date.month)[3][0]
# 
# 
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

def getAppointments(start_date, end_date, is_cancelled = False, appt_email = "", first_name = "", last_name = "", appt_phone = ""):
	"""
	Get all active appointments from Acuity calendar that are between two dates.
	Optionally, get only cancelled appointments.

	Parameters: start date (Date), end date (Date), get cancelled appts only (Bool), 
    search by email (string), search by first name or last name (string), search by phone (string)
  """
	
	acuity_user_id = 11403102
	api_key = "11736d22f3b5b3359050f7614ac023f8"

	str_is_cancelled = "&canceled=true" if is_cancelled else ""

	# request = urllib2.Request("https://acuityscheduling.com/api/v1/appointments?max=1000&calendarID=140955&minDate=" + last_lqm_date_string + "&maxDate=" + next_lqm_date_string)
	request = urllib2.Request("https://acuityscheduling.com/api/v1/appointments?max=1000&minDate=" + start_date + "&maxDate=" + end_date + str_is_cancelled + "&firstName=" + first_name + "&lastName=" + last_name + "&email=" + appt_email + "&phone=" + appt_phone)
	base64string = base64.encodestring('%s:%s' % (acuity_user_id, api_key)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)
	result = urllib2.urlopen(request)

	response_string =  result.read()

	return json.loads(response_string)

#  ======= TESTING HERE ===========

response_object = getAppointments("", "", "", "damiand@howtomanage.com", "", "", "")
response_object = getAppointments("", "", "", "DAMIAND@HOWTOMANAGE.COM", "", "", "")
response_object = getAppointments("", "", "", "", "", "", "+19544657537")
response_object = getAppointments("", "", "", "", "", "", "954-465-7537")
response_object = getAppointments("", "", "", "", "", "", "(954)4657537")

exit
#  ======= END TESTING HERE ===========

# QUERY FOR SCHEDULED CALLS BETWEEN LQM AND LQM 

response_object = getAppointments(str(last_lqm_date), str(next_lqm_date))

# TOTAL SCHEDULEED APPOINTMETS BETWEEN LQMs (Not counting 'follow up' and 'New Member Onboarding Call')
total_schedule_appointments_lqm_to_lqm = 0
total_schedule_follow_ups_lqm_to_lqm = 0
total_schedule_vip_appointments_lqm_to_lqm = 0

for item in response_object:
    if(item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
        total_schedule_appointments_lqm_to_lqm += 1
    if(item['calendar'] == 'Follow Up'):
		total_schedule_follow_ups_lqm_to_lqm += 1
    if(item['calendar'] == 'VIP Appointment'):
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
    if(item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
        total_schedule_appointments_lqm_to_yesterday += 1

    if(item['calendar'] == 'Follow Up'):
		total_schedule_follow_ups_lqm_to_yesterday += 1

    if(item['calendar'] == 'VIP Appointment'):
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
    if(item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
        total_schedule_appointments_today_to_LQM += 1

    if(item['calendar'] == 'Follow Up'):
		total_schedule_follow_ups_today_to_LQM += 1

    if(item['calendar'] == 'VIP Appointment'):
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
    if(item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
        total_schedule_appointments_next_two_weeks += 1

    if(item['calendar'] == 'Follow Up'):
		total_schedule_follow_ups_next_two_weeks += 1

    if(item['calendar'] == 'VIP Appointment'):
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
    if(item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
        total_schedule_appointments_month_to_date += 1

    if(item['calendar'] == 'Follow Up'):
		total_schedule_follow_ups_month_to_date += 1

    if(item['calendar'] == 'VIP Appointment'):
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
    if(item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
        total_schedule_appointments_today_to_EOM += 1

    if(item['calendar'] == 'Follow Up'):
		total_schedule_follow_ups_today_to_EOM += 1

    if(item['calendar'] == 'VIP Appointment'):
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
	# print item
	if(item['noShow'] == False and item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
		total_sales_cancelations_LQM_to_LQM += 1
	if(item['noShow'] == True and item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
		total_sales_no_shows_LQM_to_LQM += 1
	if(item['noShow'] == False and item['calendar'] == 'Follow Up'):
		total_follow_ups_cancelations_LQM_to_LQM += 1
	if(item['noShow'] == True and item['calendar'] == 'Follow Up'):
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
	# print item
	if(item['noShow'] == False and item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
		total_sales_cancelations_LQM_to_yesterday += 1
	if(item['noShow'] == True and item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
		total_sales_no_shows_LQM_to_yesterday += 1
	if(item['noShow'] == False and item['calendar'] == 'Follow Up'):
		total_follow_ups_cancelations_LQM_to_yesterday += 1
	if(item['noShow'] == True and item['calendar'] == 'Follow Up'):
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
	# print item
	if(item['noShow'] == False and item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
		total_sales_cancelations_Today_to_LQM += 1
	if(item['noShow'] == True and item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
		total_sales_no_shows_Today_to_LQM += 1
	if(item['noShow'] == False and item['calendar'] == 'Follow Up'):
		total_follow_ups_cancelations_Today_to_LQM += 1
	if(item['noShow'] == True and item['calendar'] == 'Follow Up'):
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
	# print item
	if(item['noShow'] == False and item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
		total_sales_cancelations_next_two_weeks += 1
	if(item['noShow'] == True and item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
		total_sales_no_shows_next_two_weeks += 1
	if(item['noShow'] == False and item['calendar'] == 'Follow Up'):
		total_follow_ups_cancelations_next_two_weeks += 1
	if(item['noShow'] == True and item['calendar'] == 'Follow Up'):
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
	# print item
	if(item['noShow'] == False and item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
		total_sales_cancelations_month_to_date += 1
	if(item['noShow'] == True and item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
		total_sales_no_shows_month_to_date += 1
	if(item['noShow'] == False and item['calendar'] == 'Follow Up'):
		total_follow_ups_cancelations_month_to_date += 1
	if(item['noShow'] == True and item['calendar'] == 'Follow Up'):
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
	# print item
	if(item['noShow'] == False and item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
		total_sales_cancelations_Today_to_EOM += 1
	if(item['noShow'] == True and item['calendar'] != 'Follow Up' and item['calendar'] != 'New Member Onboarding Call'):
		total_sales_no_shows_Today_to_EOM += 1
	if(item['noShow'] == False and item['calendar'] == 'Follow Up'):
		total_follow_ups_cancelations_Today_to_EOM += 1
	if(item['noShow'] == True and item['calendar'] == 'Follow Up'):
		total_follow_ups_no_shows_Today_to_EOM += 1

print "Total Sales Cancelations today to LQM: ", total_sales_cancelations_Today_to_EOM
print "Total No-SHows today to LQM: ", total_sales_no_shows_Today_to_EOM
print "Total follow ups cancelations today to LQM: ", total_follow_ups_cancelations_Today_to_EOM
print "Total follow ups no shows today to LQM: ", total_follow_ups_no_shows_Today_to_EOM



#GET SALES FROM INFUSIONSOFT
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
PAID_ORIENTATION_TAG = 10813  																# TODO make sure to update tag of orientation sold (2 different places)

"""
30Aug2019:  Adding new types of sales into summary section of report 
"""
# Bootcamp sales
# 10385	2019-10-Business Plan Bootcamp - PAID
# 10945 2020-01 - Business Plan Bootcamp - PAID
# -1 TBD
PAID_BOOTCAMP_TAG = 10945

# Law Firm 500 general admission sales
# 10013	2019-10 - LF500 - General Seating (PAID)
# -1 TBD
PAID_LF500_GENERAL_TAG = -1

# Law Firm 500 VIP sales
# 10017	2019-10 - LF500 - VIP Seating (PAID)
# -1 TBD
PAID_LF500_VIP_TAG = -1

# Law Firm 500 gala-only sales
# 10021	2019-10 - LF500 - Gala Only (PAID)
# -1 TBD
PAID_LF500_GALA_ONLY_TAG = -1

#--------------------------------------
# Orientations aka Discovery Day sales
#--------------------------------------
orientations_sold_contacts = ContactByTag([PAID_ORIENTATION_TAG]).contact_result 

print "HERE: ", len(orientations_sold_contacts)
# for x in orientations_sold_contacts:
# 	print x

# TODO add to meteor app script
# 5060 Test account employee TAG
test_acount_members = ContactByTag([5060]).contact_result

# for x in test_acount_members:
# 	print x

print "test ACCOUNTS TO BE REMOVED", len(test_acount_members)
# remove test acounts
orientations_sold_contacts = [member for member in orientations_sold_contacts if member not in test_acount_members]


# for contact in orientations_sold_contacts:
#   print contact

# print len(orientations_sold_contacts)

orientations_sold = len(orientations_sold_contacts)

print "total orientations sold for the current tag (" + str(PAID_ORIENTATION_TAG) +  "): " + str(orientations_sold)  #TODO update string for the correct tag


#--------------------------------------
# Bootcamp sales
#--------------------------------------
bootcamp_sold_contacts = ContactByTag([PAID_BOOTCAMP_TAG]).contact_result 

bootcamp_sold_contacts = [member for member in bootcamp_sold_contacts if member not in test_acount_members]

bootcamps_sold = len(bootcamp_sold_contacts)

print "total bootcamps sold for the current tag (" + str(PAID_BOOTCAMP_TAG) +  "): " + str(bootcamps_sold)  #TODO update string for the correct tag


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