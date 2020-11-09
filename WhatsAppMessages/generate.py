import numpy as np
import pandas as pd


# Generate some fake data
np.random.seed(42)

# The total number of HSMs to test
hsm_n = 3
hsms = [f"hsm_template_{i+1}" for i in range(3)]

# Total number of incoming messages
in_messages_n = 10_000
ids = np.linspace(1, in_messages_n, in_messages_n)

# Messages come at different times of the day and we'll model this with a Beta distribution
# The support of the Beta distribution is [0, 1] and we use this to represent the fraction of the day
# For example: 10 p.m. => 22/24 = 0.92
ts_day = np.random.beta(7, 5, size=in_messages_n) * 24

# Now we can generate data about the hour of the day
zero_rounder = lambda v: round(v, 0)
zero_rounder = np.vectorize(zero_rounder)
hour_of_day = zero_rounder(ts_day)

# We can also extract the minutes of the day
minute_of_day = zero_rounder(ts_day * 60)

# We'll model these messages to be received during the course of a week
# So we'll distribute them in five days
total_days = 5

# For the sake of simplicity let's distribute the day of the week uniformly
day_of_week = np.random.randint(1, total_days + 1, size=in_messages_n)

# Create a sort of timestamp
ts = ts_day + (day_of_week * 24)

# For each HSM, we need to determine what the outcome would be
#  1 = "Response" and 0 = "Ignored"

# We'll model this in two ways, the simple and the complex
# In the simple method, we'll assign a distribution to each HSM
# and draw samples for it to determine if the message was replied
# In the complex method we'll take into account the time and day
# simulating time-of-day effects (saying "Good evening" in the morning)
# and day-of-week effects (templated getting old)

# We start by assigning random conversion rates to each HSM
conv_rates = np.random.beta(3, 70, size=3)

# Now we can generate the result for each HSM
results = [
    np.random.choice([0, 1], p=[1 - p, p], size=in_messages_n) for p in conv_rates
]

# Put it all together in a Pandas DF
df = pd.DataFrame([ids, ts, ts_day, hour_of_day, minute_of_day, day_of_week]).T
df.columns = ["id", "ts", "ts_day", "hour_of_day", "minute_of_day", "day_of_week"]
df["id"] = df["id"].astype(int)

# Load the result for each HSM
for idx, hsm in enumerate(hsms):
    df[f"{hsm}_result"] = results[idx]

# Export data as CSV
df.to_csv("whatsapp_messages.csv", index=False)
