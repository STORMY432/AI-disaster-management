from classifier import classify_disaster

from agents.flood import flood_agent
from agents.earthquake import earthquake_agent
from agents.cyclone import cyclone_agent
from agents.wildfire import wildfire_agent
from agents.landslide import landslide_agent
from agents.tsunami import tsunami_agent
from agents.general import general_agent



def route_query(prompt: str):


    disaster_type = classify_disaster(prompt)


    print("Detected Disaster:", disaster_type)



    if disaster_type == "flood":

        return flood_agent(prompt)


    elif disaster_type == "earthquake":

        return earthquake_agent(prompt)


    elif disaster_type == "cyclone":

        return cyclone_agent(prompt)


    elif disaster_type == "wildfire":

        return wildfire_agent(prompt)


    elif disaster_type == "landslide":

        return landslide_agent(prompt)


    elif disaster_type == "tsunami":

        return tsunami_agent(prompt)


    else:

        return general_agent(prompt)