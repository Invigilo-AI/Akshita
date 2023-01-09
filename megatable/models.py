from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Date,ForeignKey,Boolean

Base = declarative_base()


class Frame(Base):

    __tablename__ = 'frame'
    frame_id = Column(String(200),primary_key=True)
    frame_url = Column(String(200))


    def __repr__(self):
        return "<Frame(frame_id='{}', frame_url='{}')>" \
            .format(self.frame_id,self.frame_url)

class Artifact(Base):

    __tablename__ = 'artifact_reference'
    artifact_type = Column(Integer,primary_key=True)
    artifact_name = Column(String(200))

    def __repr__(self):
        return "<Artifact(artifact_type='{}', artifact_name='{}')>" \
            .format(self.artifact_type,self.artifact_name)

class Customer(Base):

    __tablename__ = 'customer_reference'
    customer_id = Column(Integer(), primary_key=True)
    customer_name = Column(String(255))

    def __repr__(self):
        return "<Customer(customer_id='{}', customer_name='{}')>" \
            .format(self.customer_id, self.customer_name)



class Customer_data(Base):

    __tablename__ = 'customer_data'
    customer_id = Column(Integer, ForeignKey('customer_reference.customer_id'), primary_key=True,nullable=False,)
    frame_id = Column(String(200), ForeignKey('frame.frame_id'), nullable=False)
    frame_date = Column(Date, nullable=False)
    artifact_type = Column(Integer, ForeignKey('artifact_reference.artifact_type'), nullable=False,)

    def __repr__(self):
        return "<Customer_data(customer_id='{}', frame_id='{}', frame_date='{}',artifact_type='{}')>" \
            .format(self.customer_id,self.frame_id,self.frame_date,self.artifact_type)



class Frame_usage(Base):

    __tablename__ = 'frame_usage'
    frame_id = Column(String(50),ForeignKey('frame.frame_id'),primary_key=True )
    usage = Column(Boolean)

    def __repr__(self):
        return "<Frame_usage(frame_id='{}', boolean='{}')>" \
            .format(self.frame_id, self.usage)



class Training( Base):
    __tablename__ = 'training'

    frame_id = Column(String(50),ForeignKey('frame.frame_id'),nullable=False,primary_key=True)
    frame_date = Column(Date,nullable=False)
    customer_id = Column(Integer(),ForeignKey('customer_reference.customer_id'))
    artifact_type = Column(Integer,ForeignKey('artifact_reference.artifact_type'),nullable=False)
    bounding_boxes_url = Column(String(255))
    video_url = Column(String(65535))
    frame_metadata_json = Column(String(65535))



    def __repr__(self):
        return "<Training(frame_id='{}', frame_date='{}', customer_id='{}', artifact_type='{}',bounding_boxes_url='{}',video_url='{}',frame_metadata_json='{}')>" \
            .format(self.frame_id, self.frame_date, self.customer_id, self.artifact_type ,self.bounding_boxes_url,self.video_url,
                    self.frame_metadata_json)




