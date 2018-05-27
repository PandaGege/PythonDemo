# -*- coding:utf-8 -*-

import traceback
import contextlib
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


'''
echo: 用logging模块打印生成的sql
url:
    sqlite:///:memory
    sqlite:///db
    mysql+pymysql://{user}:{passwd}@{host}/{database}?charset=utf8
'''


conninfo = {
    'user': 'regan',
    'passwd': '32DHidsa12937#!',
    'host': 'localhost',
    'database': 'domin'
}


Base = declarative_base()


class Domain(Base):
    __tablename__ = 'domain'
    id = Column(Integer, primary_key=True, autoincrement=True,
                comment=u'自增主键')
    # nullable 可否为空
    # unique 唯一索引
    domain_name = Column(String(255), nullable=False, unique=True,
                         comment=u'域名')
    suffix = Column(String(32), comment=u'后缀')
    '''
    sqlalchemy.dialects.mysql.FLOAT(precision=None, scale=None,\
         asdecimal=False, **kw)
        precision: 总位数
        scale: 小数点后位数
        asdecimal: 是否decimal，decimal比float精度高
        unsigned: 可选，有无符号
        zerofill: 可选,0填充,如果不够指定长度,作为字符串; 但不改变db中的类型
    '''
    cost = Column(Float(8, 2), comment=u'成本')
    sale = Column(Float(precision=8, scale=2, asdecimal=True), comment=u'售价')
    buy_time = Column(DateTime, comment=u'买入时间',
                      default=datetime.datetime.now)
    # onupdate 更新该条记录时自动更新
    update_time = Column(
            DateTime, comment=u'更新时间',
            default=datetime.datetime.now,  onupdate=datetime.datetime.now)


# 此时不会真正连接到数据库，懒加载
engine = create_engine(
        'mysql+pymysql://{user}:{passwd}@{host}/{database}?charset=utf8'
        .format(**conninfo), echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


@contextlib.contextmanager
def get_session():
    try:
        session = Session()
        yield session
    except Exception:
        traceback.print_exc()
        session.rollback()
    finally:
        session.close()


with get_session() as session:
    d1 = Domain()
    d1.domain_name = 'baidu'
    d1.suffix = 'com'
    d1.cost = 1234.88
    session.add(d1)
    session.commit()

    d2 = Domain(domain_name='sian', suffix='app', cost=312.21)
    session.add(d2)
    session.commit()

    d = session.query(Domain).filter(Domain.domain_name == 'baidu').all()
    assert d[0] == d1
