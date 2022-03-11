import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px

from scipy.stats import chisquare

data = pd.read_excel('./HamlineData.xlsx')
data['total'] = data.Blue + data.Green + data.Pink + data.Purple + data.Yellow

data['blue_perc'] = data.Blue / data.total
data['green_perc'] = data.Green / data.total
data['pink_perc'] = data.Pink / data.total
data['purple_perc'] = data.Purple / data.total
data['yellow_perc'] = data.Yellow / data.total

total_blue_perc = data.Blue.sum() / data.total.sum()
total_green_perc = data.Green.sum() / data.total.sum()
total_pink_perc = data.Pink.sum() / data.total.sum()
total_purple_perc = data.Purple.sum() / data.total.sum()
total_yellow_perc = data.Yellow.sum() / data.total.sum()

data_long = pd.melt(data, id_vars=['Grade'], value_vars=[
                    'Blue', 'Green', 'Pink', 'Purple', 'Yellow'])

st.set_page_config(layout="wide")

st.markdown("""<style>
.css-fk4es0 {
    position: absolute;
    top: 0px;
    right: 0px;
    left: 0px;
    height: 0.5rem;
    background-image: linear-gradient(
90deg, rgb(52, 152, 219), rgb(194, 224, 244));
    z-index: 1000020;
}
</style>""", unsafe_allow_html=True)

with st.container():
  st.title('Hamline M&M Data - Analytics & Data Science')
  st.markdown('''Let's explore the frequencies of colors in our m&m data! 
  This app is made using Streamlit, Plotly, and Pandas in Python. This is only a small
  example of what we can do with data science.''')

  st.markdown(f"**So far, {data.shape[0]} students have participated in Hamline M&M Data Study.**")

  c1, c2, c3, c4, c5, c6 = st.columns(6)
  with c1:
    st.metric('Blue', f"{round(total_blue_perc * 100, 1)}%")
  with c2:
    st.metric('Green', f"{round(total_green_perc * 100, 1)}%")
  with c3:
    st.metric('Pink', f"{round(total_pink_perc * 100, 1)}%")
  with c4:
    st.metric('Purple', f"{round(total_purple_perc * 100, 1)}%")
  with c5:
    st.metric('Yellow', f"{round(total_yellow_perc * 100, 1)}%")
  with c6:
    st.metric('Average per Bag', data.total.sum() // data.shape[0])

st.subheader('Your M&M Data')

num = st.number_input("How many students do you want to see?", min_value=1, max_value=data.shape[0])
display_data = data.tail(num)

st.table(display_data[['Blue', 'Green', 'Pink', 'Purple', 'Yellow', 'total']])

display_data_show = st.checkbox('Whole Data', value=False)

if display_data_show:
  fig = px.bar(data_long.groupby('variable').sum().reset_index(), x='variable', y='value', color='variable', text_auto=True,
              color_discrete_map={'Blue': '#3498DB', 'Green': 'green', 'Pink': 'pink', 'Purple': 'purple', 'Yellow': 'yellow'})
  fig.update_layout(title='Frequency of Colors in M&M Data')
  fig.update_xaxes(title_text='Color')
  fig.update_yaxes(title_text='Frequency')
  fig.update_layout(showlegend = False)
  fig.add_hline(y=data.total.sum()/5, line_color='orange', line_width=2)

  st.plotly_chart(fig)

else:
  display_data_long = pd.melt(display_data, id_vars=['Grade'], value_vars=['Blue', 'Green', 'Pink', 'Purple', 'Yellow'])

  fig = px.bar(display_data_long.groupby('variable').sum().reset_index(), x='variable', y='value', color='variable', text_auto=True,
               color_discrete_map={'Blue': '#3498DB', 'Green': 'green', 'Pink': 'pink', 'Purple': 'purple', 'Yellow': 'yellow'})
  fig.update_layout(title='Frequency of Colors in **Your** M&M Data')
  fig.update_xaxes(title_text='Color')
  fig.update_yaxes(title_text='Frequency')
  fig.update_layout(showlegend=False)

  st.plotly_chart(fig)

st.write('---')

st.subheader('Chi-Square Test')
st.markdown('''Let's see if the frequencies of colors in our data are statistically significant. 
That means that we are checking to see if the frequencies of each color are significantly different from beign the same.''')

st.markdown(r'''We will use the [Chi-Square Test](https://en.wikipedia.org/wiki/Chi-squared_test) to test this.
The formula for the Chi-Square Test is:
$$
\chi^2 = \sum_{i=1}^{n} (\frac{(O_i - E_i)^2}{E_i})
$$

- $H_0$: The frequencies of each color are the same.
- $H_a$: The frequencies of each color are different.

Since we have 5 colors, if all the colors are the same, then proportions will be the same.

**Expectation = [0.2, 0.2, 0.2, 0.2, 0.2]**

We test to find a p-value, and compare that to our significance level, or $\alpha$. 
If p-value is less than $\alpha$, then we reject the null hypothesis, $H_0$.''')



csq = chisquare([total_blue_perc, total_green_perc, total_pink_perc,
          total_purple_perc, total_yellow_perc])

cs1, cs2, cs3 = st.columns(3)
with cs1:
  st.metric('Chi-Square Statistic', f"{round(csq[0], 2)}")
with cs2:
  st.metric("p-value", f"{round(csq[1], 2)}")
with cs3:
  st.metric(r"Critical Value \alpha", 0.05)

if csq[1] < 0.05:
  st.markdown('''**The p-value is less than 0.05, so we can reject the null hypothesis.
  The frequencies of the colors are significantly different from being the same.**''')
else:
  st.markdown('''**The p-value is greater than 0.05, so we cannot reject the null hypothesis.
  The frequencies of the colors are not significantly different from being the same.**''')

st.write('---')

st.subheader('So how do we do this?')
st.write("""The short answer: **Statistics and Code!** The longer answer is that we are using the 
Chi-Square Test to test the null hypothesis that the frequencies of each color are the same, and doing
so using the power (and magic) of computer code.""")

st.code(""" 
import pandas as pd
from scipy.stats import chisquare

data = pd.read_excel('./HamlineData.xlsx')
data['total'] = data.Blue + data.Green + data.Pink + data.Purple + data.Yellow

data['blue_perc'] = data.Blue / data.total
data['green_perc'] = data.Green / data.total
data['pink_perc'] = data.Pink / data.total
data['purple_perc'] = data.Purple / data.total
data['yellow_perc'] = data.Yellow / data.total

total_blue_perc = data.Blue.sum() / data.total.sum()
total_green_perc = data.Green.sum() / data.total.sum()
total_pink_perc = data.Pink.sum() / data.total.sum()
total_purple_perc = data.Purple.sum() / data.total.sum()
total_yellow_perc = data.Yellow.sum() / data.total.sum()

csq = chisquare([total_blue_perc, total_green_perc, total_pink_perc,
          total_purple_perc, total_yellow_perc])
""")
