import csv
import pandas as pd
import matplotlib.pyplot as plt
import re

def append_zero_to_search_patterns():
    for key in search_patterns:
        search_patterns[key].append(0)

# Enter the name of the Satellite production log file to analyze
input_file = str(input("Enter the name of the Satellite production log file to analyze (e.g. production.log.1):  "))

# Generate pattern
input_date = str(input("Enter date (e.g. 2020-05-10):  "))
search_pattern_prefix = input_date + "T"

search_patterns = {}

hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
minutes_seconds = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
                    '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']

for hour in hours:
    search_pattern_hour = search_pattern_prefix + hour + ':'

    for minute in minutes_seconds:
        search_pattern_minute = search_pattern_hour + minute
        # search_patterns[search_pattern_minute] = 0
        search_patterns[search_pattern_minute] = []
        search_pattern_minute = search_pattern_hour

    search_pattern_prefix = input_date + "T"

# 'Processing by' entries in Satellite's production.log
processing_by_msgs = {'Processing by Katello::Api::V2::RootController#rhsm_resource_list as JSON' : {'input_file.0' : 0},
                      'Processing by Katello::Api::Rhsm::CandlepinProxiesController#serials as JSON' : {'input_file.1' : 0},
                      'Processing by Katello::Api::Rhsm::CandlepinProxiesController#server_status as JSON' : {'input_file.2' : 0},
                      'Processing by Katello::Api::Rhsm::CandlepinProxiesController#consumer_show as JSON' : {'input_file.3' : 0},
                      'Processing by Katello::Api::Rhsm::CandlepinProxiesController#get as JSON' : {'input_file.4' : 0},
                      'Processing by Katello::Api::V2::PingController#index as */*' : {'input_file.5' : 0},
                      'Processing by Katello::Api::V2::PingController#server_status as */*' : {'input_file.6' : 0},
                      'Processing by Katello::Api::Rhsm::CandlepinProxiesController#facts as JSON' : {'input_file.7' : 0},
                      'Processing by UsersController#login as */*' : {'input_file.8' : 0},
                      'Processing by Api::V2::HomeController#status as JSON' : {'input_file.9' : 0},
                      'Processing by Katello::Api::Rhsm::CandlepinProxiesController#async_hypervisors_update as JSON' : {'input_file.10' : 0},
                      'Processing by HostsController#externalNodes as YML' : {'input_file.11' : 0},
                      'Processing by Api::V2::HostsController#facts as JSON' : {'input_file.12' : 0},
                      'Processing by Api::V2::ConfigReportsController#create as JSON' : {'input_file.13' : 0},
                      'Processing by Api::V2::Compliance::ArfReportsController#create as JSON' : {'input_file.14' : 0},
                      'Processing by Api::V2::HostsController#show as JSON' : {'input_file.15' : 0},
                      'Processing by Api::V2::FactValuesController#index as JSON' : {'input_file.16' : 0},
                      'Processing by DashboardController#index as HTML' : {'input_file.17' : 0},
                      'Processing by Katello::Api::Rhsm::CandlepinProxiesController#post as JSON' : {'input_file.18' : 0},
                      'Processing by Katello::Api::V2::ContentViewsController#index as HTML' : {'input_file.19' : 0},
                      'Processing by Katello::Api::V2::EnvironmentsController#index as HTML' : {'input_file.20' : 0},
                      'Processing by Katello::Api::V2::ContentViewsController#show as HTML' : {'input_file.21' : 0},
                      'Processing by Katello::Api::V2::ContentViewVersionsController#index as HTML' : {'input_file.22' : 0},
                      'Processing by Katello::Api::V2::ContentViewVersionsController#promote as HTML' : {'input_file.23' : 0},
                      'Processing by ForemanTasks::Api::TasksController#show as HTML' : {'input_file.24' : 0},
                      'Processing by Api::V2::HostsController#index as JSON' : {'input_file.25' : 0}}

# input_files = ["0_rhsm_resource_list.log", "1_serials.log", "2_server_status.log", "3_consumer_show.log", "4_get.log", "5_index.log", "6_server_status_1.log", "7_facts.log", "8_login.log", "9_status.log",
#                 "10_async_hypervisors_update.log", "11_externalNodes.log", "12_facts_1.log", "13_create.log", "14_ArfReportsController_create.log", "15_show.log", "16_index_1.log"]

# Prepare a list of input files for next stage in the analysis
input_files = []
for key in processing_by_msgs:
    for subkey in processing_by_msgs[key]:
        input_files.append(subkey)

# Populate temporary files with 'Processing by ...' messages from the production log being analyzed
for key in processing_by_msgs:
    for subkey in processing_by_msgs[key]:
        temp_file = open(subkey, 'w')
        with open(input_file) as f:
            for line in f:
                if re.search(key, line):
                    temp_file.write(line)
        temp_file.close()

# Print blank line
print()

# Print header for the statistics table
print('API Call', 'Total number of calls between 00:00:00 and 23:59:59 on ' + input_date)
print('--------', '-----------------------------------------------------------------')

# Count the lines in each temporary file
for file in input_files:
    number_of_lines = 0
    f = open(file, "r")
    for line in f:
        number_of_lines += 1
    f.close()

    for key in processing_by_msgs:
        for subkey in processing_by_msgs[key]:
            if subkey == file:
                processing_by_msgs[key][subkey] = number_of_lines
                print(key, str(number_of_lines))

# Print blank line
print()

# Gather statistics
for file in input_files:
    append_zero_to_search_patterns()

    with open(file) as f:
        for line in f:
            for key in search_patterns:
                if line.startswith(key):
                    search_patterns[key][input_files.index(file)] +=1


# for key in search_patterns:
#     print(key, search_patterns[key])

customIndex = []

for msg in processing_by_msgs:
    customIndex.append(msg.replace(' ', '_'))

# Create DataFrame
df = pd.DataFrame(search_patterns,index = customIndex)

# Transpose the original DataFrame
df_transposed = df.T

# Convert the index of the DataFrame to a column
df_transposed.reset_index(level=0, inplace=True)

# Rename DataFrame columns - Replace spaces in the column labels with underscores to be able to reference columns with dot notation
df_transposed.columns = [label.replace(' ', '_') for label in df_transposed.columns]

# print (df_transposed.columns)
#
# print(df)
#
# print(df_transposed)


# Sum a column
# print(df_transposed['Processing_by_Katello::Api::V2::RootController#rhsm_resource_list_as_JSON'].sum())

# Plot the DataFrame
for index in customIndex:
    df_transposed.plot(x ='index', y=index, kind = 'bar')
plt.show()




# Pick a column
# print(df[["'2020-05-10'T00:00"]])

# Pick specific columns
# print(df[["'2020-05-10'T00:00", "'2020-05-10'T00:01", "'2020-05-10'T00:02"]])


# with open('analysis_results.csv', mode='w') as analysis_results_file:
#     analysis_results_writer = csv.writer(analysis_results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#
#     for key in search_patterns:
#         analysis_results_writer.writerow([str(key), search_patterns[key]])
