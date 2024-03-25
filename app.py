import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prometheus_client import Counter, REGISTRY, MetricsHandler
from http.server import HTTPServer
import threading
import socket

##################################################### CONNECTION WITH PROMETHEUS ################################################################################
# I had error with port already being used, this is the link to the github that I used to solve my problem : https://github.com/prometheus/client_python/issues/155
# Custom HTTP Server class for Prometheus with SO_REUSEADDR set
class HttpServerReuseSocket(HTTPServer):
    def server_bind(self):
        """Override server_bind to set SO_REUSEADDR."""
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        HTTPServer.server_bind(self)

# Function to start the HTTP server for Prometheus metrics
def start_custom_http_server(port):
    """Starts a custom HTTP server for Prometheus metrics."""
    try:
        httpd = HttpServerReuseSocket(('', port), MetricsHandler)
        thread = threading.Thread(target=httpd.serve_forever)
        thread.daemon = True
        thread.start()
        return httpd
    except OSError as e:
        if e.errno == 98:  # Error code for address already in use
            print(f"Port {port} is already in use. Prometheus server not started.")
        else:
            raise

# Start the Prometheus HTTP server only once using the session state
if 'prometheus_server' not in st.session_state:
    st.session_state['prometheus_server'] = start_custom_http_server(9000)

# Function to get or create the counter
@st.cache_resource
def get_or_create_counter(name, description, registry=REGISTRY):
    # Check if the counter already exists
    if name in registry._names_to_collectors:
        # Get the existing counter
        return registry._names_to_collectors[name]
    else:
        # Create and return a new counter
        return Counter(name, description, registry=registry)

# Use the function to get or create the counter
c = get_or_create_counter('my_button_clicks', 'Number of clicks on my button')

if st.button('Click Me!'):
    c.inc()
    st.write('Button clicked!')




######################################################## VISUALISATIONS #######################################################################################
@st.cache_data
def load_data():
    data = pd.read_csv("housing.csv")
    return data


data = load_data()


if st.checkbox('Montrer le DataFrame'):
    st.write(data)



# Histogramme de la valeur médiane des maisons
st.subheader('Histogramme de la valeur médiane des maisons')
fig, ax = plt.subplots()
sns.histplot(data['median_house_value'], bins=30, kde=False, ax=ax)
st.pyplot(fig)

# Diagramme de dispersion de la valeur médiane des maisons par rapport au revenu médian
st.subheader('Diagramme de dispersion de la valeur médiane des maisons par rapport au revenu médian')
fig, ax = plt.subplots()
sns.scatterplot(x='median_income', y='median_house_value', data=data, ax=ax)
st.pyplot(fig)


# Diagramme en barres de l'âge médian des maisons
st.subheader('Diagramme en barres de l\'âge médian des maisons')
median_age = data['housing_median_age'].value_counts().sort_index()
fig, ax = plt.subplots()
median_age.plot(kind='bar', ax=ax)
st.pyplot(fig)

# Boîte à moustaches pour les revenus médians
st.subheader('Boîte à moustaches pour les revenus médians')
fig, ax = plt.subplots()
sns.boxplot(data=data, x='ocean_proximity', y='median_income', ax=ax)
st.pyplot(fig)



