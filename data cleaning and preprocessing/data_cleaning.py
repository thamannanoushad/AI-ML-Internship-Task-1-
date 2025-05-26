import pandas as pd
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

# #Load the Titanic dataset
df=pd.read_csv('titanic.csv')

#displays the first 5 rows
print(df.head())

#gives the number of columns,column labels,data types,memory usage, range index, and the number of cells in each column
print(df.info())

#gives some statistical data like percentile, mean and standard deviation of the numerical values of the DataFrame
print(df.describe())

#chech for missing values in each column
print(df.isnull().sum())

#handing missing values

#fill missing values in 'Age' column with the median because it is not affected by outliers
df['Age']=df['Age'].fillna(df['Age'].median())

#fill missing values in 'Embarked' column with the mode because it is categorical
df['Embarked']=df['Embarked'].fillna(df['Embarked'].mode()[0])

#drop the 'Cabin' column because it has too many missing values
df=df.drop(columns=['Cabin'])

#check for duplicates
print("Number of duplicate rows:", df.duplicated().sum())
df=df.drop_duplicates()

#encoding categorical variables

#for binary category we use map
df['Sex']=df['Sex'].map({'male':1,'female':0})

#for multi category we use get_dummies
embarked=pd.get_dummies(df['Embarked'],prefix='Embarked')
df=pd.concat([df,embarked], axis=1)
df=df.drop(columns=['Embarked'])

#standardizing numerical columns
columns_to_scale=['Age', 'Fare','SibSp','Parch']
scaler=StandardScaler()
df[columns_to_scale]=scaler.fit_transform(df[columns_to_scale])
print(df[['Age', 'Fare', 'SibSp', 'Parch']].head())

#boxplot of numerical columns to check for outliers
numerical_col=['Age','Fare','SibSp','Parch']
for col in numerical_col:
    sns.boxplot(x=df[col])
    plt.title(f'Boxplot of {col}')
    plt.show()

#removing outliers using IQR method
for col in numerical_col:
    plt.figure(figsize=(10, 5))

    #before outlier removal
    plt.subplot(1,2,1)
    sns.boxplot(x=df[col])
    plt.title(f'Before Outlier Removal: {col}')

    Q1=df[col].quantile(0.25)
    Q3=df[col].quantile(0.75)
    IQR=Q3-Q1
    lower_bound=Q1-1.5*IQR
    upper_bound=Q3+1.5*IQR
    filtered=df[(df[col]>=lower_bound)&(df[col]<=upper_bound)][col].reset_index(drop=True)

    #after outlier removal
    plt.subplot(1,2,2)
    sns.boxplot(x=filtered)
    plt.title(f'After Outlier Removal: {col}')

    plt.show()
