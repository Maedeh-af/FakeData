import numpy as np
import pandas as pd


# Generate some fake data
np.random.seed(42)

# The total number of customers
customers_n = 4
customers = [f"customer_{i+1}" for i in range(customers_n)]

messages = {}

# We'll use the same timeframe for all customers
weeks = 10
days = np.linspace(1, weeks * 7, weeks * 7)

# Iterate all the customers
# We'll generate messages for customers one by one
for customer in customers:
    customer_messages = []

    # Iterate the number of weeks
    for week in range(weeks):

        # Iterate days of the week
        for day in range(7):

            # Starting number of messages
            if len(customer_messages) == 0:
                # Random starting number of messages between 10K and 50K
                new_messages = np.random.randint(100, 1_000)

            # If it's not the first day of history
            else:
                # Randomly decide if the number of messages will increase or decrease
                # We use a binomial to be able to be biased towards an increase/decrease
                # Our bias will change depending on the day of the week
                if day == 5 or day == 6:
                    # Weekends will be more likely to decrease
                    growth_decrease = np.random.binomial(1, 0.3)
                else:
                    # Weekdays will be more likely to increase
                    growth_decrease = np.random.binomial(1, 0.9)

                # We'll randomly generate the growth or deacrease rate
                # The rate will come from a broad Beta distribution
                rate = np.random.beta(2, 2)

                # Calculate the number of new messages as a function of the previous
                new_messages = int(customer_messages[-1] * (growth_decrease + rate))

            # Store the new messages for the customer
            customer_messages.append(new_messages)

    # Store the customer's message history
    messages[customer] = customer_messages


# Put it all together in a Pandas DF
df = pd.DataFrame(messages)
df["day"] = days.astype(int)

# Black magic to change the order of the columns, because OCD
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]

# Export data as CSV
df.to_csv("whatsapp_messages.csv", index=False)
