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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    is_city_valid = False
    while is_city_valid == False:
        city = input("Please enter the city you would like to view data for: ").lower()
        #the is_city_valid variable will become True if the city entered is one of the three that we have data for
        if city in CITY_DATA:
            is_city_valid = True
        else:
            print('Invalid input, Please pick either Chicago, New York City, or Washington')


    # get user input for month (all, january, february, ... , june)
    is_month_valid = False
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while is_month_valid == False:
        month = input("Please enter month you would like to view data for (all, January through June): ").lower()
        if month in months:
            is_month_valid = True
        else:
            print('Invalid input, Please pick a month from January to June or all, lowercase')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    is_day_valid = False
    days = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    while is_day_valid == False:
        day = input("Please enter day you would like to view data for (all, Sunday, Monday.. etc) ").lower()
        if day in days:
            is_day_valid = True
        else:
            print('Invalid input, Please pick a week day or "all"')


    print('-'*40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] =pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.weekday


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        day = days.index(day) + 1
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    if month == 'all':
        # display the most common month
        df['month'] = df['Start Time'].dt.month
        popular_month = df['month'].mode()[0]
        print('Most Popular Month:', popular_month)

    # display the most common day of week
    if day == 'all':
        df['weekday'] = df['Start Time'].dt.weekday
        popular_day = df['weekday'].mode()[0]
        print('Most Popular Day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station']
    pop_start_station = start_station.mode()[0]
    print('The most commonly used start station: ',pop_start_station)

    # display most commonly used end station
    end_station = df['End Station']
    pop_end_station = end_station.mode()[0]
    print('The most commonly used End Station: ',pop_end_station)

    # display most frequent combination of start station and end station trip
    start_end_combo = df['Start Station'] + ' and ' + df['End Station']
    pop_combo = start_end_combo.mode()[0]
    print('The most commonly used Start/End Station Combination: ',pop_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    tot_time = sum(travel_time.dt.total_seconds()) / 60
    print('The total travel time is : ',tot_time, ' minutes')

    # display mean travel time
    avg_trav_time = travel_time.mean()
    print('The average travel time is ', avg_trav_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if city == 'chicago' or city == 'new york city':
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)



        # Display earliest, most recent, and most common year of birth
        YOB = df['Birth Year']
        MC_BY = YOB.mode()[0]
        print('The most common birthyear is ', MC_BY)


        Min_BY = np.min(YOB)
        print('The earliest birth year is ', Min_BY)


        Max_BY = np.max(YOB)
        print('The most recent birth year is ', Max_BY)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
"""Displays raw trip data for individual trips per user input"""
    raw_data = 'yes'
    indx = 0
    while raw_data == 'yes':
        raw_data = input('Would you like to see individual trip data? Type "yes" or "no"')
        if raw_data == 'yes':
            print(df.iloc[indx:(indx + 5)])
            indx += 5

            if (indx) + 5 >= len(df):
                print(df.iloc[indx:])
                print('All available data has been displayed.')
                break
        elif raw_data == 'no':
            print('Thank you!')
        else:
            print('Please enter either "yes" or "no": ')
            raw_data = 'yes'


def main():
    """The "main" function that calls all of the subfunctions in this script"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
