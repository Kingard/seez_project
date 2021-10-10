# A simple data wrangling project for SEEZ

**This is a simple data wrangling project where I passed-in a csv file containing car 
information from the MENA (Middle East and North Africa) region. Below, I have written a Python script using the OOP paradigm.
The procedures I carried out on the data are represented by the class-based methods. I also
highlighted my thought process in developing some of the algorithms used.**

To use this project locally you must have [python](https://www.python.org/downloads/) installed.

1. **Clone the repository:**
    ```sh
    git clone -b master https://github.com/Kingard/seez_project.git
    ```
2. **Setup the virtual environment by running:**
    ```sh
    virtualenv env
    source env/Scripts/activate # for windows
    source env/bin/activate # for MacOs
    ```
    in the project root folder.
3. **Install External Dependencies:**
    ```sh
    pip install -r requirements.txt

4. **Running the script**

5. **Imports**
    ```py
        import numpy as np
        import pandas as pd
        import statistics
        from collections import Counter
        from datetime import datetime, timezone, date, timedelta
    ```

## Script

### Middle East and North Africa Car Usage Facts and Figures
Located at [main.py](main.py) this script uses *pandas* to fetch the
**Middle East and North Africa Car data** in the csv file provided.

1. **The python  ```__init__``` constructor. This is an integral part of OOP style development, 
and it gets called whenever the class is initialized.** <br> **I parsed in under the ```__init__```
block since the data is integral for every method within the class.**
  
    ```py
        def __init__(self,data):
            self.data = pd.read_csv('DE_Lead_test.csv')
    ```

2. **The ```load_data``` method. This just returns the first 5 rows of the data and shows
 that it was parsed correctly.**
  
    ```py
        def load_data(self):
            return self.data.head()
    ```
3. **The ```find_duplicate```method. This method returns all duplicate rows by leveraging
 on python's in-built ```.duplicated()``` *method*.** 
  
    ```py
        def find_duplicate(self):
            return self.data[self.data.duplicated()]
    ```
4. **The ```clean_engine_disp```method. This method cleans the engine_display and removes outliers
  and nan values. By convention, for categorical data, the Nan values are replaced with the mode, 
  and for numerical data, the Nan values are replaced by the median value ```2.7``` in this case.** 
  
    ```py
        def clean_engine_disp(self):
            median_value = statistics.median(self.data.engine_displacement.dropna().values)
            self.data.engine_displacement.fillna(median_value, inplace=True)
            return self.data.head()
   ```

5. **The ```create_warranty_info```method. This method checks the tag column, creates a warranty column 
 and maps Yes for cars under warranty, and NO for cars that aren't under warranty. It leverages
 on Numpy's in-built method ```np.where(condition, action under condition, action otherwise)```.** 
  
    ```py
        def create_warranty_info(self):
        # Locates the tag column, creates a warranty column and maps Yes for cars under warranty,
        # and then No to cars without the under_warranty tag
            self.data['under warranty'] = np.where(self.data['tags'] == '{under_warranty}', 'YES', 'NO')
    ``` 
   
6. **The ```compare```method. This method compares the title column with the tags column to check
   if the warranty information is consistent: it *returns* True/False. it uses two counters: 
   ```counter_1``` and ```counter_2``` that check for the occurrence of warranty in the title string and the 
   tags string per vehicle respectively. Since we know that the vehicles that have warranty contain
   *warranty* in the title string it's easy to check using the ```if ``` statement.** 
  
    ```py
        def compare(self):
            info = self.data['title'].values # Extracting the values in the title column
            tags_data = self.data['tags'].values # Extracting the values in the tags column
            counter_1 = counter_2 = 0
            for _ in info:
                if 'WARRANTY' in str(_) or 'warranty' in str(_): # In the title column, cars with warranty contain the "WARRANTY" string
                    counter_1 +=1
            for _ in tags_data:
                if _ == "{under_warranty}":
                    counter_2 += 1
   
            # This last statement checks to see if there are as many warranty count in the 
            # title column as there are in the tags column. Returns True if they're equal and 
            # and False otherwise
            if counter_1 != counter_2:
                return False

            else:
                return True
    ``` 
7. **The ```sec_most_expensive_car```method. This method returns the second most expensive car.
   it uses python's in-built ```sorted()``` *method* along with the slice notation to extract 
   the second-highest value which is at index ```[-2] ``` of any sorted array. It returns the car(s)
   with the second-highest price.** 
  
    ```py
        def sec_most_expensive_car(self):
        
            # Find second most expensive price
            second_most_value = sorted(list(self.data['price'].values))[-2]
            
            # Find the car(s) that correspond to that price tag
            return self.data[self.data['price'] == second_most_value]['title'].values
    ```
8. **The ```find_count```method. This method returns the number of cars per make using python's 
 in-built ```Counter``` method. The output is of the form ```{'audi':25,'toyota':77}```** 
  
    ```py
        def find_count(self):
            # Here we simply leverage on the Counter module
            # that returns the count of items of a list as a dictionary
            return Counter(self.data.make)   # we are counting based on the 'make' column
    ```
   
9. **The ```cheapest_per_make```method. This method returns the cheapest car for every make. I used 
    python's in-built sorted() method to arrange the price values and then returned the cheapest 
    price for every car. The Output structure is initially of the form 
``` {lexus: [12300,234555,2345555], nissan: [12500,28700,35600]} ```. The final result returns the 
    cars with the prices in a DataFrame** 
  
     ```py
         def cheapest_per_make(self):
             required_data = {}
             for i, j in zip(list(self.data.make.values), list(self.data.price.values)):
                 if i not in required_data:
                     required_data[str(i)] = [j]

                 else:
                     required_data[i].append(j)  # required data is of the form:
                     # {lexus: [12300,234555,2345555],
                     # nissan: [12500,28700,35600]}

                 final_data = pd.DataFrame(list(required_data.keys()))
                 # the first index value of a sorted list is the smallest value
                 final_data['prices'] = [sorted(i)[0] for i in required_data.values()]
                 final_data.columns = ['car make', 'cheapest price']

             return final_data  # gives a table showing each car and the cheapest one
     ```
   
10. **The ```sanity_check``` method checks to see if there's an anomaly characterized by a car updated
    before it was created. It returns ```True``` if there's any such entry and ```False``` otherwise.**
    
    ```py
        def sanity_check(self):
    
            # Checks if there's any instance where a car is updated before being created;
            # returns True or False if any exists
    
            self.data['sanity_check'] = self.data['updated_at'] > self.data['created_at']
            return list(self.data.sanity_check.values).count(True) == len(list(self.data.sanity_check.values))
    ```
11. **The ```actives_and_nonactives``` method returns the number of actives and nonactives per city(country).
   the number of ```True``` values correspond to the number of actives per city(country), whereas the 
   number of ```False``` values correspond to the number of nonactives per city (country).**
    ```py
         def actives_and_nonactives(self):
            x = self.data[['city', 'active']].dropna().sort_values(by='city')
            return x.groupby('city')['active'].value_counts()
    ```
    
12. **The ```recency_finder``` method creates a column for the number of days between today and when each car was
 last updated. I used the in-built method ```pd.Timestamp.utcnow()``` which takes the time zone into
 consideration.**
    ```py
        def recency_finder(self):
            # Returns the number of days between the update_date and today
            self.data['recency'] = pd.Timestamp.utcnow().normalize() - pd.to_datetime(self.data['updated_at'],errors='coerce')
    ```
    
13. **The ```submodel_extractor``` method returns a list of the sumbodels of the cars as extracted 
from the title column by using the make column as a benchmark. Since we know that the title comprises the make and 
the sub-model name, we can thus extract the sub-model name from the title by removing the make value from 
the title. I used python's in-built ```.replace()``` method to extract the sub-model names.**
    ```py
        def submodel_extractor(self):
            submodel_list = []
            for i in range(len(list(self.data.title.values))):
                if str(self.data.make.values[i]) in str(self.data.title.values[i]):
                    # Since we know that the title comprises the make and the submodel name
                    # we can thus extract the submodel name from the title
                    submodel = str(self.data.title.values[i]).replace(str(self.data.make.values[i]), '')
                    submodel_list.append(str(self.data.title.values[i]).replace(str(self.data.make.values[i]), ''))

                

            return submodel_list
    ```

14. **The ```create_new_table``` method creates a new table with an extra column called ```unique id```. This 
 ```unique id``` column is a combination of the ```make, model, year, city, created_at``` columns. This 
 method returns the first 5 rows of the new table.**
    ```py
        def create_new_table(self):
            new_table = self.data
            new_table['unique id'] = self.data['make'] + ' ' + self.data['model'] + ' '+ self.data['year'] + ' '+self.data['city'] + ' '+self.data['created_at']
            return new_table.head()
    ```
