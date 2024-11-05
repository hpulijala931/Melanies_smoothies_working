# Import necessary packages
import streamlit as st
import json
import pandas as pd  # Import pandas
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

# Rename DataFrame for clarity
pd_df = my_dataframe  # Use pd_df as a version of my_dataframe

# Ingredient selection with a maximum of 5 options
ingredients_list = st.multiselect('Choose Up to 5 Ingredients:', pd_df['FRUIT_NAME'], max_selections=5)

# If ingredients are selected, prepare and display the order
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    st.write("Selected Ingredients:", ingredients_string)

    # Retrieve and display the "SEARCH_ON" values for each selected ingredient
    search_values = []
    for fruit_chosen in ingredients_list:
        # Get the "SEARCH_ON" value for the selected fruit
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        search_values.append(search_on)
        st.write('The search value for', fruit_chosen, 'is', search_on)

    # Prepare the SQL insert statement with the chosen ingredients
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
