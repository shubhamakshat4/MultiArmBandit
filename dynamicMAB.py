import numpy as np
import pandas as pd

# Load simulated dataset
# Assuming the dataset generated earlier is saved as 'simulated_lead_distribution.csv'
simulated_data = pd.read_csv("simulated_lead_distribution.csv")

# Parameters for Multi-Armed Bandit
num_agents = 100
num_days = 100
leads_per_day = 1000
min_leads = 3  # Minimum leads to be allocated to an agent
max_leads = 25  # Maximum leads to be allocated to an agent

# Initialize Thompson Sampling parameters
# For each agent, maintain success (alpha) and failure (beta) counts
alpha = np.ones(num_agents)  # Prior successes
beta = np.ones(num_agents)   # Prior failures

# Record allocation and results
results = []

for day in range(1, num_days + 1):
    # Sample conversion rates for each agent from their Beta distributions
    sampled_conversion_rates = np.random.beta(alpha, beta)

    # Calculate lead allocation proportional to sampled conversion rates
    total_sample = np.sum(sampled_conversion_rates)
    lead_allocations = (sampled_conversion_rates / total_sample) * leads_per_day

    # Apply minimum and maximum lead constraints
    lead_allocations = np.clip(lead_allocations, min_leads, max_leads)

    # Normalize lead allocations to ensure total leads remain consistent
    lead_allocations = (lead_allocations / np.sum(lead_allocations)) * leads_per_day

    # Simulate leads and sales for each agent based on allocations
    daily_data = simulated_data[simulated_data['Day'] == day]  # Fetch actual data for the day
    for agent_id in range(1, num_agents + 1):
        allocated_leads = lead_allocations[agent_id - 1]

        # Fetch the true conversion rate from the simulated data (ground truth)
        true_conversion_rate = daily_data[daily_data['Agent_ID'] == agent_id]['Conversion_Rate'].values[0]

        # Calculate actual sales based on true conversion rate
        actual_sales = allocated_leads * true_conversion_rate

        # Update alpha and beta based on observed results
        alpha[agent_id - 1] += actual_sales
        beta[agent_id - 1] += allocated_leads - actual_sales

        # Record results
        results.append({
            "Day": day,
            "Agent_ID": agent_id,
            "Leads_Allocated": allocated_leads,
            "True_Conversion_Rate": true_conversion_rate,
            "Sales_Closed": actual_sales
        })

# Create a DataFrame for the results
mab_results = pd.DataFrame(results)

# Save results to a CSV file (optional)
mab_results.to_csv("dynamic_mab_results4.csv", index=False)

# Display the first few rows of the results
print(mab_results.head())
