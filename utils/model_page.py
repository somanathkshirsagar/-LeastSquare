from utils.libraries import *
from utils.functions import *
from utils import config

def compare_model_page(data):
    st.title("Let's Compare All Models")

    outliers = st.selectbox("**Remove outliers by?**", ["IQR", "Z-Score"])
    data = prepare_for_modeling(data, outliers)

    ohe = OneHotEncoder()
    ohe.fit(data[['Company', 'Car','Variant','Transmission','Owner_Type','Fuel']])

    column_trans = make_column_transformer(
        (OneHotEncoder(categories=ohe.categories_),['Company', 'Car','Variant','Transmission','Owner_Type','Fuel']),
        remainder='passthrough'
    )

    scaler = StandardScaler(with_mean=False)

    # Linear Regression
    lr = LinearRegression()

    st.write("""
        #### Linear Regression
    """)

    pipe = make_pipeline(column_trans, scaler, lr)
    metrics_df, lr = train_model(data, 'Price', pipe)
    st.dataframe(metrics_df)

    st.write("""
            #### Ridge Regression
        """)

    # Alpha values
    alphas = [0.005, 0.05, 0.1, 0.3, 1, 3, 5, 10, 15, 30, 80]

    alpha_r = st.selectbox("Select Alpha for Ridge", alphas)

    ridge = Ridge(alpha=int(alpha_r))
    pipe = make_pipeline(column_trans, scaler, ridge)
    metrics_df, lasso = train_model(data, 'Price', pipe)

    st.dataframe(metrics_df)

    st.write("""
            #### Lasso Regression
        """)

    alpha_l = st.selectbox("Select Alpha for Lasso", alphas)

    lasso = Lasso(alpha=alpha_l)
    pipe = make_pipeline(column_trans, scaler, lasso)
    metrics_df, lasso = train_model(data, 'Price', pipe)
    st.dataframe(metrics_df)

    ok = st.button("Save Regression Model")

    if ok:
        data = {"lr": lr, "ridge": ridge, "lasso": lasso}

        with open(config.model_pickle, 'wb') as file:
            pickle.dump(data, file)
