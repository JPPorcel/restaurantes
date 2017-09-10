from mongoengine import *
from sitio_web.settings import DBNAME
 
connect(DBNAME)

class restaurants(Document):
    name             = StringField(required=True, max_length=80)
    restaurant_id    = StringField()
    cuisine          = StringField()
    borough          = StringField()
    city             = StringField()
    address          = StringField()
    image			 = ImageField(size=(600, 400, True))
    @property
    def gridfile_attr(self):
		return str(self.image.grid_id)
