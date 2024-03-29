import pandas as pd
import requests
import streamlit
import snowflake.connector
from urllib.error import URLError

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

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get('https://fruityvice.com/api/fruit/'+this_fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error('Please select a fruit to get information.')
    else:
        # streamlit.write('The user entered', fruit_choice)
        # output as table
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error(e)

#streamlit.stop()


#my_cur = my_cnx.cursor()
## my_cur.execute('select current_user(), current_account(), current_region()')
#my_cur.execute('SELECT * FROM fruit_load_list')
#my_data_row = my_cur.fetchall()
#streamlit.text('The fruit load list contains:')
#streamlit.dataframe(my_data_row)

#fruit_choice_add = streamlit.text_input('What fruit would you like to add?')
#my_data_row.append([fruit_choice])
#streamlit.text(f'Thanks for adding {fruit_choice_add}')
#my_cur.execute('insert into fruit_load_list values("from streamlit")')


def get_fruit_load_list(my_cnx):
    with my_cnx.cursor() as my_cur:
        my_cur.execute('select * from fruit_load_list')
        return my_cur.fetchall()
#
streamlit.header('View Our Fruit List - Add Your Favorites')
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])
    my_data_rows = get_fruit_load_list(my_cnx)
    my_cnx.close()
    streamlit.dataframe(my_data_rows)


def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute(f"insert into fruit_load_list values('{new_fruit}')")
        return f'Thanks for adding {new_fruit}'

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets['snowflake'])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)



html_string = "<h3>this is an html string</h3>"

streamlit.markdown(html_string, unsafe_allow_html=True)

html_string = f'''
    <details>
        <summary>hello</summary>
        <p> content paragraph </p>
        <ul>
            <li>one</li>
            <li>two</li>
            <li>three</li>
        </ul>
        <p>Diagram</p>
        <img src="https://kroki.io/plantuml/svg/eNpzKC5JLCopTyrm0opWzi9KzEtPjVVwSS1IzUtJzUuuVAgpSk3l0tJSCAly0wsLj3fx9I0PCPJ3CXUOiXcK9XPxceXS0tKKV0hMSbHCo8YhNS-lPKkYAIzaIhw=" />
    </details>
'''
streamlit.markdown(html_string, unsafe_allow_html=True)