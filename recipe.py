import streamlit as st
from surprise import Dataset, Reader, SVD
import pandas as pd
import openai

# Load the dataset
df = pd.read_csv('final_data.csv')

# Set up OpenAI API
openai.api_key = "your_openai_api_key"

# Define Streamlit app content
def streamlit_app():
    # Set page width and background color
    st.set_page_config(page_title="Recipe Search App", layout="wide", page_icon="🥘", initial_sidebar_state="expanded")

    # Create a Streamlit app
    st.title('Recipe Search App')
    st.markdown(
        """
        <style>
        body {
            background-color: #000000; /* Set background color to black */
            color: #FFFFFF; /* Set text color to white */
        }
        .css-1aumxhk {
            background-color: #000000; /* Set sidebar background color to black */
            color: #FFFFFF; /* Set sidebar text color to white */
        }
        .css-1aumxhk a {
            color: #FFFFFF; /* Set sidebar link color to white */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create navigation sidebar with custom colors
    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Go to', ['Home', 'About', 'Search'])

    # Display content based on selected page
    if page == 'Home':
        st.write('Welcome to Recipe Search App!')
        st.write('Use the navigation on the left to explore.')
    elif page == 'About':
<<<<<<< HEAD
        st.write('This app helps you search for recipes.')
        st.write('The app returns recipes based on search terms if recipe name is not there it will return recipe name not found')
        st.write('It uses a machine learning model to recommend recipes based on your input.')
    elif page == 'Search':
        st.title('Recipe Search')
=======
        st.write('This app helps users to search for recipes by key in `Recipe Name`.')
        st.write('Key in `User ID` which is any integer.')
        st.write('It uses a machine learning model to recommend top 10 recipes based on high ratings.')
    elif page == 'Results':
        st.title('Recipe Search Results')
>>>>>>> 42eb58c8ded7649dc650010f83e7f2acfc1aeccc

        # Add text input for entering search term
        search_term = st.text_input('Enter Search Term:')
        search_button = st.button('Search')
<<<<<<< HEAD

        # Initialize a session state to keep track of displayed recipe names
        if 'displayed_recipe_names' not in st.session_state:
            st.session_state.displayed_recipe_names = set()

        # Filter recipes based on search term and display the results
        if search_term:
            filtered_recipe = df[df['recipe_name'].str.contains(search_term, case=False)]
            if not filtered_recipe.empty:
                for _, row in filtered_recipe.iterrows():
                    if row['recipe_name'] not in st.session_state.displayed_recipe_names:
                        st.session_state.displayed_recipe_names.add(row['recipe_name'])  # Add recipe name to displayed recipe names
                        st.markdown(f"**Recipe Name:** {row['recipe_name']}")
                        st.write(f"**Predicted Rating:** {row['ratings']}")
                        st.markdown(f"**Ingredients:** {row['ingredients']}")
                        st.markdown(f"**Cooking Instructions:** {row['cooking_instructions']}")
                        st.write('---')
            else:
                st.write("Recipe name not found.")
=======
        # Get recommendations for the user
        if user_id and recipe_name:
            recommended_recipe = get_recommendations(int(user_id), df)
            for recipe_code, predicted_rating in recommended_recipe[:10]:
                recipe_name = df[df['recipe_code'] == recipe_code]['recipe_name'].iloc[0]
                ingredients = df[df['recipe_code'] == recipe_code]['ingredients'].iloc[0]
                # Check if cooking instructions exist before accessing them
                if 'cooking_instructions' in df.columns and not df[df['recipe_code'] == recipe_code]['cooking_instructions'].empty:
                    cooking_instructions = df[df['recipe_code'] == recipe_code]['cooking_instructions'].iloc[0]
                    st.write(f"Recipe Name: {recipe_name}")
                    
                    st.write(f"Predicted Rating: {predicted_rating}")
                    st.write(f"Ingredients: {ingredients}")
                    st.write(f"Cooking Instructions: {cooking_instructions}")
                else:
                    st.write(f"Recipe Name: {recipe_name}")
                    st.write(f"Predicted Rating: {predicted_rating}")
                    st.write(f"Ingredients: {ingredients}")
                    st.write("Cooking Instructions not available for this recipe.")
>>>>>>> 42eb58c8ded7649dc650010f83e7f2acfc1aeccc

# Run the Streamlit app
if __name__ == "__main__":
    streamlit_app()
