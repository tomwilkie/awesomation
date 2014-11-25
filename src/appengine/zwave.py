      value = data['valueId'].copy()

      command_class = value.pop('commandClass')
      index = value.pop('index')
      del value['homeId']
      del value['nodeId']

      self._devices[node_id]['command_classes'][command_class][index] = value
      logging.info(self._devices)

            self._devices[node_id] = {'command_classes': collections.defaultdict(dict)}