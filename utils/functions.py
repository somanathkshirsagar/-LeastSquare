from utils.libraries import *
from utils import config


def find_number(text):
    """
    Extracts integers from text. 
    Returns a string of Numbers.

    Parameters :
    -----------
    text: string
    """

    num = re.findall(r'[0-9]+',text)
    return "".join(num)


def feature_engineering(cars):
    """
    Does Feature Engineering.
    And Returns a Clean Dataframe.

    Parameters :
    -----------
    cars: pandas.DataFrame - DataFrame on which you wish to perform Feature Engineering.
    """

    # First seven columns are relevant
    cars = cars.iloc[:,:7]

    # Giving Proper names to features
    cars.rename(columns = {'Title':'Name', 'cvakb':'Variant', 'cvakb1':'Transmission', 'bvr0c':'km_driven', 'bvr0c2':'Owner_Type', 'bvr0c3':'Fuel', '_7udzz':'Price'}, inplace = True)

    # Extracting only numbers
    cars["Price"] = cars["Price"].apply(lambda x: find_number(x))

    # Extracting year of purchase from Name
    cars['Year_Purchased'] = [' '.join(x.split(' ')[0:1]) for x in cars['Name']]

    # Extracting name excluding year of purchase
    cars['Company'] = [' '.join(x.split(' ')[1:2]) for x in cars['Name']]

    cars['Car'] = [' '.join(x.split(' ')[2:]) for x in cars['Name']]

    # Removing "km"
    cars["km_driven"] = cars["km_driven"].str.split().str.slice(start=0,stop=1).str.join(' ')

    # Extracting only numbers
    cars["km_driven"] = cars["km_driven"].apply(lambda x: find_number(x))

    # Removing Transmission type from the end of Variant
    cars['Variant'] = [' '.join(x.split(' ')[:-1]) for x in cars['Variant']]

    # Converting features to int
    cars = cars.astype({"km_driven":"int","Price":"int", "Year_Purchased":"int"})

    # Deriving Age of Vehical from Year of Purchase
    cars["Age"] = date.today().year - cars["Year_Purchased"]
    cars.drop(['Year_Purchased', 'Name'], axis=1, inplace=True)

    return cars


# For converting big values into readable form
def format_float(num):
    return np.format_float_positional(round(num, 2), trim='-')


# Returns Dataframe consisting all errors
def metrics(y_test, y_pred, X_train):
    """
    Returns a Dataframe containing MAE, MSE, RMSE, R2, Adj R2.

    Parameters :
    -----------
    y_test: pandas.Series - Target Test values.
    y_pred: pandas.Series - Target Predicted values.
    X_train: pandas.Series - Input Train values.
    """

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    # Number of rows
    n = len(X_train)

    # Number of Independent Features
    k = len(X_train.columns)

    adj_r2 = 1- ((1-r2) * (n-1)/(n-k-1))

    dict_ = {
        "MAE": [format_float(mae)],
        "MSE": [format_float(mse)],
        "RMSE": [format_float(rmse)],
        "R2": [(r2)],
        "Adjusted-R2": [(adj_r2)]
    }

    results = pd.DataFrame(dict_)
    results.index = ["Values"]

    return results


# For Training model
def train_model(data, target, pipe):
    """
    Does,
    1. OneHotEncoding
    2. Scaling
    3. Model Fitting

    Returns a Dataframe containing MAE, MSE, RMSE, R2, Adj R2.

    Parameters :
    -----------
    data: pandas.Dataframe - Independent Features.
    target: string - Target column name.
    pipe
    """

    X = data.drop(columns =[target])
    y = data[target]

    X_train, x_test, Y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
    pipe.fit(X_train, Y_train)
    y_pred = pipe.predict(x_test)
    
    return metrics(y_test, y_pred, X_train), pipe


def prepare_for_modeling(data, outliers):
    
    if outliers == 'Z-Score':
        data['zscore'] = (data['Price'] - data['Price'].mean()) / data['Price'].std()
        data = data[(data['zscore'] > -3) & (data['zscore'] < 3)]
        del data["zscore"]

    elif outliers == 'IQR':
        Q1, Q3 = np.percentile(data['Price'], [25, 75])
        IQR = Q3-Q1
        lower_fence = Q1 - (1.5*IQR)
        higher_fence = Q3 + (1.5*IQR)
        data = data[(data['Price'] > lower_fence) & (data['Price'] < higher_fence)]

    return data


# For Loading the Pickle File
def load_model(PATH):
    with open(PATH, 'rb') as file:
        data = pickle.load(file)
    return data
