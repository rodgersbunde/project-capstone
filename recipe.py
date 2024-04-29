
import streamlit as st
import pickle

# Load recipes from pickle file
with open('top_recommendations.pkl', 'rb') as f:
    top_recommendations = pickle.load(f)

# Define Streamlit app content
def streamlit_app():
    st.title('Recipe Search App')

    # Add a text input for searching recipes
    search_recipe = st.text_input('Enter a recipe name:')

    # Handle search
    if search_recipe:
        if search_recipe in top_recommendations:
            ingredients, rating = top_recommendations[search_recipe]
            st.write(f"Recipe: {search_recipe}")
            st.write(f"Ingredients: {', '.join(ingredients)}")
            st.write(f"Rating: {rating}")
            
            # Render a template
            st.markdown("""
            ## Recipe Template

            <div style="background-color:#f5f5f5; padding:10px">
            <h3>Recipe: {recipe_name}</h3>
            <p><strong>Ingredients:</strong> {ingredient_list}</p>
            <p><strong>Rating:</strong> {recipe_rating}</p>
            </div>
            """.format(recipe_name=search_recipe, ingredient_list=', '.join(ingredients), recipe_rating=rating))
            
        else:
            st.write("Recipe not found.")
            
              

if __name__ == "__main__":
    streamlit_app()









