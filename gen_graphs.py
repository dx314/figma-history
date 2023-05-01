import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

def format_date(date_str):
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    day_of_week = date.strftime('%a')
    date_str = date.strftime('%d-%m-%y')
    formatted_date = f'{day_of_week} {date_str}'

    return formatted_date

def plot_duration_changes(num_days=None):
    df = pd.read_csv('daily_data.csv')
    df = df.iloc[::-1]

    if num_days:
        df = df.tail(num_days)

    df['start_time'] = pd.to_datetime(df['start_time'], format='%Y-%m-%d %H:%M:%S')
    df['end_time'] = pd.to_datetime(df['end_time'], format='%Y-%m-%d %H:%M:%S')

    df['duration'] = ((df['end_time'] - df['start_time']) / np.timedelta64(1,'m'))

    df['month'] = pd.to_datetime(df['day']).dt.to_period('M')
    monthly_dfs = [group for _, group in df.groupby('month')]

    for i, df in enumerate(monthly_dfs):
        first_day = df['day'].iloc[0]
        last_day = df['day'].iloc[-1]
        month_year = first_day[:7].replace('-', '_')
        plot_title = f"{datetime.datetime.strptime(first_day, '%Y-%m-%d').strftime('%B, %Y')}"

        num_entries = len(df)
        width = max(6, num_entries * 1.5)  # Adjust the multiplier (1.5) as needed
        fig, ax1 = plt.subplots(figsize=(width, 6))

        ax1.set_xlabel('Day', fontsize=8)

        ax1.set_ylabel('Duration (min)')
        colors = np.where(df['duration'] >= 420, 'black', 'tab:red')
        ax1.bar(df['day'], df['duration'], color=colors)

        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('Changes made that day', color=color)
        ax2.plot(df['day'], df['change count'], color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        ax1.axhline(y=480, color='black', linestyle='--')

        ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: format_date(df['day'].iloc[int(x)])))
        plt.subplots_adjust(left=0.1, right=0.9)
        plt.xticks(fontsize=8)

        ax2.yaxis.label.set_color(color)
        ax2.tick_params(axis='y', colors=color)

        plt.title(plot_title)
        plt.savefig(f'plot_{month_year}.png', dpi=300, bbox_inches='tight')
        plt.close(fig)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Figma activity plots")
    parser.add_argument("--days", type=int, help="Number of days to include in the plot (default: all)")
    args = parser.parse_args()

    plot_duration_changes(args.days)
