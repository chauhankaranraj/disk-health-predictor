def extract_smartctl_attrs(daywise_smartctl_data):
    # dummy vars
    emptydict = dict()
    emptylist = list()

    smartctl_attrs = dict()
    for day, daydata in daywise_smartctl_data.items():
        # smart attributes for current day
        day_smartctl_attrs = dict()

        # get smartctl attribute table
        smartctl_attr_table = daydata.get("ata_smart_attributes", emptydict,).get(
            "table",
            emptylist,
        )

        for attr in smartctl_attr_table:
            # ===================== #
            #  get raw smart value
            # ===================== #
            rawvaldict = attr.get("raw")
            if rawvaldict is not None:
                # try to extract numeric value
                # if not available then try to extract string value
                rawval = rawvaldict.get("value", rawvaldict.get("string"))

                # if NA then set to None
                if rawval is None:
                    day_smartctl_attrs[f"smart_{attr['id']}_raw"] = None

                # if string, convert to numeric
                elif isinstance(rawval, str):
                    if rawval.isdigit():
                        day_smartctl_attrs[f"smart_{attr['id']}_raw"] = int(rawval)
                    elif rawval.split(" ")[0].isdigit():
                        day_smartctl_attrs[f"smart_{attr['id']}_raw"] = int(
                            rawval.split(" ")[0]
                        )

                # otherwise simply save the extracted numeric value
                else:
                    day_smartctl_attrs[f"smart_{attr['id']}_raw"] = rawval

            # get normalzied smart value
            day_smartctl_attrs[f"smart_{attr['id']}_normalized"] = attr.get("value")

        # add power on hours manually, if it wasnt extracted from smart attribute table
        if day_smartctl_attrs.get("smart_9_raw") is None:
            day_smartctl_attrs["smart_9_raw"] = daydata.get(
                "power_on_time", emptydict
            ).get("hours")

        # add device capacity
        user_capacity = daydata.get("user_capacity", emptydict).get("bytes")
        if isinstance(user_capacity, dict):
            user_capacity = user_capacity["n"]
        day_smartctl_attrs["user_capacity"] = user_capacity

        # add todays smartctl attrs to dict of all days' smartctl attrs
        smartctl_attrs[day] = day_smartctl_attrs

    return smartctl_attrs
