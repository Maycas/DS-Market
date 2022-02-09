import pandas as pd
import plotly.express as px
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly


def clean_df(df_in):
    """
    Cleans and returns the 'df_in' dataframe to adapt it to prophet
    """
    df = df_in.copy()
    df.index.name = 'ds'
    df.columns = ['store', 'item', 'y']
    df.reset_index(inplace=True)
    df['ds'] = pd.to_datetime(df['ds'])
    return df


def filter_df(df, store=None, item=None):
    """
    Given a 'df' a 'store' identifier and an 'item' identifier it filters and prepares 
    its data to be ingested into prophet as a dataframe with columns ds (date) and y
    """
    if store and item:
        return df[(df.store == store) & (df.item == item)].drop(columns=['item', 'store'])
    elif store:
        return df[df.store == store].drop(columns=['item', 'store']).groupby('ds').sum().reset_index()
    elif item:
        return df[df.item == item].drop(columns=['item', 'store']).groupby('ds').sum().reset_index()
    else:
        print('A store and/or an item are mandatory')
        return None


def train_prophet(df, predict_periods, holidays_list=None):
    """
    Trains and predicts a model given a prepared 'df' for a number of
    'predict_periods' and also an optional 'holidays_list'.

    Returns a trained 'model' and the prediction 'forecast'
    """
    if holidays_list is None:
        model = Prophet()
    else:
        model = Prophet(holidays=holidays_list)
    model.fit(df)

    future = model.make_future_dataframe(periods=predict_periods)
    forecast = model.predict(future)

    return model, forecast


def plot_prophet_time_series(df, styles, model=None, forecast=None):
    """
    Given a 'df' containing the columns ds (dates) and y it plots a time series.

    If a 'model' and a 'forecast' are given, it uses prophets plotting methods to
    plot the predictions of the given 'model'.

    It additionally requires a styles dictionary with title and label (xaxes_label
    yaxes_label) information for the plotting
    """
    if model is None:
        fig = px.line(
            df,
            x='ds',
            y='y',
            hover_name='ds',
            title=styles['title']
        )
    else:
        fig = plot_plotly(model, forecast)

    if styles['xaxes_label']:
        fig.update_yaxes(title=styles['xaxes_label'])
    if styles['yaxes_label']:
        fig.update_yaxes(title=styles['yaxes_label'])

    fig.show()


def pipeline(df_in, predict_periods, store=None, item=None, holidays_list=None):
    """
    Executes the pipeline to create a model predictions for a 'df_in' dataframe,
    for a given 'predict_periods'.

    It requires either a 'store' code or an 'item' code to group data by.

    Optionally, a 'holiday_list' can be given to feed the model with holiday dates information
    """
    print('Cleaning Data...')
    df = clean_df(df_in)

    print('Selecting features...')
    df = filter_df(df, store=store, item=item)

    title = 'Daily number of sold items '
    if store:
        title += '(store = ' + store + ') '
    if item:
        title += '(item = ' + item + ')'

    plot_prophet_time_series(
        df,
        {
            'title': title,
            'xaxes_label': 'Date',
            'yaxes_label': 'Number of Sales'
        }
    )

    print('Training model...')
    model, forecast = train_prophet(df, predict_periods, holidays_list)

    plot_prophet_time_series(
        df,
        {
            'xaxes_label': 'Date',
            'yaxes_label': 'Total Income'
        },
        model,
        forecast
    )

    plot_components_plotly(model, forecast).show()

    return df
