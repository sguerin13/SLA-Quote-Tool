import tkinter
import numpy as np
import keras
from keras.models import model_from_json
import json
import os
from sklearn.externals import joblib
import sklearn.preprocessing as preprocessing
from  sklearn.preprocessing import StandardScaler
from  sklearn.preprocessing import LabelEncoder
from  sklearn.preprocessing import OneHotEncoder 
from  sklearn.externals import joblib

cur_dir = os.getcwd()
# load json and create model
json_file = open(cur_dir + '\\Quote Tool Cleaned Data 1-17-19 R1.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("Quote Tool Cleaned Data 1-17-19 R1.h5")
print("Loaded model from disk")

# load the scalers
x_scaler = joblib.load("X_scaler.save")
y_scaler = joblib.load("Y_scaler.save")
lenc     = joblib.load("Lenc.save")
one_hot  = joblib.load("One_Hot.save")

def calc_cost():
    
    global volume
    global layer_var
    global resin_var
    global num_layer
    global hours
    global cost
    global post
    global units
    
    # global margin
    # global discount
    
    vol         = volume.get()
    layer_thick = layer_var.get()
    resin_type  = resin_var.get()
    layers      = num_layer.get()
    #print([layers,layer_thick,vol,resin_type])
    inputs = [layers,layer_thick,vol,resin_type]
    inputs[-1] = list(lenc.transform([inputs[-1]]))[:]
    inputs[-1] = inputs[-1][0]
    inputs = one_hot.transform([inputs]).toarray()
    inputs = x_scaler.transform(inputs)
    #print(inputs)
    
    pre_scaled_out = loaded_model.predict(inputs)
    #print(pre_scaled_out)
    hour = y_scaler.inverse_transform(pre_scaled_out)
    
    #print(hours)
    hours.delete(0,tkinter.END)
    hours.insert(0,np.round(hour[0][0],4)) # insert at first location location

    post_get = post.get()
    unit_get = units.get()
    vol_get  = volume.get()
    
    quote_total = np.round(5*hour[0][0] + 30*float(post_get)*int(unit_get) \
                           + 500*float(vol_get)/1000,2)
    #print(quote_total)
    cost.delete(0,tkinter.END)
    cost.insert(0,quote_total)

x = tkinter.Tk(screenName = 'SLA Quote Tool')
x.title('SLA QUOTE TOOL')
# Define the Entry Forms:

x.geometry("215x275")
tkinter.Label(x,text = 'Volume').place(x = 34,y = 20)
volume = tkinter.Entry(x)
volume.place(x = 85,y = 20)

calculate_button = tkinter.Button(x,text = 'Calculate',
                                  command = calc_cost).place(x = 115,y = 190)

tkinter.Label(x,text = 'Num_Layers').place(x = 10,y = 40)
num_layer = tkinter.Entry(x)
num_layer.place(x = 85,y = 40)

tkinter.Label(x,text = 'Units').place(x = 50,y = 60)
units = tkinter.Entry(x)
units.place(x = 85,y = 60)

tkinter.Label(x,text = 'Post Per Unit').place(x = 10,y = 80)
post = tkinter.Entry(x)
post.place(x = 85,y = 80)

tkinter.Label(x,text = 'Resin').place(x = 10,y = 100)
resin_var = tkinter.StringVar()
y_loc = 120
for item in ["Black", "Tough V5", "White V4", "Grey V4","Clear V4"]:
    resin_button = tkinter.Radiobutton(x,text = item,
                                       variable = resin_var,
                                       value = item)
    resin_button.place(x = 10,y = y_loc)
    y_loc = y_loc + 20

tkinter.Label(x,text = 'Layer Thickness').place(x = 110,y = 100)
layer_var = tkinter.StringVar()
y_loc = 120
for item in [25,50,100]:
    resin_button = tkinter.Radiobutton(x,text = item,
                                       variable = layer_var,
                                       value = item)
    resin_button.place(x = 110,y = y_loc)
    y_loc = y_loc + 20
    
tkinter.Label(x,text = 'Hours').place(x = 45,y = 225)
hours = tkinter.Entry(x)
hours.place(x = 85,y = 225)
    
tkinter.Label(x,text = 'Price').place(x = 50,y = 245)
cost = tkinter.Entry(x)
cost.place(x = 85,y = 245)

x.mainloop()