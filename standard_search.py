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

	# custom_rings = raw_input("Do you want custom rings? (separate by commas; default is 1, 3, 5): >>> ")
	# if custom_rings:
	# 	rings_list = custom_rings.split(",")
	# 	rings_list = [float(ring.strip()) for ring in rings_list]
	# 	get_df(location, rings=rings_list)
	# else:
	# 	get_df(location)

	retail = [acq.get_value(location, ring=radius, data_type="industrybysiccode.S09_SALES") for radius in [.5, 1]]
	pop = [acq.get_value(location, ring=radius, data_type="KeyUSFacts.TOTPOP_CY") for radius in [1, 2, 3]]
	inc = [acq.get_value(location, ring=radius, data_type="KeyUSFacts.MEDHINC_CY") for radius in [1, 2, 3]]
	# retail = [154119, 317779]
	# pop = [16613, 48506, 94114]
	# inc = [83981, 84487, 89754]
	print
	print "Retail Info".ljust(30, ".") + "Radius .5".rjust(20, ".") + "Radius 1".rjust(20, ".")
	print "Sales".ljust(30, ".") + "{:,}".format(retail[0]).rjust(20, ".") + "{:,}".format(retail[1]).rjust(20, ".")
	print
	print "Demographic Info".ljust(30, ".") + "Radius 1".rjust(20, ".") + "Radius 2".rjust(20, ".") + "Radius 3".rjust(20, ".")
	print "Population Density".ljust(30, ".") + "{:,}".format(pop[0]).rjust(20, ".") + "{:,}".format(pop[1]).rjust(20, ".") + "{:,}".format(pop[2]).rjust(20, ".")
	print "Median Income".ljust(30, ".") + "{:,}".format(inc[0]).rjust(20, ".") + "{:,}".format(inc[1]).rjust(20, ".") + "{:,}".format(inc[2]).rjust(20, ".")
	print
	pyperclip.copy("\n".join(str(x) for x in retail+pop+inc))