import time
import pandas as pd
import numpy as np


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    valid_cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n")
        city = city.lower()
        if city in valid_cities:
            break

    valid_filters = ['month', 'day', 'not at all']
    while True:
        filter_data = input("Would you like to filter the data by month, day, or not at all?\n")
        filter_data = filter_data.lower()
        if filter_data in valid_filters:
            break

    if filter_data == 'not at all':
        month = 'all'
        day = 'all'
    else:
        if filter_data == 'month':
            while True:
                month = input("Which month - January, February, March, April, May, or June?\n")
                month = month.lower()
                valid_months = ['january', 'february', 'march', 'april', 'may', 'june']
                if month in valid_months:
                    break
            day = 'all'
        else:
            month = 'all'
            while True:
                day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n")
                day = day.lower()
                valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                if day in valid_days:
                    break

    print('-'*40)
    return city, month, day

def display_raw_data(df):
    """
    Displays raw data upon user request 5 lines at a time.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    start_index = 0
    while True:
        display_data = input("Would you like to see 5 lines of raw data? Enter 'yes' or 'no'.\n")
        if display_data.lower() == 'yes':
            print(df.iloc[start_index : start_index + 5])
            start_index += 5
        else:
            break

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
    CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

    # Load csv
    df = pd.read_csv(CITY_DATA[city])

    #check if it is loaded properly 
    #print(df.head()) 
    
    #convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month and day of week from the 'Start Time' column
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.dayofweek

    #apply filters if specified
    if month != 'all':
        # Convert month name to month number
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    if day != 'all':
        #convert day name to day number (Monday = 0, Tuesday = 1, etc.)
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day.lower())
        df = df[df['Day of Week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        df (pandas.DataFrame): The DataFrame containing the travel data.
    
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['Month'].mode()[0]
    print('Most common month:', popular_month)

    # display the most common day of week
    popular_day_of_week = df['Day of Week'].mode()[0]
    print('Most common day of week:', popular_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    
    Args:
        df (pandas.DataFrame): The DataFrame containing the travel data.
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most most commonly used start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most most commonly used end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('Most frequent trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time, 'seconds')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of User Types:\n', user_types)

    #If the Gender column exists
    if 'Gender' in df.columns:
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print('\nCounts of Gender:\n', gender_counts)

    #If the Birth Year column exists
    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('\nBirth Year Statistics:')
        print('Earliest Birth Year:', earliest_birth_year)
        print('Most Recent Birth Year:', most_recent_birth_year)
        print('Most Common Birth Year:', most_common_birth_year)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        # Prompt the user for city, month, and day filters
        city, month, day = get_filters()

        # Load the data based on the filters
        df = load_data(city, month, day)

        # Display the raw data to the user
        display_raw_data(df)

        # Calculate and display time statistics
        time_stats(df)

        # Calculate and display station statistics
        station_stats(df)

        # Calculate and display trip duration statistics
        trip_duration_stats(df)

        # Calculate and display user statistics
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
