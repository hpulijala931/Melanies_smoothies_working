# Import necessary packages
import streamlit as st
import json
import pandas as pd
import requests  # To make API calls (if needed)
from snowflake.snowpark.functions import col

# Set up the Streamlit UI
st.title("Customise Your Smoothie 🥤")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

# Input fields for smoothie customization
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# Establish connection to Snowflake using st.connection
cnx = st.connection("snowflake")  # Ensure 'snowflake' matches the connection name in your Streamlit app settings
session = cnx.session()

# Retrieve fruit options from Snowflake and convert to Pandas DataFrame
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON")).to_pandas()
pd_df = my_dataframe  # Use pd_df as a version of my_dataframe

# Ingredient selection with a maximum of 5 options
ingredients_list = st.multiselect('Choose Up to 5 Ingredients:', pd_df['FRUIT_NAME'], max_selections=5)

# If ingredients are selected, prepare and display the order
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    st.write("Selected Ingredients:", ingredients_string)

    # Loop through each selected ingredient to fetch the "SEARCH_ON" value and display nutrition info
    for fruit_chosen in ingredients_list:
        # Get the "SEARCH_ON" value for the selected fruit
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        
        # Display the fruit and corresponding search value
        st.subheader(f"{fruit_chosen} Nutrition Information")
        
        # Example API call to Fruityvice (if available)
        # fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
        # For demonstration, replace with sample JSON if API is down
        try:
            fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
            fv_df = pd.DataFrame(fruityvice_response.json())  # Convert response to DataFrame
            st.dataframe(data=fv_df, use_container_width=True)  # Display nutrition info
        except:
            st.error("Unable to fetch data from Fruityvice. Please try again later.")
    
    # Prepare the SQL insert statement for storing the order in the database
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """
    st.write("SQL Insert Statement:", my_insert_stmt)

    # Button to submit the order
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
