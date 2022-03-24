#import division to keep floating point numbers
from __future__ import division
from AppointmentsAndSalesNumbers import *

from datetime import datetime
# functionto find differnece of days
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)




days_since_last_LQM = days_between(str(last_lqm_date), yesterday_date_string)
print "days since last LQM:", days_since_last_LQM

days_until_next_LQM = days_between(today_date_string, str(next_lqm_date))
print "days until next LQM:", days_until_next_LQM


# days_since_beginning_of_year = days_between(year_start_date_string, today_date_string)
# print "days since the beginning of the year: ", days_since_beginning_of_year

# days_until_end_of_year = days_between(today_date_string, year_end_date_string)
# print "days left until the end of the year: ", days_until_end_of_year



# Current Conversion rate
print "orientations Sold:", orientations_sold, "Scheduled appointments LQM to Yesterday:", total_schedule_appointments_lqm_to_yesterday
print "Orientation Sold after last LQM:", orientations_sold_after_last_lqm

current_conversion_rate_is_default_notice = ""
try:
	current_conversion_rate = (orientations_sold_after_last_lqm / total_schedule_appointments_lqm_to_yesterday) * 100
except ZeroDivisionError:
	current_conversion_rate = 30.00
	current_conversion_rate_is_default_notice = "NOTE: unable to calculate conversion rate; using a default value instead."

#round answer
current_conversion_rate = round(current_conversion_rate, 2)
if (current_conversion_rate <= 0):
	current_conversion_rate = 30.00
	current_conversion_rate_is_default_notice = "NOTE: actual conversion rate = 0; using a default value instead."

print "Current Conversion Rate: ", current_conversion_rate


projected_orientations_sold_from_now_to_LQM = total_schedule_appointments_today_to_LQM * (current_conversion_rate / 100)
projected_orientations_sold_from_now_to_LQM = round(projected_orientations_sold_from_now_to_LQM, 2)
print "Projected_orientations_sold_from_now_to_LQM: ", projected_orientations_sold_from_now_to_LQM

projected_orientations_sold_from_now_to_EOM = total_schedule_appointments_today_to_EOM * (current_conversion_rate / 100)
projected_orientations_sold_from_now_to_EOM = round(projected_orientations_sold_from_now_to_EOM, 2)
print "projected_orientations_sold_from_now_to_EOM: ", projected_orientations_sold_from_now_to_EOM


# Create Object to pass into collection
appointments_sales_calculations_and_numbers = {'entryDate':str(today_date) , 'yesterday_date':str(yesterday_date),\
											   'days_since_last_LQM':days_since_last_LQM, 'days_until_next_LQM':days_until_next_LQM,\
#											   'days_since_beginning_of_year':days_since_beginning_of_year, 'days_until_end_of_year':days_until_end_of_year,\
											   'last_lqm_date':str(last_lqm_date), 'next_lqm_date':str(next_lqm_date),\
#											   'year_start_date':str(year_start_date), 'year_end_date':str(year_end_date),\
											   'total_schedule_appointments_lqm_to_lqm':total_schedule_appointments_lqm_to_lqm,	'total_schedule_follow_ups_lqm_to_lqm':total_schedule_follow_ups_lqm_to_lqm,\
											   'total_schedule_appointments_lqm_to_yesterday':total_schedule_appointments_lqm_to_yesterday, 'total_schedule_follow_ups_lqm_to_yesterday':total_schedule_follow_ups_lqm_to_yesterday,\
											   'total_schedule_appointments_today_to_LQM':total_schedule_appointments_today_to_LQM, 'total_schedule_follow_ups_today_to_LQM':total_schedule_follow_ups_today_to_LQM,\
											   'total_sales_cancellations_LQM_to_LQM':total_sales_cancelations_LQM_to_LQM, 'total_sales_no_shows_LQM_to_LQM':total_sales_no_shows_LQM_to_LQM,\
											   'total_follow_ups_cancellations_LQM_to_LQM':total_follow_ups_cancelations_LQM_to_LQM, 'total_follow_ups_no_shows_LQM_to_LQM':total_follow_ups_no_shows_LQM_to_LQM,\
											   'total_sales_cancellations_LQM_to_yesterday':total_sales_cancelations_LQM_to_yesterday, 'total_sales_no_shows_LQM_to_yesterday':total_sales_no_shows_LQM_to_yesterday,\
											   'total_follow_ups_cancellations_LQM_to_yesterday':total_follow_ups_cancelations_LQM_to_yesterday, 'total_follow_ups_no_shows_LQM_to_yesterday':total_follow_ups_no_shows_LQM_to_yesterday,\
											   'total_sales_cancellations_Today_to_LQM':total_sales_cancelations_Today_to_LQM, 'total_sales_no_shows_Today_to_LQM':total_sales_no_shows_Today_to_LQM,\
											   'total_follow_ups_cancellations_Today_to_LQM':total_follow_ups_cancelations_Today_to_LQM, 'total_follow_ups_no_shows_Today_to_LQM':total_follow_ups_no_shows_Today_to_LQM,\
											   'orientations_sold':orientations_sold, 'current_number_of_members':current_number_of_members,\
											   'current_conversion_rate':current_conversion_rate, 'projected_orientations_sold_from_now_to_LQM':projected_orientations_sold_from_now_to_LQM}


print appointments_sales_calculations_and_numbers


# make html string to pass into email calculations

goal_bootcamp_sold_month_1 = 75  # TODO change to the desired goal
goal_bootcamp_sold_month_2 = 135  # TODO change to the desired goal

goal_sixmonth_sold_quarter = 75  # TODO change to the desired goal

# TODO GOAL IS HARD CODED FOR THE EMAILS (figure out a way to get it programmatically)
goal_orientations_sold_quarter = 50 # TODO change to the desire goal (some calculations are based on this)
goal_orientations_sold_month = int(goal_orientations_sold_quarter/3)

number_of_calls_needed_to_reach_goal_at_current_conversion_rate =int(round((((goal_orientations_sold_quarter - orientations_sold)/current_conversion_rate)*100), 0))

target_number_of_calls_difference_string = ""
if(number_of_calls_needed_to_reach_goal_at_current_conversion_rate >  total_schedule_appointments_today_to_LQM):
	calls_difference = number_of_calls_needed_to_reach_goal_at_current_conversion_rate - total_schedule_appointments_today_to_LQM
	#compose string with number of calls
	target_number_of_calls_difference_string = "<b style='color:red;'>" + str(calls_difference) + "</b> calls under target."

else:
	calls_difference =  total_schedule_appointments_today_to_LQM - number_of_calls_needed_to_reach_goal_at_current_conversion_rate
	target_number_of_calls_difference_string = "<b style='color:green;'>" + str(calls_difference) + "</b> calls above target."

# Do not account for sales to date for this calculation; it is simply the overall quarterly goal
total_number_of_calls_needed_to_reach_quarter_goal_at_current_conversion_rate =int(round(((goal_orientations_sold_quarter/current_conversion_rate)*100), 0))

addl_number_of_calls_needed_to_reach_quarter_goal = total_number_of_calls_needed_to_reach_quarter_goal_at_current_conversion_rate - total_schedule_appointments_lqm_to_yesterday - total_schedule_appointments_today_to_LQM

days_remaining_in_quarter = days_until_next_LQM
if (days_remaining_in_quarter != 0):
	avg_daily_appointments_to_schedule_by_quarter_end = int(round(addl_number_of_calls_needed_to_reach_quarter_goal / days_remaining_in_quarter, 0))
else:
	avg_daily_appointments_to_schedule_by_quarter_end = 0


# Do not account for sales to date for this calculation; it is simply the quarterly goal divided evenly over 3 months
total_number_of_calls_needed_to_reach_month_goal_at_current_conversion_rate = int(round((((goal_orientations_sold_month)/current_conversion_rate)*100), 0))

addl_number_of_calls_needed_to_reach_month_goal = total_number_of_calls_needed_to_reach_month_goal_at_current_conversion_rate - total_schedule_appointments_month_to_date - total_schedule_appointments_today_to_EOM

days_remaining_in_month = days_between(today_date_string, str(current_month_end_date))
if (days_remaining_in_month != 0):
	avg_daily_appointments_to_schedule_by_month_end = int(round(addl_number_of_calls_needed_to_reach_month_goal / days_remaining_in_month, 0))
else:
	avg_daily_appointments_to_schedule_by_month_end = 0


addl_number_of_calls_needed_to_reach_month_goal_message = ""
if (addl_number_of_calls_needed_to_reach_month_goal > 0):
	addl_number_of_calls_needed_to_reach_month_goal_message = "<em> * <span style='font-weight: bold; color: red;'>" + str(addl_number_of_calls_needed_to_reach_month_goal) + "</span>"\
		" calls <span style='color: red;'>under</span> target. Need to add " + str(avg_daily_appointments_to_schedule_by_month_end) + " appt/day in next <strong>" + str(days_remaining_in_month) + "</strong> days to reach goal.</em>"
else:
	addl_number_of_calls_needed_to_reach_month_goal_message = "<em> * <span style='font-weight: bold; color: darkgreen;'>" + str(abs(addl_number_of_calls_needed_to_reach_month_goal)) + "</span>"\
		" calls <span style='color: darkgreen;'>at or over</span> target, based on current conversion rate</em>"

addl_number_of_calls_needed_to_reach_quarter_goal_message = ""
if (addl_number_of_calls_needed_to_reach_quarter_goal > 0):
	addl_number_of_calls_needed_to_reach_quarter_goal_message = "<em> ** <span style='font-weight: bold; color: red;'>" + str(addl_number_of_calls_needed_to_reach_quarter_goal) + "</span>"\
		" calls <span style='color: red;'>under</span> target. Need to add " + str(avg_daily_appointments_to_schedule_by_quarter_end) + " appt/day in next <strong>" + str(days_remaining_in_quarter) + "</strong> days to reach goal.</em>"
else:
	addl_number_of_calls_needed_to_reach_quarter_goal_message = "<em> * <span style='font-weight: bold; color: darkgreen;'>" + str(abs(addl_number_of_calls_needed_to_reach_quarter_goal)) + "</span>"\
		" calls <span style='color: darkgreen;'>at or over</span> target, based on current conversion rate</em>"

calculations_string = \
	"There are  <strong>" + str(days_until_next_LQM) + "</strong> days left until next LQM on " + next_lqm_date_string + ". <br>" \
	+ "Our Goal is to sell <strong>" + str(goal_orientations_sold_quarter) + "</strong> orientations before next LQM<br>"\
	+ "\nOrientations sold = <strong>" + str(orientations_sold) + "</strong><br><br>" \
	+ "\n\nCurrent conversion rate = <strong>" + str(current_conversion_rate) + "%." + "</strong>  <em>" + current_conversion_rate_is_default_notice + "</em>"\
	+ "<br>To meet our goal there should be <strong>" + str(number_of_calls_needed_to_reach_goal_at_current_conversion_rate) + "</strong> sales calls scheduled from today until the next LQM."\
	+ "<br># of sales calls scheduled Quarter to Date = <strong>" + str(total_schedule_appointments_lqm_to_yesterday) + "</strong>"\
	+ "<br># of sales calls scheduled this month = <strong>" + str(total_schedule_appointments_month_to_date + total_schedule_appointments_today_to_EOM) + "</strong>"\
	+ "<br># of sales calls scheduled in next 2 weeks = <strong>" + str(total_schedule_appointments_next_two_weeks) + "</strong>"\
	+ "<br>Currently projected to sell <strong>" + str(int(orientations_sold_after_month_start + projected_orientations_sold_from_now_to_EOM)) + "</strong> Discovery Days this month</strong>" \
	+ "<br>Total # of sales calls needed to fulfill this month in order to meet our goal = <strong>" + str(total_number_of_calls_needed_to_reach_month_goal_at_current_conversion_rate) + "</strong>"\
	+ "<br>We currently have <strong>" + str(total_schedule_appointments_today_to_LQM) + "</strong> sales calls scheduled from today to next LQM, and are " + target_number_of_calls_difference_string\
	+ "<br>We are currently on track to sell <strong>" + str(int(projected_orientations_sold_from_now_to_LQM)) + "</strong> orientations."\
	+ " With a total of <strong>" + str(int(projected_orientations_sold_from_now_to_LQM + orientations_sold)) + "</strong> orientations sold by LQM."\
	+ "<br>Additional appointments required to hit MONTHLY sales target: <strong>" + str(addl_number_of_calls_needed_to_reach_month_goal) + "</strong> "\
	+ "in next <strong>" + str(days_remaining_in_month) + "</strong> days (" + str(avg_daily_appointments_to_schedule_by_month_end) + " appt/day)"\
	+ "<br><br> Follow ups from last LQM to yesterday: <strong>" + str(total_schedule_follow_ups_lqm_to_yesterday) + "</strong>"\
	+ "<br> Follow ups from today to LQM: <strong>" + str(total_schedule_follow_ups_today_to_LQM) + "</strong>" \
	+ "<br><br> VIP Appointments from last LQM to yesterday: <strong>" + str(total_schedule_vip_appointment_lqm_to_yesterday) + "</strong>" \
	+ "<br> VIP Appointments from today to LQM: <strong>" + str(total_schedule_vip_appointments_today_to_LQM) + "</strong>"

member_sales_detail = ""
for program_idx, program in enumerate(MEMBER_SALES_META):
	if ( program['tag'] > -1):
	    member_sales_detail += "\n" + program['label'] + ": <strong>" + str(program['count']) + "</strong><br>"

member_sales_detail += "\n" + "SLFU paid, pending contract" + ": <strong>" + str(member_program_paid) + "</strong><br>"

#bootcamp_group_1C =	"\n<br/>" if bootcamp_participants_1_C == 0 else "\nGroup C (" + NEXT_BOOTCAMP_1_DATE_GROUP_C + ") participants: <strong>" + str(bootcamp_participants_1_C) + "</strong> <span style='font-size: smaller; font-weight: normal;'>(" + str(bootcamp_rollovers_1_C) + " rollover)</span><br>"
#bootcamp_group_2C =	"\n<br/>" if bootcamp_participants_2_C == 0 else "\nGroup C (" + NEXT_BOOTCAMP_2_DATE_GROUP_C + ") participants: <strong>" + str(bootcamp_participants_2_C) + "</strong> <span style='font-size: smaller; font-weight: normal;'>(" + str(bootcamp_rollovers_2_C) + " rollover)</span><br>"

# May 2021:  all bootcamp sales going into May paid tag only.  To avoid confusion, hide the monthly sales
#    + "\n<p><span style='font-size: smaller; font-weight: normal;'>(Total Participants = Sold - Postponed + Rollover)</span></p>"\
#bootcamp_sold_1_lit = "\nSold: <strong>" + str(bootcamps_sold_1) + "</strong><br>"
bootcamp_sold_1_lit = ""
#bootcamp_sold_2_lit = "\nSold: <strong>" + str(bootcamps_sold_2) + "</strong><br>"
bootcamp_sold_2_lit = ""
# also, postponed do not make sense for month 2 since all sales only into month 1
#bootcamp_postponed_2_lit = "\nPostponed: <strong>" + str(bootcamps_postponed_2) + "</strong><br>"
bootcamp_postponed_2_lit = ""

email_header = \
	"<style>body { color: #000c; font-family: 'Courier New', monospace;}" \
	+ "td { width: 4em; padding: 5px 10px 5px 10px; text-align: center;}"\
	+ "th { vertical-align: bottom; }"\
	+ "H4 { margin-bottom: 1px; }"\
	+ "</style>"\
	+ "There are  <strong>" + str(days_until_next_LQM) + "</strong> days left until next LQM on " + next_lqm_date_string + ". <br>"

bootcamp_section = \
    "<h3><u>Bootcamp Sales</u></h3>"\
	+ "\n<p><strong>Total Bootcamp Sales: " + str(bootcamps_sold_1 + bootcamps_sold_2) + "</strong><br/>"\
	+ "\n - Postponed: <strong>" + str(bootcamps_postponed_1) + "</strong><br>"\
	+ "\n + Total rollover: <strong>" + str(bootcamp_rollovers_1_A + bootcamp_rollovers_1_B + bootcamp_rollovers_1_C + bootcamp_rollovers_2_A + bootcamp_rollovers_2_B + bootcamp_rollovers_2_C + bootcamp_rollovers_2_D + bootcamp_rollovers_2_E) + "</strong><br>"\
	+ "\n = <strong>Total Participants: " + str(bootcamp_participants_1_A + bootcamp_participants_1_B + bootcamp_participants_1_C + bootcamp_participants_2_A + bootcamp_participants_2_B + bootcamp_participants_2_C + bootcamp_participants_2_D + bootcamp_participants_2_E) + "</strong><br>"\
	+ "</p>"\
	+ "\n<p><strong>" + NEXT_BOOTCAMP_1_DATE + " Bootcamp</strong></p>"\
	+ "\nGoal: " + str(goal_bootcamp_sold_month_1) + "<br>"\
	+ bootcamp_sold_1_lit\
	+ "\nRollovers: <strong>" + str(bootcamp_rollovers_1_A + bootcamp_rollovers_1_B + bootcamp_rollovers_1_C) + "</strong><br>"\
	+ "\nParticipants: <strong>" + str(bootcamp_participants_1_A + bootcamp_participants_1_B + bootcamp_participants_1_C) + "</strong><br>"\
	+ "\nGroup A (" + NEXT_BOOTCAMP_1_DATE_GROUP_A + ") participants: <strong>" + str(bootcamp_participants_1_A) + "</strong> <span style='font-size: smaller; font-weight: normal;'>(" + str(bootcamp_rollovers_1_A) + " rollover)</span><br>"\
	+ "\nGroup B (" + NEXT_BOOTCAMP_1_DATE_GROUP_B + ") participants: <strong>" + str(bootcamp_participants_1_B) + "</strong> <span style='font-size: smaller; font-weight: normal;'>(" + str(bootcamp_rollovers_1_B) + " rollover)</span><br>"\
	+ "\nGroup C (" + NEXT_BOOTCAMP_1_DATE_GROUP_C + ") participants: <strong>" + str(bootcamp_participants_1_C) + "</strong> <span style='font-size: smaller; font-weight: normal;'>(" + str(bootcamp_rollovers_1_C) + " rollover)</span><br>"
	# Not used in Sep 2021
	# + "\n<p><strong>" + NEXT_BOOTCAMP_2_DATE + " Bootcamp</strong></p>"\
	# + "\nGoal: " + str(goal_bootcamp_sold_month_2) + "<br>"\
	# + bootcamp_sold_2_lit\
	# + bootcamp_postponed_2_lit\
	# + "\nRollovers: <strong>" + str(bootcamp_rollovers_2_A + bootcamp_rollovers_2_B + bootcamp_rollovers_2_C + bootcamp_rollovers_2_D + bootcamp_rollovers_2_E) + "</strong><br>"\
	# + "\nParticipants: <strong>" + str(bootcamp_participants_2_A + bootcamp_participants_2_B + bootcamp_participants_2_C + bootcamp_participants_2_D + bootcamp_participants_2_E) + "</strong><br>"\
	# + "\nGroup A (" + NEXT_BOOTCAMP_2_DATE_GROUP_A + ") participants: <strong>" + str(bootcamp_participants_2_A) + "</strong> <span style='font-size: smaller; font-weight: normal;'>(" + str(bootcamp_rollovers_2_A) + " rollover)</span><br>"\
	# + "\nGroup B (" + NEXT_BOOTCAMP_2_DATE_GROUP_B + ") participants: <strong>" + str(bootcamp_participants_2_B) + "</strong> <span style='font-size: smaller; font-weight: normal;'>(" + str(bootcamp_rollovers_2_B) + " rollover)</span><br>"\
	# + "\nGroup C (" + NEXT_BOOTCAMP_2_DATE_GROUP_C + ") participants: <strong>" + str(bootcamp_participants_2_C) + "</strong> <span style='font-size: smaller; font-weight: normal;'>(" + str(bootcamp_rollovers_2_C) + " rollover)</span><br>"\
	# + "\nGroup D (" + NEXT_BOOTCAMP_2_DATE_GROUP_D + ") participants: <strong>" + str(bootcamp_participants_2_D) + "</strong> <span style='font-size: smaller; font-weight: normal;'>(" + str(bootcamp_rollovers_2_D) + " rollover)</span><br>"\
	# + "\nGroup E (" + NEXT_BOOTCAMP_2_DATE_GROUP_E + ") participants: <strong>" + str(bootcamp_participants_2_E) + "</strong> <span style='font-size: smaller; font-weight: normal;'>(" + str(bootcamp_rollovers_2_E) + " rollover)</span><br>"

member_sales_section = \
	"<h3><u>Member Sales</u> <span style='font-size: smaller; font-weight: normal;'> (Cohort: " + NEXT_MEMBER_COHORT_DATE + ")</span></h3>" \
	+ "\nMember Sales Goal: " + str(goal_sixmonth_sold_quarter) + "<br>"\
	+ "<p></p>"\
	+ member_sales_detail\
	+ "\n<p><strong>Total Member Sales: " + str(member_program_sold) + "</strong></p>"
	# Remove until used again
	# + "<h3>Law Firm 500</h3>" \
	# + "\nLF500 Livestream sold: <strong>" + str(lf500_general_sold) + "</strong><br>"\
	# + "\nLaw Firm 500 VIP sold = <strong>" + str(lf500_vip_sold) + "</strong><br>"\
	# + "\nLaw Firm 500 gala-only sold = <strong>" + str(lf500_gala_only_sold) + "</strong><br>"\

discovery_day_sales_section = \
	"<h3><u>Discovery Day Sales</u></h3>" \
	+ "<p>Sold: <strong>" + str(orientations_sold) + "</strong><br>"
	#+ "Goal: <strong>" + str(goal_orientations_sold_quarter) + "</strong><br>"\

bootcamp_rsvp_section = \
	"<h3><u>Bootcamp Bonus Day RSVP</u></h3>" \
	+ "<p>RSVPs: <strong>" + str(bootcamp_rsvp) + "</strong><br>"

sales_total_section = \
	"<br/>"\
	+ "<h3><strong>Total Sales: " + str(orientations_sold + bootcamps_sold_1 + bootcamps_sold_2 + lf500_general_sold + lf500_vip_sold + lf500_gala_only_sold + member_program_sold) + "</strong></h3><br><br>"

summary_table_monthly = \
	"<h4>Current Month</h4> <span>(" + current_month_start_date_str + " to " + current_month_end_date_str + ")</span>"\
	+ "<table><tr><th> </th><th>Sales</th><th>Sched<br>Calls</th></tr>"\
	+ "<tr style='background-color: lightgrey;'>"\
	+ "<td style='width: 7em; text-align: left;'>Goal</td>"\
	+ "<td>" + str(goal_orientations_sold_month) + "</td>"\
	+ "<td>" + str(total_number_of_calls_needed_to_reach_month_goal_at_current_conversion_rate) + "</td>"\
	+ "</tr>"\
	+ "<tr>"\
	+ "<td style='width: 7em; text-align: left;'>Actual MTD</td>"\
	+ "<td>" + str(orientations_sold_after_month_start) + "</td>"\
	+ "<td>" + str(total_schedule_appointments_month_to_date) + "</td>"\
	+ "</tr>"\
	+ "<tr style='background-color: lightgrey;'>"\
	+ "<td style='width: 7em; text-align: left;'>Today to EOM</td>"\
	+ "<td> -  </td>"\
	+ "<td>" + str(total_schedule_appointments_today_to_EOM) + "</td>"\
	+ "</tr>"\
	+ "<tr>"\
	+ "<td style='width: 7em; text-align: left;'>Projected</td>"\
	+ "<td>" + str(int(orientations_sold_after_month_start + projected_orientations_sold_from_now_to_EOM)) + "</td>"\
	+ "<td>*</td>"\
	+ "</tr></table>"\
	+ "<p>" + addl_number_of_calls_needed_to_reach_month_goal_message + "</p>"

summary_table_quarterly = \
	"<h2>Discovery Day Detailed Projections</h2>"\
	+ "<h4>Quarter Ending " + next_lqm_date_string + "</h4>"\
	+ "<table><tr><th> </th><th>Sales</th><th>Sched<br>Calls</th></tr>"\
	+ "<tr style='background-color: lightgrey;'>"\
	+ "<td style='width: 7em; text-align: left;'>Goal</td>"\
	+ "<td>" + str(goal_orientations_sold_quarter) + "</td>"\
	+ "<td>" + str(total_number_of_calls_needed_to_reach_quarter_goal_at_current_conversion_rate) + "</td>"\
	+ "</tr>"\
	+ "<tr>"\
	+ "<td style='width: 7em; text-align: left;'>Actual QTD</td>"\
	+ "<td>" + str(orientations_sold_after_last_lqm) + "</td>"\
	+ "<td>" + str(total_schedule_appointments_lqm_to_yesterday) + "</td>"\
	+ "</tr>"\
	+ "<tr style='background-color: lightgrey;'>"\
	+ "<td style='width: 7em; text-align: left;'>Today to EOQ</td>"\
	+ "<td> -  </td>"\
	+ "<td>" + str(total_schedule_appointments_today_to_LQM) + "</td>"\
	+ "</tr>"\
	+ "<tr>"\
	+ "<td style='width: 7em; text-align: left;'>Projected</td>"\
	+ "<td>" + str(int(orientations_sold_after_last_lqm + projected_orientations_sold_from_now_to_LQM)) + "</td>"\
	+ "<td>**</td>"\
	+ "</tr></table>"\
	+ "<p>" + addl_number_of_calls_needed_to_reach_quarter_goal_message + "</p>"

#	"<p>Current conversion rate = <strong>" + str(current_conversion_rate) + "%.</strong>  <em>" + current_conversion_rate_is_default_notice + "</em>"\
appointments_section = \
	"Report as of " + report_date_str\
	+ "<p># of sales calls scheduled in next 2 weeks = <strong>" + str(total_schedule_appointments_next_two_weeks) + "</strong></p>"\
	+ "<p>Follow ups from last LQM to yesterday: <strong>" + str(total_schedule_follow_ups_lqm_to_yesterday) + "</strong>"\
	+ "<br>Follow ups from today to LQM: <strong>" + str(total_schedule_follow_ups_today_to_LQM) + "</strong></p>"\
	+ "<p>VIP Appointments from last LQM to yesterday: <strong>" + str(total_schedule_vip_appointment_lqm_to_yesterday) + "</strong> "\
	+ "<br>VIP Appointments from today to LQM: <strong>" + str(total_schedule_vip_appointments_today_to_LQM) + "</strong></p>"

# Text to be displayed at top of email during the specified dates (YYYY, MM, DD);  useful for temporary announcements 
announcement_date_start = datetime(2019, 5, 3)
announcement_date_end = datetime(2019, 5, 3)
announcement_header = ""

if ( today_date >= announcement_date_start and today_date <= announcement_date_end ):
	announcement_header = \
		"<p><em><strong>NOTICE:</strong> The Sales Appointments Report has been updated, including the layout.</em><br>"\
		+ "It's intended to give you a better visual snapshot of progress against goals for the month and quarter.<br>"\
		+ "Please <a href='mailto:damiand@howtomanage.com'>click this link</a> to send any feedback (looks great, I like the old one better, I have ideas...) "\
		+ "to the bot wranglers. Thank you!</a></p><hr>"


# calculations_string =  announcement_header + email_header + summary_table_quarterly + summary_table_monthly + email_detail
calculations_string =  announcement_header + email_header + bootcamp_section + member_sales_section + discovery_day_sales_section + bootcamp_rsvp_section + sales_total_section + appointments_section

# if(goal_scheduled_calls >= total_schedule_appintments_lqm_to_lqm):
#     calculations_string +=  str(abs(int(diff_goal_and_scheduled_calls))) +"</strong> calls under target."
# elif(goal_scheduled_calls < total_schedule_appintments_lqm_to_lqm):
#     calculations_string += str(abs(int(diff_goal_and_scheduled_calls))) + "</strong> calls above target."

# calculations_string = "test string to be sent"

# Disable email sending via command line arg
if (len(sys.argv) > 1 and sys.argv[1].strip() == "nosendemail"):
	no_send_email = True
else:
	no_send_email = False

# Override if you prefer for testing
# no_send_email = True

if (no_send_email):
	print "#########  BEGIN EMAIL CONTENT ############"
	print calculations_string
	print "#########  END EMAIL CONTENT ############"
else:
	# import library to send email
	from send_email import sendEmail

	# sendEmail(['jonathang@howtomanage.com', 'khalilj@howtomanage.com', 'alex@howtomanage.com', 'julianc@howtomanage.com'], "Acuity Test", "Reports/AcuityAPITest.csv")
	# sendEmail(['jonathang@howtomanage.com', 'khalilj@howtomanage.com'], "Sales Appointments Calculations", 'Reports/' + str(today_date.date()) + 'SalesAppointmentsCalculatoins.csv', calculations_string) #TEST
	# sendEmail(['jonathang@howtomanage.com'], "Sales Appointments Calculations", 'Reports/' + str(today_date.date()) + 'SalesAppointmentsCalculatoins.csv', calculations_string) #TEST

	# TODO check on Aprl 20 2017
	# sendEmail(['jonathang@howtomanage.com', 'alex@howtomanage.com', 'stephanieg@howtomanage.com', 'reneer@howtomanage.com', 'andyv@howtomanage.com', 'oscarf@howtomanage.com', 'sherrim@howtomanage.com','damiand@howtomanage.com'], "Sales Appointments Calculations", calculations_string)
	sendEmail(['hbot_sales_report@howtomanage.com'], "Daily Sales Report", calculations_string)
	# sendEmail(['jonathang@howtomanage.com'], "Sales Appointments Calculations", calculations_string)
	
	#sendEmail(['jonathang@howtomanage.com','damiand@howtomanage.com', 'stephanieg@howtomanage.com'], "Sales Appointments Calculations", calculations_string) #TEST	
	#sendEmail(['damiand@howtomanage.com'], "Sales Appointments Calculations", calculations_string) #TEST	

pass
