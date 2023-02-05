from utils.libraries import *


def show_explore_page(cars):

    st.title("Explore Cars Dataset")

    st.write(
        """
    ### Cars
    """
    )
    st.dataframe(cars.head())

    shape = cars.shape
    st.write("There are", shape[0], "rows and ", shape[1], "columns in the Dataset.")

    fig, ax = plt.subplots()
    ax = sns.set(rc={'figure.figsize': (8, 5)})
    plt.title("Heat Map for Missing Values")
    sns.heatmap(cars.isnull(), yticklabels=False, cbar=False, cmap='viridis')
    st.pyplot(fig)

    cars.dropna(inplace=True)

    st.write("""
        #### Exploratory Data Analysis
        """)

    fig, ax = plt.subplots()
    ax = sns.set(rc={'figure.figsize': (10, 8)})
    plt.title("Countplot Owner Type Vs Number of Cars")
    sns.countplot(x ='Owner_Type', data = cars)
    st.pyplot(fig)

    st.write("""
        **Observation**

        **First Owned Cars** are **highest among all**.
    """)

    fig, ax = plt.subplots()
    ax = sns.set(rc={'figure.figsize': (10, 8)})
    plt.title("Type of Owner Vs Number of cars")
    plt.pie(cars['Owner_Type'].value_counts(),labels=cars['Owner_Type'].unique(),pctdistance=1.1, labeldistance=1.2,autopct='%.2f')
    st.pyplot(fig)

    st.write("""
        **Observation**

        1. **79.75 %** of cars are **First Owned**.
        2. **19.46 %** of cars are **Second Owned**.
        3. **0.79 %** of cars are **Third Owned**.
    """)

    fig, ax = plt.subplots()
    ax = sns.set(rc={'figure.figsize': (10, 8)})
    plt.title("Owner Type Vs Price")
    sns.barplot(x='Owner_Type',y='Price',data=cars,palette='spring')
    st.pyplot(fig)

    st.write("""
        **Observation**

        **First Owner cars** have **high average selling price**. 

        As **number of owners** increases the **selling price** of car **decreases**.
    """)

    fig, ax = plt.subplots()
    ax = sns.set(rc={'figure.figsize': (10, 8)})
    plt.title("Transmission Vs Number of Cars")
    sns.countplot(x ='Transmission', data = cars)
    st.pyplot(fig)

    st.write("""
        **Observation**

        Most of the cars are **Manual**.
    """)

    fig, ax = plt.subplots()
    ax = sns.set(rc={'figure.figsize': (10, 8)})
    plt.title("Transmission Vs Selling Price")
    sns.barplot(x='Transmission',y='Price',data=cars,palette='spring')
    st.pyplot(fig)

    st.write("""
        **Observation**

        Cars having **Automatic Transmission have high selling price**.
    """)

    fig, ax = plt.subplots()
    ax = sns.set(rc={'figure.figsize': (10, 8)})
    plt.title("Fuel Vs Number of Cars")
    sns.countplot(x ='Fuel', data = cars)
    st.pyplot(fig)

    st.write("""
        **Observation**

        Most of the cars are **Petrol**.
    """)

    fig, ax = plt.subplots()
    ax = sns.set(rc={'figure.figsize': (10, 8)})
    plt.title("Fuel Vs Price")
    sns.barplot(x='Fuel',y='Price',data=cars,palette='spring')
    st.pyplot(fig)

    st.write("""
        **Observation**

        **Diesel cars** have **high average selling price**.
    """)

    fig, ax = plt.subplots()
    ax = sns.set(rc={'figure.figsize': (10, 8)})
    plt.title("Fuel Vs Selling Price")
    sns.barplot(x ='Age', y="Price", data = cars ,palette='spring')
    st.pyplot(fig)

    st.write("""
        **Observation**

        As the age of Vehical increases, Price Decreases.
    """)