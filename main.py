ITEMS = [
	{"id": 1, "parent": "root"},
	{"id": 2, "parent": 1, "type": "test"},
	{"id": 3, "parent": 1, "type": "test"},
	{"id": 4, "parent": 2, "type": "test"},
	{"id": 5, "parent": 2, "type": "test"},
	{"id": 6, "parent": 2, "type": "test"},
	{"id": 7, "parent": 4, "type": None},
	{"id": 8, "parent": 4, "type": None}
]


# noinspection PyPep8Naming,PyShadowingBuiltins
class TreeStore:
	def __init__(self, items):
		self.items = {}
		for item in items:
			try:
				id = item['id']
			except Exception as ex:
				print('Exception item not have key "id"', ex)
				raise ex
			try:
				_parent = item['parent']
			except Exception as ex:
				print('Exception item not have key "parent"', ex)
				raise ex
			self.items[id] = item
	
	def getAll(self):
		return self.items
	
	def getItem(self, id):
		return self.items.get(id, {})
	
	def getChildren(self, id):
		"""
		Если дерево не большое то можно так, с перебором всех элементов
		"""
		ids = [self.getItem(id)['id']]
		result = []
		while True:
			ids = list(map(
				lambda y: y['id'], filter(
					lambda x: x['parent'] in ids, self.items.values()
				)
			))
			if not ids:
				break
			for _id in ids:
				item = self.getItem(_id)
				if item:
					result.append(item)
		return result
	
	def getChildrenBig(self, id):
		"""
		А если сильно большое то может имеет смысл удалять уже пройденные "id". Либо сделать TreeNode class. Метод лучше по задаче выбирать
		"""
		keys = set(self.items.keys())
		item_id = self.getItem(id)['id']
		try:
			keys.remove(item_id)
		except Exception as _ex:
			pass
		
		ids = [item_id]
		result = []
		while True:
			_ids = []
			for key in keys:
				item = self.getItem(key)
				if item and item['parent'] in ids:
					_ids.append(key)
					result.append(item)
			if not _ids:
				break
			for _id in _ids:
				try:
					keys.remove(_id)
				except Exception as _ex:
					pass
			ids = _ids
		return result
	
	def getAllParents(self, id):
		item = self.items[id]
		result = []
		while True:
			item = self.getItem(item.get('parent'))
			if not item:
				break
			result.append(item)
		return result


if __name__ == '__main__':
	ts = TreeStore(ITEMS)
	print('getAll', ts.getAll())
	print('getItem', ts.getItem(7))
	print('getChildren', ts.getChildren(4))
	print('getChildren', ts.getChildren(5))
	print('getChildrenBig', ts.getChildrenBig(4))
	print('getChildrenBig', ts.getChildrenBig(5))
	print('getAllParents', ts.getAllParents(7))
