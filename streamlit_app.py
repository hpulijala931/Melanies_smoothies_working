# Import necessary packages
import streamlit as st
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

# Retrieve fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME")).to_pandas()  # Convert to pandas DataFrame for compatibility with Streamlit

# Ingredient selection with a maximum of 5 options
ingredients_list = st.multiselect('Choose Up to 5 Ingredients:', my_dataframe['FRUIT_NAME'], max_selections=5)

# If ingredients are selected, prepare and display the order
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    st.write("Selected Ingredients:", ingredients_string)

    # Prepare the SQL insert statement
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

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
