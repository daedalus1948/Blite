from django.db.models import Q # complex query string for search

def build_Q_dictionary(querystring_dict): # this dictionary is for .filter() complex searches
    Q_dict = Q()
    for key, value in querystring_dict.items():
        if key == "page": # skip page key, this key is for pagination not filtering
            continue
        if key == "author": # foreign-key lookup, modify the string - project specific
            key = "author__username" # correct string
        key += "__icontains"  # SQL LIKE operator
    Q_dict.add(Q(**{key: value}), Q.AND) # build a Q dict out of querystring parameters
    return Q_dict