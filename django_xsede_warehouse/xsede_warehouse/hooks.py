from xsede_warehouse.urls import urlpatterns_internal

def remove_internal_apis(endpoints):
    import pdb
    pdb.set_trace()
    return [
        (path, path_regex, method, callback)
        for (path, path_regex, method, callback) in endpoints
        if path not in urlpatterns_internal
    ]
#    result = []
#    for (path, path_regex, method, callback) in endpoints
#        if path not in urlpatterns_internal:
#            result.append([path, path_regex, method, callback])
#    return(result)
#    for endpoint in endpoints:
#        if endpoint in urlpatterns_internal:
#            pass
#        apidoc_endpoints.append(endpoint)
#    return(apidoc_endpoints)
