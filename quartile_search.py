from esri import Acquisitions
import pyperclip

if __name__ == "__main__":
	acq = Acquisitions()
	location = raw_input("Enter Location (address or latitude/longitude ie 42.151326, -87.850597; to cancel, hit 'control+c'): >>> ")
	try:
		locations_list = location.split(",")
		locations_list = [float(loc.strip()) for loc in locations_list]
		location = locations_list
	except:
		location = location

	radius = int(raw_input("How wide is the radius in miles? (default is 1): >>> "))

	households = [acq.get_value(location, ring=radius, data_type="Policy.HINC75_CY"), 
				  acq.get_value(location, ring=radius, data_type="Policy.HINC100_CY"),
				  acq.get_value(location, ring=radius, data_type="Policy.HINC150_CY"),
				  acq.get_value(location, ring=radius, data_type="Policy.HINC200_CY"),]
	total_households = reduce(lambda x,y: x+y, households)
	avg_household_size = acq.get_value(location, ring=radius, data_type="AtRisk.AVGHHSZ_CY")

	print
	print "HHs > $75K".ljust(30, ".") + "{:,}".format(households[0]).rjust(20, ".")
	print "HHs > $100K".ljust(30, ".") + "{:,}".format(households[1]).rjust(20, ".")
	print "HHs > $150K".ljust(30, ".") + "{:,}".format(households[2]).rjust(20, ".")
	print "HHs > $200K".ljust(30, ".") + "{:,}".format(households[3]).rjust(20, ".")
	print "Total Households over $75K".ljust(30, ".") + "{:,}".format(total_households).rjust(20, ".")
	print
	print "Average Household Size".ljust(30, ".") + "{:,}".format(avg_household_size).rjust(20, ".")
	print
	print "Est. Pop. Density > $75K ".ljust(30, ".") + "{:,}".format(avg_household_size*total_households).rjust(20, ".")
	print
	# pyperclip.copy("\n".join(str(x) for x in retail+pop+inc))