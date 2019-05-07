class CamelRoute:

    direct_dic = {}

    def __init__(self, direct_dic, route_idx, frm, to, context_id="undefined", name="undefined"):
        self.route_idx = route_idx
        self.context_id = context_id
        self.frm = CamelRouteNode(frm)

        to_nodes = []
        for uri in to:
            to_nodes.append(CamelRouteNode(uri))

        self.to = CamelToList(direct_dic, to_nodes)
        self.direct_dic = direct_dic

        if name is not None:
            self.name = name
        else:
            self.name = "route_{}".format(route_idx)

        if self.is_from_direct():
            direct_dic[self.get_from_direct_target()] = self

    def is_from_direct(self):
        return self.frm.is_direct()

    def get_from_direct_target(self):
        return self.frm.get_direct_target()

    def set_direct_dic(self, dic):
        self.to.direct_dic = dic

    def link_direct_routes(self):
        for to_node in self.to:
            if to_node.is_direct():
                to_node.target = self.direct_dic[to_node.get_direct_target()]

    def __str__(self):
        return "Context id: {node.context_id}\n" \
               "Route Index: {node.route_idx}\n" \
               "Name: {node.name}\n" \
               "From: {node.frm.uri}\n" \
               "{node.to}".format(node=self)


class CamelRouteNode:

    target = None

    def __init__(self, uri):
        self.uri = uri

    def is_direct(self):
        return self.uri.lower().startswith('direct:')

    def get_direct_target(self):
        if self.is_direct():
            idx = self.uri.find('?')
            if self.uri.find('?') < 0:
                idx = len(self.uri)

            return self.uri[7:idx]
        else:
            return None


class CamelToList(list):

    direct_dic = {}

    def __init__(self, direct_dic, to):
        super(CamelToList, self).__init__(to)
        self.direct_dic = direct_dic

    def __str__(self):
        _str = ""
        for to_node in self:
            uri = to_node.uri
            _str += "To: {}\n".format(uri)

            if to_node.target is not None:
                _str += "\t-----> Context id: {node.context_id} " \
                    "Route Index: {node.route_idx} " \
                    "Name: {node.name}\n".format(node=to_node.target)

        return _str
