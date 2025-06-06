"""plot spending using Starling's CSV export
allows multiple files (appended) as Starling's maximum export is 1 year of data
"""
import argparse
import csv
import datetime
import matplotlib.pyplot as plt
import matplotlib
import numpy

parser = argparse.ArgumentParser(
    description="Plot spending using Starling's CSV export"
)
parser.add_argument("files", nargs="+", help="CSV files to plot")
# add trendline argument (integer)
parser.add_argument(
    "-t",
    "--trendline",
    type=int,
    help="add a trendline to the graph using the last n days",
    default=30,
)
args = parser.parse_args()

times: datetime.datetime = []
balances: float = []
for i in args.files:
    with open(i, newline="", encoding="unicode_escape") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            times.append(datetime.datetime.strptime(row[0], "%d/%m/%Y"))
            balances.append(float(row[5]))

# data for trendline
times_trend = []
balances_trend = []
for i, time in enumerate(times):
    if time > datetime.datetime.now() - datetime.timedelta(days=args.trendline):
        times_trend.append(time)
        balances_trend.append(balances[i])

# find the trendline
trendline = numpy.polyfit(
    matplotlib.dates.date2num(times_trend),
    balances_trend,
    1,
)

# find zero crossing
zero_crossing = -trendline[1] / trendline[0]
# as a datetime
zero_crossing = matplotlib.dates.num2date(zero_crossing)
today = datetime.datetime.now(
    tz=datetime.timezone(datetime.timedelta(hours=0))
).replace(hour=0, minute=0, second=0, microsecond=0)
days_until_zero = zero_crossing - today


plt.xkcd()
plt.plot(times, balances, label="Balance", zorder=2)
plt.plot(
    [
        datetime.datetime.now() - datetime.timedelta(days=args.trendline),
        datetime.datetime.now() + datetime.timedelta(days=90),
    ],
    [
        trendline[0]
        * matplotlib.dates.date2num(
            datetime.datetime.now() - datetime.timedelta(days=args.trendline)
        )
        + trendline[1],
        trendline[0]
        * matplotlib.dates.date2num(
            datetime.datetime.now() + datetime.timedelta(days=90)
        )
        + trendline[1],
    ],
    "--",
    alpha=0.5,
    zorder=1,
    label=f"{args.trendline} day trend\n£{trendline[0]:.2f} per day\n"
    f"Zero in {days_until_zero.days} days\n  on {zero_crossing.strftime('%d/%m/%Y')}",
)

# line on each new year
plotdates = [
    datetime.datetime(yr, 1, 1)
    for yr in range(
        int(min(times).strftime("%Y")) + 1,
        int(max(times).strftime("%Y")) + 1,
    )
]
plt.vlines(plotdates, 0, 2000, "gray", "--")


plt.xlabel("Time")
plt.ylabel("Balance")
plt.title("Balance over time")
plt.ylim(bottom=0)
plt.xlim(right=datetime.datetime.now() + datetime.timedelta(days=90))
plt.grid(True, axis="y", lw=0.5, zorder=0)
plt.axvline(datetime.datetime.now(), color="k", linestyle="--", zorder=1)
plt.legend(loc="upper left")
plt.show()
