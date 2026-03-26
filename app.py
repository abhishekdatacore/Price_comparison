import serpapi
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def compare(product_name):
    params = {
        "engine": "google_shopping",
        "q": product_name,
        "api_key": "7b4f1c879e1ceea1cb33f35be6e42637a3c0f9e9687389c37d8a756708bd6348",
        "gl": "in"
    }
    search = serpapi.GoogleSearch(params)
    results = search.get_dict()
    search_data=results["shopping_results"]
    return search_data

#header

c1,c2 =st.columns(2)
c1.image("picture.png", width= 600)
c2.header("Price comparison system")


#"""----------------------------------------------------------------------------------------------------------"""

st.sidebar.title("Compare prices of your Product :")
Product_name =st.sidebar.text_input("Enter Your Product Name here ️⬇️ : ")
number = st.sidebar.text_input("Enter number of options here ⬇️ : ")
product_comp=[]
pro_price=[]

if Product_name is not None:
    if st.sidebar.button("compare Prices"):
        shopping_results = compare(Product_name)
        st.sidebar.image(shopping_results[0].get("thumbnail"))
        lowest_price = float(shopping_results[0].get("price")[1:].replace("₹","").replace(",", "").strip())
        lowest_price_index = 0

#"""---------------------------------------------------------------------------------------"""

        for i in range(int(number)):
            current_price =float((shopping_results[i].get('price'))[1:].replace("₹","").replace(",", "").strip())
            product_comp.append(shopping_results[i].get('source'))
            pro_price.append(current_price)

        #----------------------------------------------------------------------------------
            st.title(f"Option {i + 1}")
            c1, c2 = st.columns(2)
            c1.write("Company : ")
            c2.write(shopping_results[i].get('source'))

            c1.write("Title : ")
            c2.write(shopping_results[i].get('title'))

            c1.write("Price : ")
            c2.write(shopping_results[i].get('price'))

            url = shopping_results[i].get('product_link')
            c1.write("Buy Link : ")
            c2.markdown(f'<a href="{url}" target="_blank">Link</a>', unsafe_allow_html=True)


#"""---------------------------------------------------------------------------------"""

            if current_price <= lowest_price:
                lowest_price = current_price
                lowest_price_index = i

        # This is Best Option to buy
        st.title("Best option to buy")
        c1, c2 = st.columns(2)
        c1.write("Company : ")
        c2.write(shopping_results[lowest_price_index].get('source'))

        c1.write("Title : ")
        c2.write(shopping_results[lowest_price_index].get('title'))

        c1.write("Price : ")
        c2.write(shopping_results[lowest_price_index].get('price'))

        url = shopping_results[lowest_price_index].get('product_link')
        c1.write("Buy Link : ")
        c2.markdown(f'<a href="{url}" target="_blank">Link</a>', unsafe_allow_html=True)


# ------------------------------------------------------------------------------------------
        #Graphs comparison

        df = pd.DataFrame({"Price": pro_price}, index=product_comp)
        st.title("Chart Comparison : ")
        st.bar_chart(df)

        fig, ax = plt.subplots()
        ax.pie(pro_price, labels=product_comp, shadow=True, startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
