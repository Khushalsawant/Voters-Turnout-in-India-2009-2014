# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 20:04:39 2019

@author: khushal
"""

import matplotlib.pyplot as plt
import io
import pandas as pd
import time

start_time = time.time()

pd.set_option('display.max_columns',1000)
img = io.BytesIO()
plt.style.use('ggplot')


path_of_input_file = "C:/Users/khushal/Documents/Python Scripts/Election To The Lok Sabha (House of people), 2014 - States.csv"
input_data_df = pd.read_csv(path_of_input_file)
print(input_data_df.columns)


# Setting the positions and width for the bars
pos = list(range(len(input_data_df['State/UT']))) 
width = 0.35     
# Plotting the bars
fig, ax = plt.subplots(figsize=(10,30))

# Create a bar with pre_score data,
# in position pos,
plt.bar(pos, 
        #using df['pre_score'] data,
        input_data_df['Percentage of votes polled-2014'], 
        # of width
        width, 
        # with alpha 0.5
        alpha=0.9, 
        # with color
        color='#EE3224', 
        # with label the first value in first_name
        label=input_data_df['State/UT'][0]) 

# Create a bar with mid_score data,
# in position pos + some width buffer,
plt.bar([p + width for p in pos], 
        #using df['mid_score'] data,
        input_data_df['Percentage of votes polled-2009'],
        # of width
        width, 
        # with alpha 0.5
        alpha=0.9, 
        # with color
        color='#F78F1E', 
        # with label the second value in first_name
        label=input_data_df['State/UT'][1]) 

# Set the y axis label
ax.set_ylabel('State/UT')
# Set the chart's title
ax.set_title('Percentage of votes polled 2009 & 2014')
# Set the position of the x ticks
ax.set_xticks([p + 1.5 * width for p in pos])
# Set the labels for the x ticks
ax.set_xticklabels(input_data_df['State/UT'],rotation=90)
# Setting the x-axis and y-axis limits
plt.xlim(min(pos)-width, max(pos)+width*4)


for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() * 1.025, p.get_height() * 1.005)) 
    
plt.grid()
plt.show()

from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.plotting import figure
from bokeh.models.widgets import Panel, Tabs

output_file("voters_turnout_2014_&_2009.html")

mean_voters_turnout_2014 = round(input_data_df['Percentage of votes polled-2014'].mean(),2)
mean_voters_turnout_2009 = round(input_data_df['Percentage of votes polled-2009'].mean(),2)

print("mean_voters_turnout_2014 =",mean_voters_turnout_2014,'\n',"mean_voters_turnout_2009 = ",mean_voters_turnout_2009)
states = input_data_df['State/UT'].tolist()
voters_turnout_2014 = input_data_df['Percentage of votes polled-2014'].tolist()
voters_turnout_2009 = input_data_df['Percentage of votes polled-2009'].tolist()
sorted_states = sorted(states, key=lambda x: voters_turnout_2014[states.index(x)])
sorted_states_2009 = sorted(states, key=lambda x: voters_turnout_2009[states.index(x)])

ColumnDataSource(data=input_data_df)


source_2009 = ColumnDataSource(data=dict(x=states, y=voters_turnout_2009))
labels_2009 = LabelSet(x='x', y='y', text='y', level='glyph',
        text_font_size='8pt',text_baseline='top',angle=90,angle_units='deg',
        x_offset=-8.5, y_offset=0, source=source_2009, render_mode='canvas')

p_2009 = figure(x_range=sorted_states_2009,y_range=[0,100],
            tools=["pan","wheel_zoom","save","reset"],
           title="Percentage of votes polled 2009",width=900)
p_2009.vbar(x=states, top=voters_turnout_2009, #source=source_2009,
       #source=source_2014,
       width=0.75, color='red')

#p.title.text ='Percentage of votes polled 2009 & 2014'
#p_2009.xaxis.axis_label = 'State/UT'
p_2009.title.text ="Overall Voters Turnout in India-2009 is " + str(mean_voters_turnout_2009)
p_2009.yaxis.axis_label = '% of Voters Turnout'
p_2009.xaxis.major_label_orientation = "vertical"
p_2009.toolbar.logo = None

#p_2009.sizing_mode = 'scale_width'
p_2009.add_layout(labels_2009)
# Make a tab with the layout 
tab_2009 = Panel(child=p_2009, title = 'Voters Turnout - 2009')


source_2014 = ColumnDataSource(data=dict(x=states, y=voters_turnout_2014))

labels_2014 = LabelSet(x='x', y='y', text='y', level='glyph',
        text_font_size='8pt',text_baseline='top',angle=90,angle_units='deg',
        x_offset=-8.5, y_offset=0, source=source_2014, render_mode='canvas')

p_2014 = figure(x_range=sorted_states,y_range=[0,100],
        tools=["pan","wheel_zoom","save","reset"],
        title="Percentage of votes polled 2014",width=900)
p_2014.vbar(x=states, top=voters_turnout_2014,
       #source=source_2014,
       width=0.75, color='red')

p_2014.title.text ="Overall Voters Turnout in India-2014 is " + str(mean_voters_turnout_2014)
p_2014.yaxis.axis_label = '% of Voters Turnout'
p_2014.xaxis.major_label_orientation = "vertical"
p_2014.toolbar.logo = None
p_2014.add_layout(labels_2014)
#p_2014.sizing_mode = 'scale_width'

tab_2014 = Panel(child=p_2014, title = 'Voters Turnout - 2014')

tabs = Tabs(tabs=[tab_2009,tab_2014])
show(tabs)


print("--- %s  = Total execution time seconds ---" % (time.time() - start_time))