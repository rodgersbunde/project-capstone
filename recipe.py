import streamlit as st
from surprise import Dataset, Reader, SVD
import pandas as pd
import openai

# Set your OpenAI API key here
api_key = "your_openai_api_key"
openai.api_key = api_key

# Load the dataset
df = pd.read_csv('final_data.csv')

# Load collaborative filtering model
reader = Reader(rating_scale=(0, 100))
data = Dataset.load_from_df(df[['user_id', 'recipe_code', 'ratings']], reader)
trainset = data.build_full_trainset()
algo = SVD()
algo.fit(trainset)

# Function to generate recipe using OpenAI
def generate_recipe(search_term):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Generate a recipe for {search_term}"}
        ],
        max_tokens=1024,
        n=1,
        stop=None,
    )
    generated_recipe = response['choices'][0]['message']['content']
    return generated_recipe

# Define Streamlit app content
def streamlit_app():
    # Set page width and background color
    st.markdown(
        """
        <style>
        body {
            background-image: url('https://img.freepik.com/premium-photo/food-cooking-background-stone-texture-with-sea-salt-pepper-garlic-parsley-light-grey-abstract-food-background-empty-space-text-can-be-used-food-posters-design-menu-top-view_253362-16400.jpg');
            background-size: cover;
            background-position: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create a Streamlit app
    st.title('Recipe Search App')

    # Create navigation sidebar with custom colors
    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Go to', ['Home', 'About', 'Search'])

    # Display content based on selected page
    if page == 'Home':
        st.write('Welcome to Recipe Search App!')
        st.write('Use the navigation on the left to explore.')
    elif page == 'About':
        st.write('This app helps you search for recipes.')
        st.write('The app returns recipes based on search terms. If a recipe name is not found, it will generate a new recipe.')
        st.write('It uses a machine learning model to recommend recipes based on your input.')
    elif page == 'Search':
        st.title('Recipe Search')

        # Add text input for entering search term
        search_term = st.text_input('Enter Search Term:')
        search_button = st.button('Search')

        # Add ingredient search input
        ingredient_search = st.text_input('Search by Ingredients (comma separated):')
        ingredient_search_button = st.button('Search by Ingredients')

        # Initialize a session state to keep track of displayed recipe names
        if 'displayed_recipe_names' not in st.session_state:
            st.session_state.displayed_recipe_names = set()

        # Filter recipes based on search term and display the results
        if search_term and search_button:
            with st.spinner('Searching for recipes...'):
                filtered_recipe = df[df['recipe_name'].str.contains(search_term, case=False)]
                if not filtered_recipe.empty:
                    for _, row in filtered_recipe.iterrows():
                        if row['recipe_name'] not in st.session_state.displayed_recipe_names:
                            st.session_state.displayed_recipe_names.add(row['recipe_name'])
                            st.markdown(f"**Recipe Name:** {row['recipe_name']}")
                            st.write(f"**Predicted Rating:** {algo.predict('user_id', row['recipe_code']).est}")
                            st.markdown(f"**Ingredients:** {row['ingredients']}")
                            st.markdown(f"**Cooking Instructions:** {row['cooking_instructions']}")
                            st.write('---')
                else:
                    st.write("Recipe name not found. Generating a new recipe...")
                    generated_recipe = generate_recipe(search_term)
                    st.write(generated_recipe)

        # Filter recipes based on ingredients and display the results
        if ingredient_search and ingredient_search_button:
            with st.spinner('Searching for recipes...'):
                ingredients = [ingredient.strip() for ingredient in ingredient_search.split(',')]
                filtered_recipes = df[df['ingredients'].str.contains('|'.join(ingredients), case=False, na=False)]

                if not filtered_recipes.empty:
                    for _, row in filtered_recipes.iterrows():
                        if row['recipe_name'] not in st.session_state.displayed_recipe_names:
                            st.session_state.displayed_recipe_names.add(row['recipe_name'])
                            st.markdown(f"**Recipe Name:** {row['recipe_name']}")
                            st.write(f"**Predicted Rating:** {algo.predict('user_id', row['recipe_code']).est}")
                            st.markdown(f"**Ingredients:** {row['ingredients']}")
                            st.markdown(f"**Cooking Instructions:** {row['cooking_instructions']}")
                            st.write('---')
                else:
                    st.write("No recipes found with the given ingredients. Generating a new recipe...")
                    generated_recipe = generate_recipe(", ".join(ingredients))
                    st.write(generated_recipe)

# Run the Streamlit app
if __name__ == "__main__":
    streamlit_app()
