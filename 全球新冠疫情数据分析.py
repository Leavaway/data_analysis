"""
Template for the COMP1730/6730 project assignment, S2 2021.
The assignment specification is available on the course web
site, at https://cs.anu.edu.au/courses/comp1730/assessment/project/


The assignment is due 25/10/2021 at 9:00 am, Canberra time

Collaborators: <list the UIDs of ALL members of your project group here>
ANU ID: u7374681  Name: Jiayong Zhu
ANU ID: u7352166  Name: Qiya Zhou
ANU ID: u7346505  Name: Jiamin Rui 
"""
import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import cm

os.chdir('C:\\Users\\Administrator\\Desktop\\COMP6730\\covid-data')
def analyse(path_to_files):
    '''
    print the results of each question by dealing with the covid-data from csv files

    param: path_to_files: path to the csv files provided

    no return values
    '''
    #quetion 1
    print(f"Analysing data from folder ...\n")
    file_names = (os.listdir(path_to_files))[1:]
    sorted_file_names = sorted(file_names, key=lambda filename: int(filename[6:10] + filename[0:2] + filename[3:5]),
                               reverse=True) # reorganize the date expression and sort from big to small.
    recent_data_file_name = sorted_file_names[0]
    print("Question 1:\n"
          f"Most recent data is in file `{recent_data_file_name}`")
    recent_sorted_records = pd.read_csv(path_to_files +'//'+ recent_data_file_name).sort_values("Last_Update",
                                                                                                ascending=False)
    # In the last updated date file, sort the column of "Last_Update" from big to small.
    last_updated = recent_sorted_records["Last_Update"][0]
    print(f"Last updated at {last_updated}")
    # definite 2 dictionaries to store the total worldwide confirmed cases and deaths.
    cases_cnt = recent_sorted_records.agg({"Confirmed": "sum"})["Confirmed"]
    deaths_cnt = recent_sorted_records.agg({"Deaths": "sum"})["Deaths"]
    print(f"Total worldwide cases: {cases_cnt} , Total worldwide deaths: {deaths_cnt}\n")

    # question 2
    print("Question 2:")
    answers2a = recent_sorted_records.groupby(["Country_Region"]).agg({"Confirmed": "sum", "Deaths": "sum"}).sort_values(
        "Confirmed", ascending=False) # use function 'groupby.agg' to disaggregate the data by country
                                      # and then aggregate the data of columns 'Confirmed' and 'Deaths'
    last_2_records = pd.read_csv(path_to_files +'//'+ sorted_file_names[1]).groupby(["Country_Region"]).agg({"Confirmed": "sum", "Deaths": "sum"})
                                      # last_2_records: store the the number of confirmed cases and deaths of each country
                                      # in the day  immediately before the last update
    # todo  question 2(c)
    # How we make an assumption on recovery data:
    #    The recovery data is not offered in the csv files. We searched total recovery numbers on the Internet 
    # and divided them by total confirmed cases. Then we assumes the medical level of a country is near constant. 
    # So we assumes this total recovery rate as the daily rocovery rate to calculate the active case of that country. 
    # The recovery data we used comes from: www.worldometers.info/coronavirus/country
    recovery = [0.7749,0.8633,0.9613,0.8184,0.8742,0.7282,0.9262,0.9201,0.9748,0.9687]
    for i in range(10):
        print(f"{answers2a.index[i]} - total cases: {answers2a['Confirmed'][i]} deaths: {answers2a['Deaths'][i]}"
              f" new: {answers2a['Confirmed'][i] - last_2_records['Confirmed'][answers2a.index[i]]}"f"  active: {answers2a['Confirmed'][i]-answers2a['Deaths'][i]-round(answers2a['Confirmed'][i]*recovery[i])}")
    x_pos = np.arange(10)
    y_pos = answers2a['Confirmed'].to_list()
    plt.subplot(221)
    plt.bar(answers2a.index[:10],answers2a['Confirmed'][:10],color = cm.rainbow(np.linspace(0, 1, 10)),align = 'center',alpha = 1)
    plt.xlabel("Top10 country")
    plt.ylabel("Total cases")
    plt.subplot(222)
    plt.bar(answers2a.index[:10],answers2a['Deaths'][:10],color = cm.rainbow(np.linspace(0, 1, 10)),align = 'center',alpha = 1)
    plt.xlabel("Top10 country")
    plt.ylabel("Total deaths")
    plt.subplot(223)
    plt.bar(answers2a.index[:10],answers2a['Confirmed'][:10]-answers2a['Deaths'][:10]-round(answers2a['Confirmed'][:10]*recovery[:10]),color = cm.rainbow(np.linspace(0, 1, 10)),align = 'center',alpha = 1)
    plt.xlabel("Top10 country")
    plt.ylabel("Total active")
    # plt.xticks(x_pos,answers2a.index[i])
    plt.show()
    print(answers2a)
    # question 3
    # load all records
    # In the Q3, there are some datas before the date 2021-08-17 and we also take them into consideration and print them
    # because we think these datas also have reference values though the answer maybe wierd because of the probably wrong data provided.
    print()
    print("Question 3:")
    all_records = [pd.read_csv(path_to_files +'//'+ file_name) for file_name in file_names] #use osp.join to pass in multiple paths
    all_records = pd.concat(all_records,axis=0) #use pd.contact to connect all the files end to end by column
    all_records["Last_Update"] = all_records["Last_Update"].map(lambda x:x[:10]) # only select year, month, date
    group_by_date_descend = all_records.groupby(["Last_Update"]).agg({"Confirmed": "sum", "Deaths": "sum"}).sort_index(axis=0,ascending=False)
                                                                                       # calculate the confirmed cases and deaths of each day;
                                                                                       # sort the dated from big to small
    group_by_date_descend["New Deaths"] = 0
    group_by_date_descend["New Confirmed"] = 0
    for i in range(1,len(group_by_date_descend)):
        today = group_by_date_descend.index[i]
        next_date = group_by_date_descend.index[i-1]
        # then subtract the data of adjacent days
        group_by_date_descend["New Confirmed"][today] = group_by_date_descend['Confirmed'][next_date] - group_by_date_descend['Confirmed'][today]
        group_by_date_descend["New Deaths"][today] = group_by_date_descend['Deaths'][next_date] - group_by_date_descend['Deaths'][today]
        print(f"{today} : new cases:{group_by_date_descend['New Confirmed'][today]} "
              f"new deaths : {group_by_date_descend['New Deaths'][today]}")

    # use function strftime and the formate parameter is :%W, returning week number with the first Monday as the first day of week one
    group_by_date_descend["week"] = group_by_date_descend.index.map(lambda x:datetime.datetime(int(x[:4]),int(x[5:7]),int(x[8:10])).strftime(f"{x[:4]}%W"))
    week_groups = group_by_date_descend[1:].groupby(["week"]) #remove the oldest day
    week_agg = week_groups.agg({"New Deaths":"sum","New Confirmed":"sum"}).sort_index(axis=0,ascending=False) # add together the new cases in the same week
    for week in week_agg.index: #for loop of each week number
        from_date = week_groups.groups[week][-1]
        to_date = week_groups.groups[week][0]
        print(f"Week {from_date} to {to_date} : New cases: {week_agg['New Confirmed'][week]} New deaths: {week_agg['New Confirmed'][week]}")

    #question 4
    print()
    print("Question 4:")
    recent_sorted_records['Population'] = recent_sorted_records['Confirmed']/recent_sorted_records['Incident_Rate'] # add a column to show population of each country/region (unit:100000)
    recent_sorted_records['Deaths'] = recent_sorted_records['Confirmed'] * recent_sorted_records['Case_Fatality_Ratio'] / 100 # add a column to show the death toll of a country/region
    recent_sorted_records_Confirmed = recent_sorted_records.groupby(["Country_Region"]).agg({"Confirmed": "sum", "Population": "sum", "Deaths":"sum"})['Confirmed']
    recent_sorted_records_Population = recent_sorted_records.groupby(["Country_Region"]).agg({"Confirmed": "sum", "Population": "sum", "Deaths":"sum"})['Population']
    recent_sorted_records_Deaths = recent_sorted_records.groupby(["Country_Region"]).agg({"Confirmed": "sum", "Population": "sum", "Deaths":"sum"})['Deaths']

    # now connect the overall number of population,deaths and confirmation of a country in a new table
    recent_sorted_records_Confirmed_Population_Deaths = pd.concat([recent_sorted_records_Confirmed,recent_sorted_records_Population,recent_sorted_records_Deaths],axis=1) #
    recent_sorted_records_Confirmed_Population_Deaths = recent_sorted_records_Confirmed_Population_Deaths.drop(index=(recent_sorted_records_Confirmed_Population_Deaths.loc[(recent_sorted_records_Confirmed_Population_Deaths['Population'] == 0)].index))
    # calculate 2 weighted ratios of each country
    recent_sorted_records_Confirmed_Population_Deaths['weighted_incident_rate'] = recent_sorted_records_Confirmed_Population_Deaths['Confirmed'] / recent_sorted_records_Confirmed_Population_Deaths['Population']
    recent_sorted_records_Confirmed_Population_Deaths['weighted_case_fatality_ratio'] = recent_sorted_records_Confirmed_Population_Deaths['Deaths'] / recent_sorted_records_Confirmed_Population_Deaths['Confirmed']
    recent_sorted_records_Confirmed_Population = recent_sorted_records_Confirmed_Population_Deaths.sort_values('weighted_incident_rate',ascending = False)
    for i in range(10):
        print("{} : {:.0f} cases per 100,000 people and case-fatality ratio:{:.2%} ".format(recent_sorted_records_Confirmed_Population.index[i],
                                                                                        recent_sorted_records_Confirmed_Population['weighted_incident_rate'][i],
                                                                                        recent_sorted_records_Confirmed_Population['weighted_case_fatality_ratio'][i]))


# The section below will be executed when you run this file.
# Use it to run tests of your analysis function on the data
# files provided.

if __name__ == '__main__':
    # test on folder containg all CSV files
    analyse('./covid-data')
