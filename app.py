import streamlit as st
from serpapi import GoogleSearch
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch shopping results
def compare(med_name):
    params = {
        "engine": "google_shopping",
        "q": med_name,
        "location": "India",
        "google_domain": "google.co.in",
        "api_key": "bacd6640ba78bf7a2ea9c5bdc2121e5e134c602316677976d7bd26692befe029"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results.get('shopping_results', [])
    return shopping_results

# Header
c1, c2 = st.columns(2)
c1.image("comparison_image.png", width=250)
c2.header("MEDICINE PRICE COMPARISON SYSTEM")

# Sidebar input
st.sidebar.title("Enter the Name of Medicine ⚕️")
med_name = st.sidebar.text_input("Enter Name of Medicine Here 👇 :")
number = st.sidebar.text_input("Enter Number of Options Here 👇 :")

# Initialize lists
shopping_results = []
medicine_comp = []
med_price = []

if med_name:
    if st.sidebar.button('Compare Price'):

        # Spinner while fetching data
        with st.spinner("Please wait while we are fetching prices... ⏳"):
            shopping_results = compare(med_name)

        if shopping_results:
            number = int(number) if number and number.isdigit() else 5

            # Initialize lowest price
            price_str = shopping_results[0].get('price', '')
            lowest_price = float(price_str.replace("₹","").replace("$","").replace(",","").strip())
            lowest_price_index = 0

            # Show first product thumbnail in sidebar
            thumbnail = shopping_results[0].get('thumbnail')
            if thumbnail:
                st.sidebar.image(thumbnail)

            # Loop through results
            for i in range(min(number, len(shopping_results))):
                price_str = shopping_results[i].get('price', '')
                current_price = float(price_str.replace("₹","").replace("$","").replace(",","").strip())

                # Append for chart
                medicine_comp.append(shopping_results[i].get('source'))
                med_price.append(current_price)

                # Update lowest price
                if current_price < lowest_price:
                    lowest_price = current_price
                    lowest_price_index = i

                # Display option details
                st.subheader(f"Option {i+1}")
                c1, c2 = st.columns(2)
                c1.write("Company Name")
                c2.write(shopping_results[i].get('source'))

                c1.write("Title")
                c2.write(shopping_results[i].get('title'))

                c1.write("Price")
                c2.write(f"₹{current_price}")

                url = shopping_results[i].get('product_link')
                c1.write("Click Here To Buy 👉 :")
                c2.write(f"[Link]({url})")

            # Best option
            st.subheader("Best option to buy :")
            best = shopping_results[lowest_price_index]
            c1, c2 = st.columns(2)
            c1.write("Company Name")
            c2.write(best.get('source'))

            c1.write("Title")
            c2.write(best.get('title'))

            best_price_str = best.get('price', '')
            best_price = float(best_price_str.replace("₹","").replace("$","").replace(",","").strip())
            c1.write("Price")
            c2.write(f"₹{best_price}")

            url = best.get('product_link')
            c1.write("Click Here To Buy 👉 :")
            c2.write(f"[Link]({url})")

            # Chart comparison
            df = pd.DataFrame({'Company': medicine_comp, 'Price': med_price})

            st.title("Chart Comparison:")
            st.bar_chart(df.set_index('Company'))

            fig, ax = plt.subplots()
            ax.pie(med_price, labels=medicine_comp, shadow=True, autopct='%1.1f%%')
            ax.axis("equal")
            st.pyplot(fig)

        else:
            st.warning("No shopping results found for this medicine.")

else:
    st.warning("Please enter a medicine name.")
