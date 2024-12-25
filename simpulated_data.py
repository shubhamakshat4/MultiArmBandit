import numpy as np
import pandas as pd

# Parameters for simulation
num_agents = 100
num_days = 100
leads_per_day = 1000

# Generate a base conversion rate for each agent (varying randomly)
np.random.seed(42)  # For reproducibility
base_conversion_rates = np.random.uniform(0.01, 0.2, num_agents)  # Random conversion rates between 1% and 20%

# Generate a daily variation matrix for conversion rates (simulating real-world fluctuations)
daily_variations = np.random.uniform(0.8, 1.2, (num_days, num_agents))  # Daily variation between 80% and 120%

# Simulate traditional lead distribution: equal leads to all agents
traditional_lead_distribution = np.full((num_days, num_agents), leads_per_day / num_agents)

# Calculate daily conversion rates for each agent (adjusted for daily variations)
daily_conversion_rates = base_conversion_rates * daily_variations

# Calculate sales closures
daily_sales_closures = traditional_lead_distribution * daily_conversion_rates

# Aggregate results into a dataset
data = []
for day in range(num_days):
    for agent in range(num_agents):
        data.append({
            "Day": day + 1,
            "Agent_ID": agent + 1,
            "Leads_Allocated": traditional_lead_distribution[day, agent],
            "Conversion_Rate": daily_conversion_rates[day, agent],
            "Sales_Closed": daily_sales_closures[day, agent]
        })

# Create a DataFrame for the dataset
simulated_data = pd.DataFrame(data)

# Save to a CSV file (optional)
simulated_data.to_csv("simulated_lead_distribution2.csv", index=False)

# Display the first few rows of the dataset
print(simulated_data.head())
