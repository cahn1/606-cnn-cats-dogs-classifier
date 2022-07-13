import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
# import numpy as np
import tensorflow as tf

########### Define your variables ######

tabtitle = 'cats vs dogs'

# Load the trained model
model = tf.keras.models.load_model('modelrun_3epochs.h5')


######## Define helper functions


def make_prediction(img_file):
    # img = image.load_img(img_file, target_size=(64, 64))
    # img = tf.reshape(img,[1,64, 64,3])
    # img = tf.cast(img, tf.float32)
    # img=img/255
    img = tf.keras.preprocessing.image.load_img(img_file, target_size=(128, 128))

    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_reshape = tf.reshape(img_array,[1,128, 128,3])
    # img_array = np.array([img_array])  # Convert single image to a batch.
    # input_arr_reshape = np.reshape(input_arr,[1,64, 64,3]) # reshape to match expected format
    img_arr_normalized=img_reshape/255 # reduce min-max to 0-1
    y_pred = model.predict(img_arr_normalized)

    prediction = (y_pred>0.5).astype("int")
    classes=['DOG', 'CAT']
    dog_prob=round(y_pred[0][0].astype("float"),4)
    cat_prob=round(1-y_pred[0][0].astype("float"),4)
    return f"DOG probability: {dog_prob}, CAT probability: {cat_prob}"


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle


########### Set up the layout

app.layout = html.Div([
    html.H1('Cats vs Dogs!'),

    html.Button(children='Submit', id='submit-val', n_clicks=0,
                    style={
                    'background-color': 'red',
                    'color': 'white',
                    'margin-left': '5px',
                    'verticalAlign': 'center',
                    'horizontalAlign': 'center'}
                    ),
    html.Div(id='output-div'),

])

@app.callback(
    Output(component_id='output-div', component_property='children'),
    Input(component_id='submit-val', component_property='n_clicks'),
    )
def update_output_div(clicks):

    if clicks==0:
        return "waiting for inputs"
    else:
        return make_prediction('cat.jpg')


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
