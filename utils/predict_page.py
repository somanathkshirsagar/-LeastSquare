from utils.libraries import *
from utils.functions import load_model
from utils import config


def show_predict_page(data):
    st.title("Predict the Price of Your Car")

    st.write("""### We need some information""")

    company_list = data["Company"].unique().tolist()
    Company = st.selectbox("**Car Company Name**", company_list)

    car_list = data[data["Company"] == Company]["Car"].unique().tolist()
    Car = st.selectbox("**Which Car?**", car_list)

    variant_list = data[(data["Company"] == Company) & (data["Car"] == Car)]["Variant"].unique().tolist()
    Variant = st.selectbox("**Variant**", variant_list)

    fuel_list = data[(data["Company"] == Company) & (data["Car"] == Car) & (data["Variant"] == Variant)]["Fuel"].unique().tolist()
    Fuel = st.selectbox("**Fuel Type**", fuel_list)

    transmission_list = data[(data["Company"] == Company) & (data["Car"] == Car) & (data["Variant"] == Variant)]["Transmission"].unique().tolist()
    Transmission = st.radio("**Transmission Type**", transmission_list)

    km_driven = st.number_input('**Kilometer Driven**', 1000, 10000000)

    owner_list = data["Owner_Type"].unique().tolist()
    Owner_Type = st.selectbox("**Owner Type**", owner_list)
    
    Year = st.number_input('**Purchased In**', 2000, date.today().year)
    Age = date.today().year - Year

    model_list = [
        "Linear Regression",
        "Ridge Regression",
        "Lasso Regression"
    ]

    model = st.selectbox("**Select Model**", model_list)

    ok = st.button("Calculate Price")

    if ok:

        dict_ = {
            "Company": [Company],
            "Car": [Car],
            "Variant": [Variant],
            "Transmission": [Transmission],
            "km_driven":[km_driven],
            "Owner_Type": [Owner_Type],
            "Fuel": [Fuel],
            "Age": [Age]
        }

        results = pd.DataFrame(dict_)

        data = load_model(config.model_pickle)
        lr_loaded = data["lr"]
        ridge_loaded = data["ridge"]
        lasso_loaded = data["lasso"]

        if model == "Linear Regression":
            price = lr_loaded.predict(results)
        elif model == "Ridge Regression":
            price = ridge_loaded.predict(results)
        elif model == "Lasso Regression":
            price = lasso_loaded.predict(results)

        st.subheader(f"The estimated price of your Car is &#8377; {price[0]:,.0f}")
