
import numpy as np
import pandas as pd
from collections import Counter
import statistics
from datetime import datetime, timezone, date, timedelta


class DataEng:

    def __init__(self,data):
        self.data = pd.read_csv('DE_Lead_test.csv')

    # Reading the data; This returns the first 5 rows of the data...
    def load_data(self):
        return self.data.head()

    # 1. Finding duplicate rows
    def find_duplicate(self):
        return self.data[self.data.duplicated()]

    def clean_engine_disp(self):
        median_value = statistics.median(self.data.engine_displacement.dropna().values)
        self.data.engine_displacement.fillna(median_value, inplace=True)
        return self.data.head()

    # 3. Extract warranty column
    def create_warranty_info(self):
        # Locates the tag column, creates a warranty column and maps Yes for cars under warranty,
        # and then No to cars without the under_warranty tag
        self.data['under warranty'] = np.where(self.data['tags'] == '{under_warranty}', 'YES', 'NO')

    # 4. Compare the title column with the tags column to check
    #    if the warranty information is consistent: return True/False
    def compare(self):
        info = self.data['title'].values
        tags_data = self.data['tags'].values
        counter_1, counter_2 = 0
        for _ in info:
            if 'WARRANTY' in str(_) or 'warranty' in str(_): # In the title column, cars with warranty contain the "WARRANTY" string
                counter_1 +=1
        for _ in tags_data:
            if _ == "{under_warranty}":
                counter_2 += 1

        if counter_1 != counter_2:
            return False

        else:
            return True

    # 5. Find the second most expensive car
    def sec_most_expensive_car(self):

        # Find second most expensive car
        second_most_value = sorted(list(self.data['price'].values))[-2]

        return self.data[self.data['price'] == second_most_value]['title'].values

    # 6. Count how many cars exist for each make/model combination.
    def find_count(self):
        # Here we simply leverage on the Counter module
        # that returns the count of items of a list as a dictionary
        return Counter(self.data.make)   # we are counting based on the 'make' column
        # output is of the form {'audi':25,'toyota':77}

    # 7. Find the cheapest car per make/model combination
    def cheapest_per_make(self):
        required_data = {}
        for i, j in zip(list(self.data.make.values), list(self.data.price.values)):
            if i not in required_data:
                required_data[str(i)] = [j]

            else:
                required_data[i].append(j)  # required data is of the form:
                # {lexus: [12300,234555,2345555],
                #  nissan: [12500,28700,35600]}

            final_data = pd.DataFrame(list(required_data.keys()))
            # the first index value of a sorted list is the smallest value
            final_data['prices'] = [sorted(i)[0] for i in required_data.values()]
            final_data.columns = ['car make', 'cheapest price']

        return final_data  # gives a table showing each car and the cheapest one

    # 8. Compare created_at, updated_at columns for sanity check
    def sanity_check(self):
        # Checks if there's any instance where a car is updated before being created;
        # returns True or False if any exists
        self.data['sanity_check'] = self.data['updated_at'] > self.data['created_at']
        return list(self.data.sanity_check.values).count(True) == len(list(self.data.sanity_check.values))

    # 9. Find the number of actives and non_actives per country(city)
    def actives_and_nonactives(self):
        x = self.data[['city', 'active']].dropna().sort_values(by='city')
        return x.groupby('city')['active'].value_counts()

    # 10. Create a column named recency where you calculate the number of days between last_seen_at and today’s date.
    def recency_finder(self):
        # Subtracting the update_at column from today's date taking the utc timezone into consideration
        self.data['recency'] = pd.Timestamp.utcnow().normalize() - pd.to_datetime(self.data['updated_at'],errors='coerce')

    # 11. Extract submodel information from the title column
    def submodel_extractor(self):
        submodel_list = []
        for i in range(len(list(self.data.title.values))):
            if str(self.data.make.values[i]) in str(self.data.title.values[i]):
                # Since we know that the title comprises the make and the submodel name
                # we can thus extract the submodel name from the title
                submodel = str(self.data.title.values[i]).replace(str(self.data.make.values[i]), '')
                submodel_list.append(str(self.data.title.values[i]).replace(str(self.data.make.values[i]), ''))

            #print(submodel)

        return submodel_list

    # 12. Finally create a new table with the above added columns, also create a unique identifier
    def create_new_table(self):
        new_table = self.data
        new_table['unique id'] = self.data['make'] + ' ' + self.data['model'] + ' ' + self.data['year'] + ' '+self.data['city'] + ' '+self.data['created_at']
        return new_table.head()


d = DataEng('DE_Lead_test.csv')
if __name__ == '__main__':
    print(d)


