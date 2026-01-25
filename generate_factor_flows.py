"""
Generate factor flow data for the USEEIO Flow Analysis visualization.
Based on Hertwich et al. (2024) Hypothetical Extraction Method.

This script extracts:
- Dollar flows (from A matrix)
- Environmental indicators (GHG, Energy, Water, Waste, etc.)
- Economic indicators (Value Added, Jobs)
"""

import pandas as pd
import numpy as np
import json

# Configuration
EXCEL_PATH = 'data/USEEIOv2.0.1-411.xlsx'
OUTPUT_PATH = 'factor_flows_data.json'

# Key indicators to include (subset of 23 available)
KEY_INDICATORS = {
    'Greenhouse Gases': {
        'code': 'GHG',
        'unit': 'kg CO2 eq',
        'unit_display': 'Mt CO2 eq',
        'scale': 1e-9,  # kg to Mt
        'group': 'Environmental',
        'color': '#dc2626',
        'threshold_pct': 0.0001
    },
    'Value Added': {
        'code': 'VADD',
        'unit': '$',
        'unit_display': 'Billion $',
        'scale': 1e-9,  # $ to billion $
        'group': 'Economic',
        'color': '#16a34a',
        'threshold_pct': 0.0001
    },
    'Jobs Supported': {
        'code': 'JOBS',
        'unit': 'jobs',
        'unit_display': 'Thousand Jobs',
        'scale': 1e-3,  # jobs to thousands
        'group': 'Economic',
        'color': '#2563eb',
        'threshold_pct': 0.0001
    },
    'Energy Use': {
        'code': 'ENRG',
        'unit': 'MJ',
        'unit_display': 'TJ',
        'scale': 1e-6,  # MJ to TJ (terajoules)
        'group': 'Environmental',
        'color': '#ea580c',
        'threshold_pct': 0.0001
    },
    'Freshwater withdrawals': {
        'code': 'WATR',
        'unit': 'kg',
        'unit_display': 'Billion kg',
        'scale': 1e-9,  # kg to billion kg
        'group': 'Environmental',
        'color': '#0ea5e9',
        'threshold_pct': 0.0001
    },
    'Land use': {
        'code': 'LAND',
        'unit': 'm2*yr',
        'unit_display': 'Thousand km²',
        'scale': 1e-9,  # m² to thousand km²
        'group': 'Environmental',
        'color': '#84cc16',
        'threshold_pct': 0.0001
    },
    'Commercial Municipal Solid Waste': {
        'code': 'CMSW',
        'unit': 'kg',
        'unit_display': 'Mt',
        'scale': 1e-9,
        'group': 'Waste',
        'color': '#a855f7',
        'threshold_pct': 0.0001
    },
    'Commercial Construction and Demolition Debris': {
        'code': 'CCDD',
        'unit': 'kg',
        'unit_display': 'Mt',
        'scale': 1e-9,
        'group': 'Waste',
        'color': '#f97316',
        'threshold_pct': 0.0001
    },
    'Commercial RCRA Hazardous Waste': {
        'code': 'CRHW',
        'unit': 'kg',
        'unit_display': 'kt',
        'scale': 1e-6,
        'group': 'Waste',
        'color': '#ef4444',
        'threshold_pct': 0.0001
    },
    'Smog Formation Potential': {
        'code': 'SMOG',
        'unit': 'kg O3 eq',
        'unit_display': 'kt O3 eq',
        'scale': 1e-6,
        'group': 'Environmental',
        'color': '#8b5cf6',
        'threshold_pct': 0.0001
    },
    'Human Health - Respiratory Effects': {
        'code': 'HRSP',
        'unit': 'kg PM2.5 eq',
        'unit_display': 'kt PM2.5 eq',
        'scale': 1e-6,
        'group': 'Health',
        'color': '#ec4899',
        'threshold_pct': 0.0001
    },
    'Acidification Potential': {
        'code': 'ACID',
        'unit': 'kg SO2 eq',
        'unit_display': 'kt SO2 eq',
        'scale': 1e-6,
        'group': 'Environmental',
        'color': '#f59e0b',
        'threshold_pct': 0.0001
    }
}

def load_useeio_data():
    """Load USEEIO matrices from Excel file."""
    print("Loading USEEIO data...")
    xlsx = pd.ExcelFile(EXCEL_PATH)
    
    data = {
        'A': pd.read_excel(xlsx, 'A', index_col=0),      # Technical coefficients
        'D': pd.read_excel(xlsx, 'D', index_col=0),      # Direct indicator coefficients
        'N': pd.read_excel(xlsx, 'N', index_col=0),      # Total multipliers
        'x': pd.read_excel(xlsx, 'x', index_col=0),      # Total output
        'indicators': pd.read_excel(xlsx, 'indicators'),
        'commodities': pd.read_excel(xlsx, 'commodities_meta')
    }
    
    print(f"Loaded {len(data['A'])} sectors")
    return data

def get_sector_metadata(data):
    """Extract sector names and classifications."""
    commodities = data['commodities']
    sectors = []
    
    # Sector mapping from NAICS codes to readable names
    naics_to_sector = {
        '11': 'Agriculture, Forestry, Fishing',
        '21': 'Mining',
        '22': 'Utilities',
        '23': 'Construction',
        '31': 'Manufacturing',
        '32': 'Manufacturing',
        '33': 'Manufacturing',
        '42': 'Wholesale Trade',
        '44': 'Retail Trade',
        '45': 'Retail Trade',
        '48': 'Transportation',
        '49': 'Transportation',
        '51': 'Information',
        '52': 'Finance & Insurance',
        '53': 'Real Estate',
        '54': 'Professional Services',
        '55': 'Management',
        '56': 'Admin & Waste Services',
        '61': 'Education',
        '62': 'Healthcare',
        '71': 'Arts & Entertainment',
        '72': 'Accommodation & Food',
        '81': 'Other Services',
        '92': 'Government',
        'S0': 'Government',
        'F0': 'Other Activities',
    }
    
    for idx, row in commodities.iterrows():
        code = row['Code']
        if '/US' not in code:
            code = f"{code}/US"
        
        # Extract sector from Category or Code
        category = str(row.get('Category', ''))
        
        # Try to get sector from category (format: "XX: Sector Name/...")
        sector_name = 'Other'
        if ': ' in category:
            # Extract the main sector from category string
            parts = category.split('/')
            if parts:
                first_part = parts[0]
                if ': ' in first_part:
                    sector_name = first_part.split(': ')[1].strip()
                    # Simplify long sector names
                    if 'Agriculture' in sector_name:
                        sector_name = 'Agriculture, Forestry, Fishing'
                    elif 'Manufacturing' in sector_name or sector_name.startswith('3'):
                        sector_name = 'Manufacturing'
        
        # Fallback: use NAICS code prefix
        if sector_name == 'Other':
            code_prefix = row['Code'][:2]
            sector_name = naics_to_sector.get(code_prefix, 'Other')
        
        sectors.append({
            'id': idx,
            'code': code,
            'name': row['Name'],
            'sector': sector_name,
            'output': float(data['x'].iloc[idx].values[0]) / 1e9  # Convert to billions
        })
    
    return sectors

def calculate_dollar_flows(data, threshold=0.05):
    """
    Calculate inter-industry dollar flows.
    Flow from i to j = A[i,j] * x[j]
    
    Accounting identity for sector j:
    - Intermediate Inputs + Value Added = Total Output = Intermediate Sales + Final Demand
    """
    A = data['A'].values
    x = data['x'].values.flatten()
    
    flows = []
    n = len(A)
    
    # Calculate all flows (for complete accounting)
    all_flows_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            all_flows_matrix[i, j] = A[i, j] * x[j] / 1e9  # Convert to billions
    
    # Calculate sector totals for accounting
    sector_accounts = {}
    for j in range(n):
        total_output = x[j] / 1e9
        intermediate_inputs = np.sum(all_flows_matrix[:, j])  # Column sum = inputs to j
        intermediate_sales = np.sum(all_flows_matrix[j, :])   # Row sum = sales from j
        value_added = total_output - intermediate_inputs
        final_demand = total_output - intermediate_sales
        
        sector_accounts[j] = {
            'total_output': round(total_output, 4),
            'intermediate_inputs': round(intermediate_inputs, 4),
            'intermediate_sales': round(intermediate_sales, 4),
            'value_added': round(value_added, 4),
            'final_demand': round(final_demand, 4)
        }
    
    # Extract flows above threshold
    for i in range(n):
        for j in range(n):
            value = all_flows_matrix[i, j]
            if value >= threshold:
                flows.append({
                    'from': i,
                    'to': j,
                    'value': round(value, 3)
                })
    
    # Sort by value descending
    flows.sort(key=lambda x: -x['value'])
    
    print(f"Dollar flows: {len(flows)} (threshold: ${threshold}B)")
    return flows, sector_accounts

def calculate_factor_flows(data, indicator_name, indicator_config):
    """
    Calculate factor flows for a given indicator using proper IO accounting.
    
    Uses the N matrix (total multipliers) for consistent accounting.
    N = D * L (direct coefficients × Leontief inverse)
    
    For a target sector t:
    
    INPUT SIDE:
    - Embodied in inputs: Σ_i(N_i * z_it) = total factors from supply chains
    - Direct factor by t: d_t * x_t = factors generated by t's production
    - Total: N_t * x_t (this equals embodied + direct by construction)
    
    OUTPUT SIDE:
    - Factor to intermediate j: N_t * z_tj
    - Factor to final demand: N_t * y_t
    - Total: N_t * x_t
    
    BALANCE: Embodied + Direct = N_t * x_t = To Intermediates + To Final Demand
    """
    A = data['A'].values
    D = data['D']
    N = data['N']  # Total multipliers (D * L)
    x = data['x'].values.flatten()
    scale = indicator_config['scale']
    threshold_pct = indicator_config.get('threshold_pct', 0.0001)
    
    # Get indicator coefficients
    if indicator_name not in D.index:
        print(f"Warning: {indicator_name} not found in D matrix")
        return [], 0, {}
    
    d = D.loc[indicator_name].values  # Direct factor intensity
    
    # Get total multiplier from N matrix
    if indicator_name not in N.index:
        print(f"Warning: {indicator_name} not found in N matrix, using D")
        n_total = d  # Fallback to direct
    else:
        n_total = N.loc[indicator_name].values  # Total factor intensity (N = D*L)
    
    n_sectors = len(A)
    
    # Calculate inter-industry dollar flows z_ij = A_ij * x_j
    dollar_flow_matrix = np.zeros((n_sectors, n_sectors))
    for i in range(n_sectors):
        for j in range(n_sectors):
            dollar_flow_matrix[i, j] = A[i, j] * x[j]
    
    # Calculate sector accounts for proper balancing
    sector_accounts = {}
    
    for t in range(n_sectors):
        # Direct factor use by sector t
        direct_factor = d[t] * x[t] * scale
        
        # Embodied in inputs using TOTAL multipliers from suppliers
        # = Σ_i(N_i * z_it) = total supply chain factors in purchased inputs
        embodied_in_inputs = sum(n_total[i] * dollar_flow_matrix[i, t] * scale for i in range(n_sectors))
        
        # Total factor content of t's output (using N matrix)
        total_factor_output = n_total[t] * x[t] * scale
        
        # Dollar flows out of t
        intermediate_sales_dollars = sum(dollar_flow_matrix[t, j] for j in range(n_sectors))
        final_demand_dollars = x[t] - intermediate_sales_dollars
        
        # Factor flows out using total multiplier
        if final_demand_dollars >= 0:
            factor_to_intermediates = n_total[t] * intermediate_sales_dollars * scale
            factor_to_final_demand = n_total[t] * final_demand_dollars * scale
        else:
            # Negative final demand: all domestic output goes to intermediates
            factor_to_intermediates = total_factor_output
            factor_to_final_demand = 0.0
        
        total_factor_out = factor_to_intermediates + factor_to_final_demand
        
        sector_accounts[t] = {
            'direct_factor': round(direct_factor, 6),
            'embodied_in_inputs': round(embodied_in_inputs, 6),
            'total_factor_output': round(total_factor_output, 6),
            'total_multiplier': round(n_total[t] * scale * 1e9, 6),  # per billion $
            'factor_to_intermediates': round(factor_to_intermediates, 6),
            'factor_to_final_demand': round(factor_to_final_demand, 6),
            'total_factor_out': round(total_factor_out, 6)
        }
    
    # Calculate factor flows between sectors using total multipliers
    # Flow from i to j = N_i * z_ij (total embodied factor in the flow)
    factor_flow_matrix = np.zeros((n_sectors, n_sectors))
    for i in range(n_sectors):
        for j in range(n_sectors):
            factor_flow_matrix[i, j] = n_total[i] * dollar_flow_matrix[i, j] * scale
    
    # Calculate total factor and threshold
    total_factor = np.sum([d[i] * x[i] * scale for i in range(n_sectors)])
    threshold = total_factor * threshold_pct
    
    # Extract flows above threshold for visualization
    flows = []
    for i in range(n_sectors):
        for j in range(n_sectors):
            if i != j:  # Exclude self-flows for cleaner visualization
                value = factor_flow_matrix[i, j]
                if value >= threshold:
                    flows.append({
                        'from': i,
                        'to': j,
                        'value': round(value, 6)
                    })
    
    # Sort by value descending
    flows.sort(key=lambda x: -x['value'])
    
    # Keep top flows (limit for performance)
    max_flows = 5000
    flows = flows[:max_flows]
    
    print(f"{indicator_config['code']}: {len(flows)} flows, total: {total_factor:.2f} {indicator_config['unit_display']}")
    
    return flows, total_factor, sector_accounts

def calculate_sector_totals(data, sectors):
    """Calculate direct factor totals for each sector."""
    D = data['D']
    x = data['x'].values.flatten()
    
    for sector in sectors:
        idx = sector['id']
        sector['factors'] = {}
        
        for ind_name, ind_config in KEY_INDICATORS.items():
            if ind_name in D.index:
                d = D.loc[ind_name].values
                direct_value = d[idx] * x[idx] * ind_config['scale']
                sector['factors'][ind_config['code']] = round(direct_value, 6)
    
    return sectors

def main():
    # Load data
    data = load_useeio_data()
    
    # Get sector metadata
    sectors = get_sector_metadata(data)
    sectors = calculate_sector_totals(data, sectors)
    
    # Calculate flows
    flow_types = {}
    sector_accounts = {}  # Proper accounting for each sector
    
    # Dollar flows
    dollar_flows, dollar_accounts = calculate_dollar_flows(data, threshold=0.1)
    flow_types['dollars'] = {
        'name': 'Dollar Flows',
        'code': 'USD',
        'unit': 'Billion USD',
        'group': 'Economic',
        'color': '#2563eb',
        'top_flows': dollar_flows
    }
    sector_accounts['dollars'] = dollar_accounts
    
    # Factor flows for each indicator
    for ind_name, ind_config in KEY_INDICATORS.items():
        code = ind_config['code']
        flows, total, factor_accounts = calculate_factor_flows(data, ind_name, ind_config)
        
        flow_types[code] = {
            'name': ind_name,
            'code': code,
            'unit': ind_config['unit_display'],
            'group': ind_config['group'],
            'color': ind_config.get('color', '#888888'),
            'total': round(total, 4),
            'top_flows': flows
        }
        
        sector_accounts[code] = factor_accounts
    
    # Build output data
    output = {
        'industries': sectors,
        'flow_types': flow_types,
        'sector_accounts': sector_accounts,  # Proper IO accounting per sector
        'indicator_metadata': {
            code: {
                'name': name,
                'unit': config['unit'],
                'unit_display': config['unit_display'],
                'group': config['group'],
                'color': config.get('color', '#888888')
            }
            for name, config in KEY_INDICATORS.items()
            for code in [config['code']]
        }
    }
    
    # Add USD to metadata
    output['indicator_metadata']['USD'] = {
        'name': 'Dollar Flows',
        'unit': 'USD',
        'unit_display': 'Billion USD',
        'group': 'Economic',
        'color': '#2563eb'
    }
    
    # Save to JSON
    print(f"\nSaving to {OUTPUT_PATH}...")
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output, f)
    
    # Print summary
    print("\n=== Summary ===")
    print(f"Sectors: {len(sectors)}")
    print(f"Flow types: {len(flow_types)}")
    for ft_name, ft_data in flow_types.items():
        print(f"  - {ft_name}: {len(ft_data['top_flows'])} flows")
    
    # Print sample accounting verification
    print("\n=== Sample Sector Accounting (sector 0) ===")
    print("Dollars:", sector_accounts['dollars'].get(0, {}))
    print("GHG:", sector_accounts.get('GHG', {}).get(0, {}))
    
    # File size
    import os
    size_mb = os.path.getsize(OUTPUT_PATH) / 1e6
    print(f"\nOutput file size: {size_mb:.2f} MB")

if __name__ == '__main__':
    main()
