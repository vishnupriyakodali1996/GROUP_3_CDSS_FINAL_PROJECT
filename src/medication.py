def get_medication(severity, age):
    print("----------------------------------------------------")
    if severity == "Intermittent":
        return "Step 1: SABA as needed"
    elif severity == "Persistent mild":
        if age >= 12:
            return "Step 2: Low dose ICS\n(Beclomethasone MDI 80 mcg, 1 puff AM and 2 puffs PM)"
        else:
            return "Step 2: Low dose ICS\n(Beclomethasone MDI 80 mcg, 1 puff two times per day)"
    elif severity == "Persistent moderate":
        if age >= 12:
            return ("Step 3: Low dose ICS + LABA\n"
                    "(Beclomethasone MDI 80 mcg, 1 puff AM and 2 puffs PM + LABA)\n"
                    "Or Medium dose ICS: 80 mcg, 2-3 puffs, 2x per day")
        else:
            return ("Step 3: Low dose ICS + LABA\n"
                    "(Beclomethasone MDI 80 mcg, 1 puff two times per day + LABA)\n"
                    "Or Medium dose ICS: 80 mcg, 2 puffs, 2x per day")
    elif severity == "Persistent severe":
        if age >= 12:
            return "Step 4: Medium dose ICS + LABA\n(Beclomethasone MDI 80 mcg, 2-3 puffs, 2x per day + LABA)"
        else:
            return "Step 4: Medium dose ICS + LABA\n(Beclomethasone MDI 80 mcg, 2 puffs, 2x per day + LABA)"
