# Medication recommendation guidelines

def recommend_asthma_medication(severity, age, history_of_allergy=None):

    if severity == "Intermittent Asthma":
        return "SABA as needed"

    # Mild persistent asthma
    if severity == "mild persistent asthma":
        if 0 <= age <= 4:
            return "low dose ICS"
        elif 5 <= age <= 11:
            return "low dose ICS"
        elif age > 12:
            return "low dose ICS"

    # Moderate persistent asthma
    if severity == "moderate persistent asthma":
        if 0 <= age <= 4:
            return "medium dose ICS"
        elif 5 <= age <= 11:
            return "low-dose ICS + either LABA, LTRA, or theophylline"
        elif age > 12:
            return "low-dose ICS + LABA OR medium-dose ICS"

    # Severe persistent asthma
    if severity == "severe persistent asthma":
        if 0 <= age <= 4:
            return "medium dose ICS"
        elif 5 <= age <= 11 and history_of_allergy is False:
            return "low-dose ICS + either LABA, LTRA, or theophylline OR medium-dose ICS"
        elif age > 12 and history_of_allergy is False:
            return "high-dose ICS + LABA"
        elif age > 12 and history_of_allergy is True:
            return "high-dose ICS + LABA AND consider omalizumab"

    return "No recommendation found for given inputs"
