import pandas as pd
import numpy as np

def acs_cleaning(acs_filepath): 
    acs_data = pd.read_csv(acs_filepath)
    acs_data = acs_data.loc[acs_data.loc[:,'county'] == 31,] 
    acs_data.loc[:,'geoid10'] = acs_data.loc[:,'geo_id'].str.split('1400000US',expand=True).loc[:,1]
    acs_data.loc[:,'geoid10'] = acs_data.loc[:,'geoid10'].astype('int')
    invalid_values = [-666666666, -999999999]
    non_changeable_cols = ["tract", "county", "geo_id", "census_name", "state", "geoid10"]
    cols_mod = [ col for col in acs_data.columns if col not in non_changeable_cols]
    acs_data.loc[:, cols_mod] = acs_data.loc[:, cols_mod].replace(invalid_values, np.nan)
    return acs_data

def acs_merge(acs_data, joined_df):
    joined_df.loc[:,'geoid10'] = joined_df.loc[:,'geoid10'].astype('int')
    libs_tracts = joined_df.loc[:,['name','geoid10']].drop_duplicates()
    libs_tracts.rename(columns={'name':'lib_name'},inplace = True)
    libs_tracts = libs_tracts.loc[~libs_tracts.loc[:,'lib_name'].isnull(),]

    non_changeable_cols = ["tract", "county", "geo_id", "census_name", "state", "geoid10"]
    acs_cols = ['geoid10','tract'] + [ col for col in acs_data.columns if col not in non_changeable_cols]
    merged_df = pd.merge(libs_tracts,acs_data.loc[:,acs_cols], on = 'geoid10', how="left")
    return merged_df

def acs_agg(acs_data, merged_df): 
    id_vars = ['tract','county','geo_id','census_name','state','geoid10'] #variables that are identifiers (no aggregation)
    avg_vars = (['median_age','perc_hh_w_children','avg_household_size',
                'avg_family_size','unemployment_rate','median_hh_income_d',
                'average_hh_income_d','per_capita_income_d','perc_fam_bellow_poverty',
                'perc_ppl_bellow_poverty','median_owner_cost_unit_mortgage_d',
                'median_owner_cost_unit_no_mortgage_d','occupied_median_rent_d'])
    sum_vars = [col for col in acs_data.columns if col not in avg_vars + id_vars]
    sum_dict = {var : 'sum' for var in sum_vars}
    avg_dict = {var : 'mean' for var in avg_vars}

    sum_df = merged_df.groupby('lib_name', as_index=False).agg(sum_dict)
    avg_df = merged_df.groupby('lib_name', as_index=False).agg(avg_dict)

    agg_df = pd.merge(sum_df,avg_df, on = 'lib_name', how = 'inner')
    agg_df.loc[:,'share_men'] = agg_df.loc[:,'total_male']/agg_df.loc[:,'total_population']
    agg_df.loc[:,'share_women'] = agg_df.loc[:,'total_female']/agg_df.loc[:,'total_population']
    return agg_df

def acs_join(acs_data, joined_df): 
    merged_df = acs_merge(acs_data, joined_df)
    agg_df = acs_agg(acs_data, merged_df)
    return agg_df