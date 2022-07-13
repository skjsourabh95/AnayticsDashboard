import time
from apps.map_view  import normal_map_data,  combined_report_data
from common.data    import year_options_max, year_options_min
from common.mapping import race_options
from common.mapping import sex_options
from common.mapping import ethnicity_options
from common.mapping import intent_options
from common.mapping import causes_options
from common.mapping import county_options
from common.mapping import state_options
from common.mapping import map_scale_options
from common.mapping import analytics_options
	
map_scale = ['state','county_fips','region']
year_range_compare_option ='last'
years_base = [None, None]
years_comparison = [None, None]
ages = [0,100]
cause = None
intent = None
ethnicity = None
sex = None
race = None
state = None

# Iterates on all map scale options and all years, to 
# generate cache files for default options, comparing the year with last
entries = 0
total_entries = len(map_scale_options) * (year_options_max - year_options_min)
print("Start caching {} entries.".format(total_entries))
for i in map_scale_options:
	map_scale = i['value']
	for year in range(year_options_min+1,year_options_max):
		start = time.time()
		normal_map_data(map_scale, analytics_options,year,years_base,years_comparison ,ages ,cause,intent,ethnicity,sex,race,state)
		end = time.time()
		entries += 1
		print("Cached {} entries. Last entry cache elapsed: {:.2f} seconds.".format(entries,end - start))


# Caches data for combined report on intent
filter_list = ['intent']
start = time.time()
combined_report_data('state', filter_list,None)
end = time.time()	
print("Cached State Combined Report, took: {:.2f} seconds.".format(end - start))

start = time.time()
combined_report_data('county_fips', filter_list,None)
end = time.time()
print("Cached County Combined Report, took: {:.2f} seconds.".format(end - start))

start = time.time()
combined_report_data('region', filter_list,None)
end = time.time()
print("Cached Region Combined Report, took: {:.2f} seconds.".format(end - start))