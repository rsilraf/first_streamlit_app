import pandas as pd
import requests
import streamlit


streamlit.title("My Mom's New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list.set_index('Fruit', inplace=True)

# offer fruit option
fruits_selected = streamlit.multiselect('Pick some fruits:', 
    list(my_fruit_list.index), ['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected or my_fruit_list.index]

# display the table
streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice Fruit Advice!')

fruityvice_response = requests.get('https://fruityvice.com/api/fruit/watermelon')
streamlit.text(fruityvice_response.json())

# normalized it
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# output as table
streamlit.dataframe(fruityvice_normalized)
