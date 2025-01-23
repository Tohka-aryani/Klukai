import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px

# Set page configuration for full width
st.set_page_config(page_title="Anime Explorer App", layout="wide")

st.markdown(
    """
    <style>
    .centered-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load CSV data
def load_data():
    file_path = "Tohka AMG - Anime List.csv"
    return pd.read_csv(file_path)

# App Pages
def introduction_page():
    st.markdown("<h2 style='text-align: center;'>Welcome to Tohka's Anime Repository</h2>", unsafe_allow_html=True)

    st.image("p9YwXL5.png", use_container_width=True)

    st.markdown("<p style='text-align: center;'>This is the place where I'll be putting all of my current list of animes as well as statistics.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Navigate through the app using the menu on the sidebar:</p>", unsafe_allow_html=True)
    st.markdown("<ul style='text-align: center;'><strong>Anime List</strong>: Filter and search for your favorite anime.", unsafe_allow_html=True)
    st.markdown("<ul style='text-align: center;'><strong>Statistics</strong>: ind answers to commonly asked questions about this app.", unsafe_allow_html=True)
    st.markdown("<ul style='text-align: center;'><strong>FAQ</strong>: ind answers to commonly asked questions about this app.", unsafe_allow_html=True)

def anime_list_page(data):
    st.write("## Anime List")

    search_query = st.text_input("Search for an anime:", "")
    genre_filter = st.selectbox("Filter by Genre:", ["All"] + sorted(set(genre.strip() for sublist in data['Genre'].dropna().str.split(',') for genre in sublist)))
    watch_status_filter = st.selectbox("Filter by Watch Status:", ["All"] + list(data['Watch Status'].unique()))

    filtered_data = data

    if search_query:
        filtered_data = filtered_data[filtered_data['Title'].str.contains(search_query, case=False, na=False)]
    
    if genre_filter != "All":
        # Filter rows where the selected genre is present in the Genre column
        filtered_data = filtered_data[filtered_data['Genre'].str.contains(fr'\b{genre_filter}\b', case=False, na=False)]
    
    if watch_status_filter != "All":
        filtered_data = filtered_data[filtered_data['Watch Status'] == watch_status_filter]

    def render_image(url):
        return f'<img src="{url}" width="200" style="border-radius:5px;">' if pd.notna(url) else ''

    if 'Image' in filtered_data.columns:
        filtered_data['Image'] = filtered_data['Image'].apply(render_image)

    # Add CSS to center-align all table content except the Image column
    st.markdown(
        """
        <style>
        .styled-table th, .styled-table td {
            text-align: center !important;
        }
        .styled-table td:nth-child(3) {
            text-align: left !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.write(f"### {len(filtered_data)} results found")
    st.markdown(
        filtered_data.to_html(escape=False, index=False, classes="styled-table"),
        unsafe_allow_html=True
    )




def faq_page():
    st.write("## Frequently Asked Questions (FAQ)")
    st.write("### How do I search for an anime?")
    st.write("Use the search bar on the Anime List page to find specific titles.")
    st.write("### Why did you give this anime a low rating & etc?")
    st.write("All ratings are subjective and based on my personal preference only.")
    st.write("### How can I filter the anime list?")
    st.write("You can filter the anime list by genre or watch status using the dropdown menus.")
    st.write("### What should I do if I encounter an issue?")
    st.write("Please contact @tohka_aryani [that's me] for any issues or feedback.")

def statistics_page(data):
    st.write("## Anime Statistics")

    # Bar chart for Watch Status
    watch_status_count = data['Watch Status'].value_counts()
    fig_watch_status = px.bar(watch_status_count, 
                              x=watch_status_count.index, 
                              y=watch_status_count.values, 
                              labels={'x': 'Watch Status', 'y': 'Count'}, 
                              title="Watch Status Distribution")
    fig_watch_status.update_traces(text=watch_status_count.values, textposition='outside')
    st.plotly_chart(fig_watch_status)

    # Pie chart for Type
    type_count = data['Type'].value_counts()
    fig_type = px.pie(type_count, 
                      names=type_count.index, 
                      values=type_count.values, 
                      title="Type Distribution", 
                      hole=0.4)
    fig_type.update_traces(textinfo='label+percent+value')
    st.plotly_chart(fig_type)

    # Bar chart for Rating based on Release Year
    if 'Release Year' in data.columns and 'Rating' in data.columns:
        rating_year = data.groupby('Release Year')['Rating'].mean().reset_index()
        fig_rating_year = px.bar(rating_year, 
                                 x='Release Year', 
                                 y='Rating', 
                                 labels={'Release Year': 'Release Year', 'Rating': 'Average Rating'}, 
                                 title="Average Rating by Release Year")
        fig_rating_year.update_traces(text=rating_year['Rating'].round(2), textposition='outside')
        st.plotly_chart(fig_rating_year)

# Main App
def main():
    data = load_data()

    with st.sidebar:
        selected = option_menu(
            "Main Menu",
            ["Introduction", "Anime List", "Statistics", "FAQ"],
            icons=["house", "list", "bar-chart", "question-circle"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important"},
                "icon": {"font-size": "20px"},
                "nav-link": {"font-size": "16px", "padding": "10px 15px"},
                "nav-link-selected": {"background-color": "#D8BFD8"},
            }
        )

    if selected == "Introduction":
        introduction_page()
    elif selected == "Anime List":
        anime_list_page(data)
    elif selected == "Statistics":
        statistics_page(data)
    elif selected == "FAQ":
        faq_page()

if __name__ == "__main__":
    main()
