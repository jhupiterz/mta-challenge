from flask_caching import Cache
import plots
import utils

# Initialize the cache (you'll need to pass the server from your main app)
cache = Cache()

# Function to set up the cache with the Flask server
def init_cache(server):
    # Initialize the cache with the Flask server
    return  Cache(server, config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': 'cache-directory'
    })

# Cache the data loading function
@cache.memoize()
def load_large_dataset():
    data_dictionary = utils.get_data_dictionary()
    # Load and preprocess your large dataset
    return {
        "figure_weekly_ridership": plots.create_animation(data_dictionary["df_animation_weekly_ridership"], 1),
        "figure_monthly_ridership": plots.create_animation(data_dictionary["df_animation_monthly_ridership"], 1),
        "figure_weekly_percent": plots.create_animation(data_dictionary["df_animation_weekly_percent"], 2),
        "figure_monthly_percent": plots.create_animation(data_dictionary["df_animation_monthly_percent"], 2)
    }