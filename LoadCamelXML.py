import xml.etree.ElementTree as ET

from CamelRoute import CamelRoute

# Load the file and get the Blueprint Root element
root = ET.parse('thecamelfile.xml').getroot()

# Setup the namespace
ns = {'cm': 'http://camel.apache.org/schema/blueprint'}

# create the list and dictionary
routes = []
direct_dic = {}

# For all the CamelContexts in the Blueprint XML
for context in root.findall('cm:camelContext', ns):
    context_id = context.get('id')
    print(context_id)
    route_idx = 0

    # For all the Routes in the CamelContext
    for route in context.findall('cm:route', ns):

        route_id = route.get('id')

        # Get the From element and the uri for the route
        from_e = route.find('cm:from', ns)
        frm = from_e.get('uri')

        # Get the To's and convert to a list of URI's
        to_uris = []
        for to in route.findall('.//cm:to', ns):
            to_uris.append(to.get('uri'))

        # Create thr CamelRoute for the Route and Store it
        node = CamelRoute(direct_dic, route_idx, frm, to_uris, context_id, route_id)

        routes.append(node)
        route_idx += 1

direct_dic = {}
for route in routes:
    if route.is_from_direct():
        direct_dic[route.get_from_direct_target()] = route

for route in routes:
    route.link_direct_routes()


print('\n'.join(map(lambda x: x.__str__(), routes)))



