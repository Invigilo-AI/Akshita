from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String

Base = declarative_base()


class Frame_test(Base):

    __tablename__ = 'frame_test'
    frame_id = Column(String(200),primary_key=True)
    frame_url = Column(String(200))


    def __repr__(self):
        return "(frame_id='{}', frame_url='{}')" \
            .format(self.frame_id,self.frame_url)
