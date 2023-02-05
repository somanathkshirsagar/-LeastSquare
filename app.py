from utils.functions import feature_engineering
from utils.predict_page import show_predict_page
from utils.explore_page import show_explore_page
from utils.model_page import compare_model_page
from utils.libraries import *
from utils import config


def side_menu():
    try:
        data = pd.read_csv(config.main_data)
        data = feature_engineering(data)
    except NameError:
        print("Some problem with file...")

    page = st.sidebar.selectbox("Explore Or Predict Or Else", ("Understanding the Data", "Compare Models", "Predict"))

    if page == "Understanding the Data":
        show_explore_page(data)
    elif page == "Compare Models":
        data.dropna(inplace=True)
        compare_model_page(data)
    elif page == "Predict":      
        show_predict_page(data)


if __name__ == '__main__':
    side_menu()
