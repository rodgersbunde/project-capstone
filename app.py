import streamlit as st
from surprise import Dataset, Reader, SVD
import pandas as pd

# Load the dataset
df = pd.read_csv('merged_data.csv')

# Load collaborative filtering model
reader = Reader(rating_scale=(0, 100))
data = Dataset.load_from_df(df[['user_id', 'recipe_code', 'ratings']], reader)
trainset = data.build_full_trainset()
algo = SVD()
algo.fit(trainset)

# Function to get recommendations for a user
def get_recommendations(user_id, df):
    user_recipe = df[df['user_id'] == user_id]['recipe_code'].unique()
    recommended_recipe = []
    for recipe_code in df['recipe_code'].unique():
        if recipe_code not in user_recipe:
            predicted_ratings = algo.predict(user_id, recipe_code).est
            recommended_recipe.append((recipe_code, predicted_ratings))
    recommended_recipe.sort(key=lambda x: x[1], reverse=True)
    return recommended_recipe

# Create a Streamlit app
st.title('Recipe Recommendation App')

# Create navigation sidebar with custom colors
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ['Home', 'About', 'Results'])

# Display content based on selected page
if page == 'Home':
    st.write('Welcome to Recipe Search App!')
    st.write('Use the navigation on the left to explore.')
elif page == 'About':
    st.write('This app helps you search for recipes.')
    st.write('It uses a machine learning model to recommend recipes based on your input.')
elif page == 'Results':
    st.title('Recipe Search Results')

    # Add text inputs for entering user ID and recipe name
    user_id = st.text_input('Enter User ID:')
    recipe_name = st.text_input('Enter Recipe Name:')

    # Get recommendations for the user
    if user_id and recipe_name:
        recommended_recipe = get_recommendations(int(user_id), df)
        for recipe_code, predicted_rating in recommended_recipe[:10]:
            recipe_name = df[df['recipe_code'] == recipe_code]['recipe_name'].iloc[0]
            ingredients = df[df['recipe_code'] == recipe_code]['ingredients'].iloc[0]
            st.write(f"Recipe Name: {recipe_name}, Recipe code: {recipe_code}, Predicted Rating: {predicted_rating}, Ingredients: {ingredients}")


if __name__ == '__main__':
    st.run()