class CamelNode:

    direct_dic = {}

    def __init__(self, direct_dic, route_idx, frm, to, context_id="undefined", name="undefined"):
        self.route_idx = route_idx
        self.context_id = context_id
        self.frm = frm
        self.to = CamelToList(direct_dic, to)
        self.direct_dic = direct_dic

        if name is not None:
            self.name = name
        else:
            self.name = "route_{}".format(route_idx)

        if self.is_from_direct():
            direct_dic[self.get_from_direct_target()] = self

    def is_from_direct(self):
        return self.frm.lower().startswith('direct:')

    def get_from_direct_target(self):
        if self.is_from_direct():
            idx = self.frm.find('?')
            if self.frm.find('?') < 0:
                idx = len(self.frm)

            return self.frm[7:idx]
        else:
            return None

    def set_direct_dic(self, dic):
        self.to.diect_dic = dic

    def __str__(self):
        return "Context id: {node.context_id}\n" \
               "Route Index: {node.route_idx}\n" \
               "Name: {node.name}\n" \
               "From: {node.frm}\n" \
               "{node.to}".format(node=self)


class CamelToList(list):

    direct_dic = {}

    def __init__(self, direct_dic, to):
        super(CamelToList, self).__init__(to)
        self.direct_dic = direct_dic

    def __str__(self):
        _str = ""
        for obj in self:
            _str += "To: {}\n".format(obj)

            if obj.lower().startswith('direct:'):
                route = self.direct_dic.get(obj[7:])
                if route is not None:
                    _str += "\t-----> {route.name} \n".format(route=self.direct_dic.get(obj[7:]))

        return _str
