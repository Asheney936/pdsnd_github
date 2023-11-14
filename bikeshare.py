import time
import pandas as pd



CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_city():
    while True:
        city = input("Please enter the name of the city (Chicago, New York City, Washington): ").lower()
        if city in ['chicago', 'new york city', 'washington']:
            return city
        else:
            print("Invalid input. Please try again.")

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city = get_city()

    while True:
        month = input("\nWhich month would you like to filter by? (January, February, March, April, May, June, or type 'all' if you do not have any preference)? ").lower()
        if month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            print("\nSorry, I didn't catch that. Please enter a valid month (January, February, March, April, May, June, or type 'all').")
            continue
        else:
            break

    DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("\nWhich day of the week would you like to filter by? (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday)? ").lower()
        if day != 'all' and day not in DAYS:
            print("\nSorry, I didn't catch that. Please enter a valid day of the week (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday).")
            continue
        else:
            break
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)

    df['month'] = pd.to_datetime(df['Start Time']).dt.month_name().str.lower()
    
    # Always create 'day_of_week' column
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.day_name().str.lower()

    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month is:", most_common_month)

    most_common_day = df['day_of_week'].value_counts().idxmax()
    print("The most common day of the week is:", most_common_day)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station is:", most_common_start_station)

    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station is:", most_common_end_station)

    most_common_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most frequent combination of start station and end station trip is:", most_common_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['Travel Time'] = df['End Time'] - df['Start Time']
    total_travel_time = df['Travel Time'].sum()
    print("The total travel time is:", total_travel_time)

    mean_travel_time = df['Travel Time'].mean()
    print("The mean travel time is:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        user_type_counts = df['User Type'].value_counts()
        print(user_type_counts)

        if 'Gender' in df.columns:
            gender_counts = df['Gender'].value_counts()
            print("Counts of gender:")
            print(gender_counts)
        else:
            print("Gender information not available in the dataset.")

        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]

        print("Earliest year of birth:", earliest_year)
        print("Most recent year of birth:", most_recent_year)
        print("Most common year of birth:", most_common_year)

    except KeyError as e:
        print(f"Error: {e}. Please check if the column names in your dataset match the expected names.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    start_idx = 0
    chunk_size = 5

    while True:
        show_data = input('\nWould you like to see 5 rows of the raw data? Enter yes or no.\n').lower()

        if show_data != 'yes':
            break

        print(df.iloc[start_idx:start_idx + chunk_size])
        start_idx += chunk_size

        more_data = input('\nWould you like to see 5 more rows? Enter yes or no.\n').lower()
        if more_data != 'yes':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
