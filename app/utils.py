import requests


def request_cran(limit, insert):
    package = requests.get("https://cran.r-project.org/src/contrib/PACKAGES")
    list_package = package.text.split("\n\n")

    result_list = []
    for item in list_package:
        dict_default = {}
        for new_item in item.replace(",\n", ",").split("\n"):
            list_dict = new_item.split(":")

            if len(list_dict) < 2:
                for key, value in result_list[-1].items():
                    dict_default[key] = value + list_dict[0]
                result_list[-1] = dict_default
            else:
                dict_default[list_dict[0]] = list_dict[1]
        result_list.append(dict_default)

    return {
        "limit": limit,
        "insert": insert,
        "data": result_list[: (limit + 1)] if limit else result_list,
    }
