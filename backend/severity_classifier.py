def classify_severity(prompt: str):

    query = prompt.lower()


    # HIGH priority emergency keywords

    high_keywords = [

        "trapped",
        "stuck",
        "injured",
        "help me",
        "emergency",
        "dying",
        "collapsed",
        "collapse",
        "can't escape",
        "cannot escape",
        "people trapped",
        "someone trapped",
        "need rescue",
        "rescue me",
        "urgent",
        "right now",
        "immediately"

    ]


    for word in high_keywords:

        if word in query:

            return "HIGH"



    # MEDIUM priority keywords

    medium_keywords = [

        "warning",
        "approaching",
        "coming",
        "near my area",
        "evacuate",
        "evacuation",
        "danger",
        "risk",
        "alert",
        "storm",
        "heavy rain",
        "strong wind"

    ]


    for word in medium_keywords:

        if word in query:

            return "MEDIUM"



    # Default

    return "LOW"