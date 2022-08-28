# example using climate data using hvPlot
# following the arcticle at:
# https://levelup.gitconnected.com/guide-to-creating-interactive-visualizations-in-python-78f79ffc7d61

import pandas as pd
import panel as pn
from panel.template import DefaultTheme
import hvplot.pandas
from ipywidgets import widgets, interact, interactive, fixed, interact_manual
from IPython.display import display

raw_data_at = pd.read_csv('C:/Users/erpasten/Documents/UEF/PET/dataframes/df_raw_at.csv')

raw_at = raw_data_at.rename(columns={'Unnamed: 0':'Days since 01/01/1971'})
raw_at.plot(kind='scatter', x='Days since 01/01/1971', y='Penman', color='blue', grid=True, title='Daily Penman PET (mm/day)')


pd.options.plotting.backend = 'holoviews'

raw_at_plot = raw_at.plot(kind='scatter', x='Days since 01/01/1971', y='Penman', color='blue', grid=True, title='Daily Penman PET (mm/day)')

#alternative method
raw_at.hvplot.scatter(x='Days since 01/01/1971', y='Penman', color='blue', grid=True, title='Daily Penman PET (mm/day)')
raw_at.hvplot.scatter(x='Days since 01/01/1971', y='Oudin', color='red', grid=True, title='Daily Penman PET (mm/day)')


climate_models = list(raw_at.CM.unique())

climate_model = pn.widgets.Select(name='Climate Model', options=climate_models)


# Create interactive dataframe
idf = raw_at.interactive()

data_pipeline = (
    idf[
        (idf.CM == climate_model) #|  (raw_at.CM == climate_model)
    ]
)


#Table
viz0 = data_pipeline[['CM', 'Site', 'Julian']].hvplot(kind='table',
                                                 title='Climate Models', 
                                                 width=600, height=400
                                                )
viz0

#Secondary scatter
viz1 = data_pipeline.hvplot(x='Penman', y='Penman_Montheit', 
                     by='CM', 
                     kind='scatter', 
                     hover_cols=['Site', 'CM', 'Month'], 
                     title='Relationship between Penman and Penman_Monteith, by Climate Model',
                     width=700, height=500,
                     grid=True,
                    )
viz1


# Generate template
template = pn.template.FastListTemplate(theme=DefaultTheme,
    title = 'Daily climate model PET projections',
    sidebar=[
        pn.pane.Markdown('# About the project'),
        pn.pane.Markdown('#### This project uses raw and processed climate model data from Euro-CORDEX'),
        #pn.pane.JPG('thimo-pedersen-dip9IIwUK6w-unsplash.jpg', sizing_mode='scale_both'),
        #pn.pane.Markdown('[Photo by Thimo Pedersen on Unsplash](https://unsplash.com/photos/dip9IIwUK6w)'),
        pn.pane.Markdown('## Filter by climate model'),
        climate_model
    ],
    main=[pn.Row(
                  pn.Column(viz0.panel(width=600, height=400, margin=(0,20))), 
                  pn.Column(pn.Row(viz1.panel(width=700, height=250, margin=(0,20)))),
                  ),
                            #pn.Column(viz2.panel(width=700, height=250), margin=(0,20))),
                 #),
          pn.Row(raw_at_plot.opts(width=1400, height=200))
    ],
    accent_base_color='#d78929',
    header_background='#d78929',
    #sidebar_footer='<br><br><a href="https://github.com/pcmaldonado/PokemonDashboard">GitHub Repository</a>',       
    main_max_width='100%'                                        
)

template.servable();
template.show()
