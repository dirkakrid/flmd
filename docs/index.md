# flmd
## flask markdown file server-ish thing

### plugins (creation)

`CLASS_NAME.py`

```python
class CLASS_NAME(plugin):
	def __init__(self):
		pass
```
> both the filename, and the classname **must** be the same for it to be called

> *example class, note, `plugin` **must** be an object of the class*

##### functions

```python
def EVENT_NAME(self, *args, **kwargs):
		pass
```
> where event name is the trigger_event name