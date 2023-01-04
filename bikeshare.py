import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello there friend! Let\'s explore some US bikeshare data!')
    print('~'*80)
    print('~'*80)

    # Fetches user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in CITY_DATA.keys():
        city = input('Would you like to explore bikeshare data for Chicago, New York City, or Washington? \n> ').lower()

        if city not in CITY_DATA.keys():
            print("\nOops! That is not a valid city in our dataset, restarting selection process.")
            print("\nInputs are not case sensitive. Valid inputs are: Chicago, New York City, and Washington.")

    print("\n You have selected your city!!")

    # Fetches user input for month (all, january, february, ... , june)
    month = ''
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input('Would you like to filter the data by month (Available Months: January - June) or view data for all months (Enter: All)? \n> ').lower()

        if month in months:
            break
        else:
            print("\nOops! That is not a valid month in our dataset, restarting selection process.")



    # Fetches user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']
    while True:
        day = input('Would you like to select a day (e.g. Sunday) or view data for all weekdays (Input: All)? \n>').lower()
        if day in days:
            break
        else:
            print("\nOops! That is not a valid day selection in our dataset. restarting selection process.")

    print('~'*80)
    print('~'*80)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #Load data for city
    print("\nLoading your super customized dataset...")
    df = pd.read_csv(CITY_DATA[city])

    #Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.weekday_name

    #Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Filter by month to create the new dataframe
        df = df[df['Month'] == month]

    #Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['Day_of_Week'] == day.title()]

    #Returns the selected file as a dataframe (df) with relevant columns

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('-'*80)
    print('\nCalculating The Most Frequent Times of Travel...')
    print('-'*80)
    start_time = time.time()

    print('\n~~~~~Bike Share Times of Travel Statistics~~~~~\n')

    #Uses mode method to find the most/least common month/day
    common_month = df['Month'].mode()[0]
    least_common_month = df['Month'].min()
    common_day = df['Day_of_Week'].mode()[0]
    least_common_day = df['Day_of_Week'].min()

    # Displays Most/Least Common Months if relevant to current dataframe
    if common_month != least_common_month:
        print("\nMost Common Month: ",common_month)
        print("\nLeast Common Month: ",least_common_month)
    else:
        print("\nMost/Least Common Months Usage Statistics Irrelevant due to selecting one month...")

    # Displays Most/Least Common Days if relevant to current dataframe
    if common_day != least_common_day:
        print("\nMost Common Day of the Week: ",common_day)
        print("\nLeast Common Day of the Week: ",least_common_day)
    else:
        print("\nMost/Least Common Days Usage Statistics Irrelevant due to selecting one day...")

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    # Uses mode method to find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('\nMost Popular Start Hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('~'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('-'*80)
    print('\nCalculating The Most Popular Stations and Trip...\n')
    print('-'*80)
    start_time = time.time()

    print('\n~~~~~Bike Share Station Statistics~~~~~\n')

    # Displays most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    print("\nThe most common starting station is: ", most_start_station)

    # Displays most commonly used end station
    most_end_station = df['End Station'].mode()[0]
    print("\nThe most common terminal station is: ",most_end_station)

    # Displays most frequent combination of start station and end station trip
    df['Trip Path'] = df['Start Station'].astype(str) + ' to ' + df['End Station'].astype(str)
    trip_path = df['Trip Path'].mode()

    print("\nThe Most Common Ride (Start to End) is: \n")
    print(df['Trip Path'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('~'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    """ Trip Duration Column From file is in Seconds so need to convert to minutes/seconds format & hours/minutes format using divmod"""

    print('-'*80)
    print('\nCalculating Trip Duration...\n')
    print('-'*80)
    start_time = time.time()

    print('\n~~~~~Bike Share Trip Duration Statistics~~~~~\n')

    # TO DO: display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_trip_duration, 60)
    hour, minute = divmod(minute, 60)

    print(f"Total Sum of all Trips: {hour} hours, {minute} minutes and {second} seconds.")

    # TO DO: display mean travel time
    average_trip_duration = round(df['Trip Duration'].mean())
    #Finds the average duration in minutes and seconds format
    minutes, seconds = divmod(average_trip_duration, 60)

    if minutes > 60:
        hours, minutes = divmod(minutes, 60)
        print(f"\nThe Average trip duration is: {hours} hours, {minutes} minutes and {seconds} seconds.")
    else:
        print(f"\nThe Average Trip Duration is: {minutes} minutes and {seconds} seconds.")

    print("\nAverage Trip Duration in Seconds by User Type: \n",df.groupby(['Month', 'User Type'])['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('~'*80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('-'*80)
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('\n~~~~~Bike Share User Statistics~~~~~\n')

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('\nCount of User Types\n')
    print('-'*35)
    print(user_type)
    print('-'*35)

    # Display counts of each gender for each user type
    # Uses the try clause since not every df has a gender column
    try:
        print('\nCount of User Types by Gender:\n')
        print('-'*35)
        print(df.groupby(['User Type'])['Gender'].value_counts())
        print('-'*35)
    except:
        print("\nOooops! My apologies, we do not have gender related information for your selected city.")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = int(df['Birth Year'].min())
        recent_birth = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print("\nEarliest Birth Year: ",earliest_birth)
        print("\nMost Recent Birth Year: ",recent_birth)
        print("\nMost Common Birth Year: ",common_birth_year)
    except:
        print("\n Oooops! My apologies, we do not have any birth year details for your selected city.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('~'*80)


def display_raw_data(df):
    """Utilizes .head() to display 5 rows from the user-selected city raw data
    Arg:
        param1 (df): The data frame for the selected city.
    Returns:
        nothing
    """
    print("\n Now Entering Raw Data Viewer...")
    print('-'*80)

    #created list to store possible response values
    response_lst = ['yes','no']
    response =''
    counter = 0

    #initial while loop to get user input and ensure it matches correct response syntax
    while response not in response_lst:
        print("\n If you want to view the first five lines of raw data enter yes, if not type no.")
        response = input().lower()

        if response =="yes":
            print(df.head())
        elif response not in response_lst:
            print("\n Oooops! Your input is something other than \'yes\' or \'no\'... please retry!!")

    #this while loop repeats the input request until the user answers something other than yes
    while response == "yes":
        print("\nDo you want to see five more lines of data?")
        print("\nIf you do... type yes. If you do not... type no.")
        counter += 5
        response = input().lower()

        if response == "yes":
            print(df[counter:counter+5])
        else:
            break

    print("\n Now Exiting Raw Data Viewer...")
    print('~'*80)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
