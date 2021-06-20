import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
from operator import attrgetter
import matplotlib.colors as mcolors

# Loading Data From Excel File
data = pd.read_csv('C:\\Users\\navee\\Desktop\\Xeno\\Data_Set_2.csv')
print(data.info())
data['created_on'] = pd.to_datetime(data['created_on'], format= "%d-%m-%Y %H:%M")

# Calculate Total Orders placed by each customer
pd.options.display.width = 0
n_orders = data.groupby(['customer_id'])['bill_no'].nunique()
mult_orders = np.sum(n_orders >1)/data['customer_id'].nunique()
print(f"{100* mult_orders:.2f}% of customers ordered more than once")

## Cohort Analysis

# Keeping  only relevant data for cohort 
df = data[["customer_id", "bill_no", "created_on"]].drop_duplicates()

# Creating variables order_month and cohort
df['order_month'] = df['created_on'].dt.to_period('M')
df['cohort'] = df.groupby('customer_id')['created_on']\
                .transform('min')\
                .dt.to_period('M')

# indicator for periods
df_cohort = df.groupby(['cohort', 'order_month']).agg(n_customers = ('customer_id', 'nunique')).reset_index(drop=False)
df_cohort['period_number'] = (df_cohort.order_month - df_cohort.cohort).apply(attrgetter('n'))

# pivot the data into a form of the matrix
cohort_pivot = df_cohort.pivot_table(index= 'cohort', columns = 'period_number', values = 'n_customers')

# divide by cohort size to obtain retention in %
cohort_size = cohort_pivot.iloc[:,0]
retention_matrix = cohort_pivot.divide(cohort_size, axis =0)

# plot the retention matrix
with sns.axes_style("white"):
    fig, ax = plt.subplots(1,2, figsize=(12,8), sharey = True, gridspec_kw={'width_ratios':[1,11]})

    sns.heatmap(retention_matrix, mask=retention_matrix.isnull(), annot= True, fmt = '.0%', cmap = 'RdYlGn', ax=ax[1])

    ax[1].set_title('Monthly Cohorts: User Retention', fontsize =16)
    ax[1].set(xlabel = "No. of Periods", ylabel='')

# cohort size
    cohort_size_df = pd.DataFrame(cohort_size).rename(columns={0: 'cohort_size'})
    white_cmap = mcolors.ListedColormap(['white'])
    sns.heatmap(cohort_size_df, 
                annot=True, 
                cbar=False, 
                fmt='g', 
                cmap=white_cmap, 
                ax=ax[0])

    fig.tight_layout()
    plt.show()
    