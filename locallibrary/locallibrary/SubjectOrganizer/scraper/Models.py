class Subject:
  def __init__(self, name, groups):
    self.name = name
    self.groups = groups


class Group:
  def __init__(self, id_group='', time='', classroom='', is_virtual=False):
    self.id = id_group
    self.time = time
    self.classroom = classroom
    self.is_virtual = is_virtual
